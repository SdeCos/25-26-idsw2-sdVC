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


class SolicitudDispensaService:
    def __init__(self, repo: SolicitudDispensaRepository) -> None:
        self.repo = repo

    async def listar(self, usuario: Usuario) -> list[SolicitudDispensa]:
        return await politica_para(usuario).obtener_listado(self.repo, usuario)

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
        # El POST solo lo permitimos al Alumno (require_rol ya filtra a este nivel).
        # alumno_id se resuelve desde la sesión — patrón "propietario implícito".
        if usuario.tipo != "alumno":
            raise NoAutorizado
        return await self.repo.crear(
            alumno_id=usuario.id,
            asignatura=datos.asignatura,
            periodo=datos.periodo,
            horario=datos.horario,
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
            # observaciones acompaña a la transición (no se valida contra editables).
            if datos.observaciones is not None:
                cambios["observaciones"] = datos.observaciones

        # Edición de campos. `estado` ya tratado arriba; `observaciones` solo
        # se salta si vino acompañando a una transición (ya aplicada al cambios).
        editables = politica.campos_editables(solicitud)
        for campo, valor in enviados.items():
            if campo == "estado":
                continue
            if campo == "observaciones" and datos.estado is not None:
                continue  # ya aplicada con la transición
            if campo not in editables:
                raise CampoNoEditable(campo)
            cambios[campo] = valor

        return await self.repo.actualizar(solicitud, cambios)
