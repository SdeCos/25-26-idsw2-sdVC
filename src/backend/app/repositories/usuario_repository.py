from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.usuario import (
    Administrador,
    Alumno,
    DirectorDeGrado,
    Profesor,
    SecretariaAcademica,
    Usuario,
)

# Mapa explícito tipo → clase concreta. SQLAlchemy hace lo mismo por debajo
# vía `polymorphic_map`, pero hacerlo explícito mantiene la decisión visible
# en código y obliga a actualizarlo al añadir un subtipo nuevo.
TIPO_A_CLASE: dict[str, type[Usuario]] = {
    "alumno": Alumno,
    "profesor": Profesor,
    "director": DirectorDeGrado,
    "secretaria": SecretariaAcademica,
    "administrador": Administrador,
}


class TipoUsuarioInvalido(Exception):
    pass


class UsuarioRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def obtener_por_username(self, username: str) -> Usuario | None:
        result = await self.session.execute(
            select(Usuario).where(Usuario.username == username)
        )
        return result.scalar_one_or_none()

    async def obtener_por_id(self, id: int) -> Usuario | None:
        return await self.session.get(Usuario, id)

    async def obtener_todos(self) -> list[Usuario]:
        result = await self.session.execute(select(Usuario).order_by(Usuario.id))
        return list(result.scalars().all())

    async def crear(
        self,
        tipo: str,
        username: str,
        password_hash: str,
        nombre: str,
        apellidos: str,
        email: str,
    ) -> Usuario:
        cls = TIPO_A_CLASE.get(tipo)
        if cls is None:
            raise TipoUsuarioInvalido(tipo)
        usuario = cls(
            username=username,
            password_hash=password_hash,
            nombre=nombre,
            apellidos=apellidos,
            email=email,
        )
        self.session.add(usuario)
        await self.session.commit()
        await self.session.refresh(usuario)
        return usuario

    async def actualizar(self, usuario: Usuario, cambios: dict) -> Usuario:
        for campo, valor in cambios.items():
            setattr(usuario, campo, valor)
        await self.session.commit()
        await self.session.refresh(usuario)
        return usuario
