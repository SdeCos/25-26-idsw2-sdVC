from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.asignatura import Asignatura


class AsignaturaRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def obtener_por_codigos(
        self, codigos: list[str]
    ) -> dict[str, Asignatura]:
        if not codigos:
            return {}
        result = await self.session.execute(
            select(Asignatura).where(Asignatura.codigo.in_(codigos))
        )
        return {a.codigo: a for a in result.scalars().all()}
