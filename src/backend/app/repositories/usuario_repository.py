from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.usuario import Usuario


class UsuarioRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def obtener_por_username(self, username: str) -> Usuario | None:
        result = await self.session.execute(select(Usuario).where(Usuario.username == username))
        return result.scalar_one_or_none()

    async def obtener_por_id(self, id: int) -> Usuario | None:
        return await self.session.get(Usuario, id)
