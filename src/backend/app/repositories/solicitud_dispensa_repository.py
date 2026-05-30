from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.solicitud_dispensa import EstadoSolicitud, SolicitudDispensa


class SolicitudDispensaRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def obtener_todas(self) -> list[SolicitudDispensa]:
        result = await self.session.execute(
            select(SolicitudDispensa).order_by(SolicitudDispensa.fecha_solicitud.desc())
        )
        return list(result.unique().scalars().all())

    async def obtener_por_alumno(self, alumno_id: int) -> list[SolicitudDispensa]:
        result = await self.session.execute(
            select(SolicitudDispensa)
            .where(SolicitudDispensa.alumno_id == alumno_id)
            .order_by(SolicitudDispensa.fecha_solicitud.desc())
        )
        return list(result.unique().scalars().all())

    async def obtener_por_id(self, id: int) -> SolicitudDispensa | None:
        return await self.session.get(SolicitudDispensa, id)

    async def crear(
        self,
        *,
        alumno_id: int,
        asignatura: str,
        periodo: str,
        horario: str,
        motivo: str | None,
    ) -> SolicitudDispensa:
        solicitud = SolicitudDispensa(
            alumno_id=alumno_id,
            asignatura=asignatura,
            periodo=periodo,
            horario=horario,
            motivo=motivo,
            estado=EstadoSolicitud.PENDIENTE.value,
        )
        self.session.add(solicitud)
        await self.session.commit()
        await self.session.refresh(solicitud)
        return solicitud

    async def actualizar(
        self, solicitud: SolicitudDispensa, cambios: dict
    ) -> SolicitudDispensa:
        for campo, valor in cambios.items():
            setattr(solicitud, campo, valor)
        await self.session.commit()
        await self.session.refresh(solicitud)
        return solicitud
