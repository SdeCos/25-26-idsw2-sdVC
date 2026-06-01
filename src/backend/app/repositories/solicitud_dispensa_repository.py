from datetime import datetime

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.models.matricula import AsignaturaMatriculada, Matricula
from app.models.solicitud_dispensa import EstadoSolicitud, SolicitudDispensa


class SolicitudDispensaRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def _eager(self):
        return (
            select(SolicitudDispensa)
            .options(
                joinedload(SolicitudDispensa.asignatura_matriculada)
                .joinedload(AsignaturaMatriculada.asignatura),
                joinedload(SolicitudDispensa.asignatura_matriculada).joinedload(
                    AsignaturaMatriculada.matricula
                ),
            )
            .order_by(SolicitudDispensa.fecha_solicitud.desc())
        )

    async def obtener_todas(self) -> list[SolicitudDispensa]:
        result = await self.session.execute(self._eager())
        return list(result.unique().scalars().all())

    async def obtener_por_alumno(self, alumno_id: int) -> list[SolicitudDispensa]:
        result = await self.session.execute(
            self._eager().where(SolicitudDispensa.alumno_id == alumno_id)
        )
        return list(result.unique().scalars().all())

    async def obtener_por_id(self, id: int) -> SolicitudDispensa | None:
        result = await self.session.execute(
            self._eager().where(SolicitudDispensa.id == id)
        )
        return result.unique().scalars().first()

    async def obtener_por_filtros(
        self,
        *,
        estado: EstadoSolicitud | None = None,
        alumno_id: int | None = None,
        desde: datetime | None = None,
        hasta: datetime | None = None,
    ) -> list[SolicitudDispensa]:
        stmt = self._eager()
        condiciones = []
        if estado is not None:
            condiciones.append(SolicitudDispensa.estado == estado.value)
        if alumno_id is not None:
            condiciones.append(SolicitudDispensa.alumno_id == alumno_id)
        if desde is not None:
            condiciones.append(SolicitudDispensa.fecha_solicitud >= desde)
        if hasta is not None:
            condiciones.append(SolicitudDispensa.fecha_solicitud <= hasta)
        if condiciones:
            stmt = stmt.where(and_(*condiciones))
        result = await self.session.execute(stmt)
        return list(result.unique().scalars().all())

    async def crear(
        self,
        *,
        alumno_id: int,
        asignatura_matriculada_id: int,
        motivo: str | None,
    ) -> SolicitudDispensa:
        solicitud = SolicitudDispensa(
            alumno_id=alumno_id,
            asignatura_matriculada_id=asignatura_matriculada_id,
            motivo=motivo,
            estado=EstadoSolicitud.PENDIENTE.value,
        )
        self.session.add(solicitud)
        await self.session.commit()
        # Recarga con eager para devolver el agregado completo.
        return await self.obtener_por_id(solicitud.id)  # type: ignore[return-value]

    async def actualizar(
        self, solicitud: SolicitudDispensa, cambios: dict
    ) -> SolicitudDispensa:
        for campo, valor in cambios.items():
            setattr(solicitud, campo, valor)
        await self.session.commit()
        return await self.obtener_por_id(solicitud.id)  # type: ignore[return-value]
