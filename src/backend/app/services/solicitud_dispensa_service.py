from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.matricula import AsignaturaMatriculada
from app.models.solicitud_dispensa import EstadoSolicitud, SolicitudDispensa
from app.models.usuario import Usuario
from app.repositories.solicitud_dispensa_repository import (
    SolicitudDispensaRepository,
)
from app.schemas.dispensas import (
    CrearSolicitudRequest,
    EditarSolicitudRequest,
)
from app.services.politica_acceso import politica_para


class SolicitudNoEncontrada(Exception):
    pass


class TransicionNoValida(Exception):
    def __init__(self, actual: str, nuevo: str) -> None:
        super().__init__(f"Transición {actual} → {nuevo} no permitida")
        self.actual = actual
        self.nuevo = nuevo


class ObservacionesRequeridas(Exception):
    pass


class CampoNoEditable(Exception):
    def __init__(self, campo: str) -> None:
        super().__init__(f"Campo {campo!r} no editable para este rol/estado")
        self.campo = campo


class NoAutorizado(Exception):
    pass


class AsignaturaMatriculadaNoExiste(Exception):
    pass


class AsignaturaMatriculadaIncoherente(Exception):
    """La asignatura matriculada no pertenece al alumno indicado."""

    pass


class SolicitudDispensaService:
    def __init__(self, repo: SolicitudDispensaRepository) -> None:
        self.repo = repo

    @property
    def session(self) -> AsyncSession:
        return self.repo.session

    async def _asignatura_matriculada(
        self, asignatura_matriculada_id: int
    ) -> AsignaturaMatriculada:
        stmt = (
            select(AsignaturaMatriculada)
            .where(AsignaturaMatriculada.id == asignatura_matriculada_id)
            .options(joinedload(AsignaturaMatriculada.matricula))
        )
        result = await self.session.execute(stmt)
        am = result.unique().scalars().first()
        if am is None:
            raise AsignaturaMatriculadaNoExiste(asignatura_matriculada_id)
        return am

    async def listar(
        self, usuario: Usuario, alumno_id_filtro: int | None = None
    ) -> list[SolicitudDispensa]:
        return await politica_para(usuario).obtener_listado(
            self.repo, usuario, alumno_id_filtro
        )

    async def obtener(self, id: int, usuario: Usuario) -> SolicitudDispensa:
        solicitud = await self.repo.obtener_por_id(id)
        if solicitud is None:
            raise SolicitudNoEncontrada(id)
        if not politica_para(usuario).puede_ver(solicitud, usuario):
            raise NoAutorizado
        return solicitud

    async def crear(
        self, datos: CrearSolicitudRequest, usuario: Usuario
    ) -> SolicitudDispensa:
        # Resolución del alumno propietario.
        # - Alumno: se ignora `alumno_id` del body (defensa contra suplantación).
        # - Secretaria: `alumno_id` viene explícito; rechazamos si falta.
        if usuario.tipo == "alumno":
            alumno_id = usuario.id
        elif usuario.tipo == "secretaria":
            if datos.alumno_id is None:
                raise NoAutorizado
            alumno_id = datos.alumno_id
        else:
            raise NoAutorizado

        # La asignatura matriculada debe pertenecer al alumno indicado.
        am = await self._asignatura_matriculada(datos.asignatura_matriculada_id)
        # `am.matricula` está eager-loaded vía joinedload en el modelo.
        if am.matricula.alumno_id != alumno_id:
            raise AsignaturaMatriculadaIncoherente

        return await self.repo.crear(
            alumno_id=alumno_id,
            asignatura_matriculada_id=datos.asignatura_matriculada_id,
            motivo=datos.motivo,
        )

    async def actualizar(
        self,
        id: int,
        datos: EditarSolicitudRequest,
        usuario: Usuario,
    ) -> SolicitudDispensa:
        solicitud = await self.repo.obtener_por_id(id)
        if solicitud is None:
            raise SolicitudNoEncontrada(id)

        politica = politica_para(usuario)
        if not politica.puede_ver(solicitud, usuario):
            raise NoAutorizado

        cambios: dict = {}
        enviados = datos.model_dump(exclude_unset=True)

        # Transición de estado (si se envió `estado`)
        if datos.estado is not None:
            estado_actual = EstadoSolicitud(solicitud.estado)
            nuevo = datos.estado
            if (estado_actual, nuevo) not in politica.transiciones_permitidas():
                raise TransicionNoValida(estado_actual.value, nuevo.value)
            if nuevo is EstadoSolicitud.RECHAZADA and not (
                datos.observaciones and datos.observaciones.strip()
            ):
                raise ObservacionesRequeridas
            cambios["estado"] = nuevo.value
            cambios.update(politica.side_effects(solicitud, nuevo, usuario))
            if datos.observaciones is not None:
                cambios["observaciones"] = datos.observaciones

        editables = politica.campos_editables(solicitud)
        for campo, valor in enviados.items():
            if campo == "estado":
                continue
            if campo == "observaciones" and datos.estado is not None:
                continue
            if campo not in editables:
                raise CampoNoEditable(campo)
            cambios[campo] = valor

        # Si se cambia la asignatura matriculada, validar que pertenece al alumno.
        if "asignatura_matriculada_id" in cambios:
            am = await self._asignatura_matriculada(cambios["asignatura_matriculada_id"])
            if am.matricula.alumno_id != solicitud.alumno_id:
                raise AsignaturaMatriculadaIncoherente

        return await self.repo.actualizar(solicitud, cambios)
