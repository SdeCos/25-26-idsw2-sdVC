from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.asistencia import Asistencia
from app.models.matricula import AsignaturaMatriculada, Matricula
from app.models.sesion_clase import EstadoSesionClase, SesionDeClase
from app.models.usuario import Usuario
from app.repositories.asistencia_repository import AsistenciaRepository
from app.repositories.sesion_clase_repository import SesionClaseRepository
from app.schemas.asistencias import AsistenciaIn


class AsistenciaNoEditable(Exception):
    """Propietario inválido o sesión cerrada."""


class AlumnoNoMatriculado(Exception):
    """El alumno no está matriculado en la asignatura de la sesión."""


class SesionClaseNoEncontradaParaAsistencia(Exception):
    pass


class AsistenciaService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = AsistenciaRepository(session)
        self.sesion_repo = SesionClaseRepository(session)

    async def _alumno_matriculado_en(
        self, alumno_id: int, asignatura_id: int
    ) -> bool:
        stmt = (
            select(AsignaturaMatriculada.id)
            .join(Matricula, AsignaturaMatriculada.matricula_id == Matricula.id)
            .where(
                Matricula.alumno_id == alumno_id,
                AsignaturaMatriculada.asignatura_id == asignatura_id,
            )
            .limit(1)
        )
        result = await self.session.execute(stmt)
        return result.first() is not None

    async def marcar(
        self,
        sesion_id: int,
        alumno_id: int,
        datos: AsistenciaIn,
        usuario: Usuario,
    ) -> Asistencia:
        sesion = await self.sesion_repo.obtener_por_id(sesion_id)
        if sesion is None:
            raise SesionClaseNoEncontradaParaAsistencia
        if sesion.profesor_id != usuario.id:
            raise AsistenciaNoEditable("no es tu sesión")
        if EstadoSesionClase(sesion.estado) is EstadoSesionClase.CERRADA:
            raise AsistenciaNoEditable("sesión cerrada — no se puede marcar")
        if not await self._alumno_matriculado_en(alumno_id, sesion.asignatura_id):
            raise AlumnoNoMatriculado
        return await self.repo.upsert(
            sesion_clase_id=sesion_id,
            alumno_id=alumno_id,
            estado=datos.estado.value,
            justificacion=datos.justificacion,
        )

    async def listar_por_sesion(
        self, sesion_id: int, usuario: Usuario
    ) -> list[Asistencia]:
        sesion = await self.sesion_repo.obtener_por_id(sesion_id)
        if sesion is None:
            raise SesionClaseNoEncontradaParaAsistencia
        if sesion.profesor_id != usuario.id:
            raise AsistenciaNoEditable("no es tu sesión")
        return await self.repo.listar_por_sesion(sesion_id)


def serializar_sesion_para_csv(asistencia: Asistencia) -> dict:
    """Aplanado para el CSV — usado por el generador."""
    s = asistencia.sesion_clase
    a = asistencia.alumno
    return {
        "fecha": s.fecha.isoformat(),
        "asignatura": s.asignatura.codigo if s.asignatura else "",
        "grupos": ", ".join(s.grupos or []),
        "aula": s.aula,
        "alumno_username": a.username,
        "alumno_nombre": a.nombre,
        "alumno_apellidos": a.apellidos,
        "estado": asistencia.estado,
        "justificacion": asistencia.justificacion or "",
    }
