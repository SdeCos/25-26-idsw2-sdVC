from datetime import date

from sqlalchemy import and_, select
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.asistencia import Asistencia
from app.models.sesion_clase import SesionDeClase


class AsistenciaRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def upsert(
        self,
        *,
        sesion_clase_id: int,
        alumno_id: int,
        estado: str,
        justificacion: str | None,
    ) -> Asistencia:
        # Sin INSERT ... ON CONFLICT en SQLAlchemy core async genérico — pero
        # `sqlite_insert` sí lo soporta. Si en el futuro migramos a PostgreSQL,
        # se cambia el import por `postgresql_insert`. Misma forma.
        stmt = sqlite_insert(Asistencia.__table__).values(
            sesion_clase_id=sesion_clase_id,
            alumno_id=alumno_id,
            estado=estado,
            justificacion=justificacion,
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=["sesion_clase_id", "alumno_id"],
            set_={"estado": stmt.excluded.estado, "justificacion": stmt.excluded.justificacion},
        )
        await self.session.execute(stmt)
        await self.session.commit()

        # Recuperamos la fila resultante (única por la UNIQUE compuesta).
        result = await self.session.execute(
            select(Asistencia).where(
                and_(
                    Asistencia.sesion_clase_id == sesion_clase_id,
                    Asistencia.alumno_id == alumno_id,
                )
            )
        )
        return result.unique().scalars().one()

    async def listar_por_sesion(self, sesion_clase_id: int) -> list[Asistencia]:
        result = await self.session.execute(
            select(Asistencia)
            .where(Asistencia.sesion_clase_id == sesion_clase_id)
            .order_by(Asistencia.alumno_id)
        )
        return list(result.unique().scalars().all())

    async def listar_por_alumno(self, alumno_id: int) -> list[Asistencia]:
        """Historial de asistencias de un alumno, más recientes primero.

        `sesion_clase` y `sesion_clase.asignatura` vienen cargados por el
        `lazy="joined"` declarado en los modelos.
        """
        stmt = (
            select(Asistencia)
            .join(SesionDeClase, Asistencia.sesion_clase_id == SesionDeClase.id)
            .where(Asistencia.alumno_id == alumno_id)
            .order_by(SesionDeClase.fecha.desc(), SesionDeClase.hora_inicio.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.unique().scalars().all())

    async def obtener_por_rango(
        self,
        asignatura_id: int,
        desde: date | None,
        hasta: date | None,
    ) -> list[Asistencia]:
        """Asistencias de una asignatura en un rango de fechas.

        Join con sesion_clase para filtrar por asignatura + fecha.
        """
        condiciones = [SesionDeClase.asignatura_id == asignatura_id]
        if desde is not None:
            condiciones.append(SesionDeClase.fecha >= desde)
        if hasta is not None:
            condiciones.append(SesionDeClase.fecha <= hasta)
        stmt = (
            select(Asistencia)
            .join(SesionDeClase, Asistencia.sesion_clase_id == SesionDeClase.id)
            .where(and_(*condiciones))
            .order_by(SesionDeClase.fecha, Asistencia.alumno_id)
        )
        result = await self.session.execute(stmt)
        return list(result.unique().scalars().all())
