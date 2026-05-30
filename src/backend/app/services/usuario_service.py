from sqlalchemy.exc import IntegrityError

from app.core.security import hash_password
from app.models.usuario import Usuario
from app.repositories.usuario_repository import (
    TipoUsuarioInvalido,
    UsuarioRepository,
)
from app.schemas.usuarios import CrearUsuarioRequest, EditarUsuarioRequest


class UsernameEnUso(Exception):
    pass


class UsuarioNoEncontrado(Exception):
    pass


class UsuarioService:
    def __init__(self, repo: UsuarioRepository) -> None:
        self.repo = repo

    async def crear(self, datos: CrearUsuarioRequest) -> Usuario:
        try:
            return await self.repo.crear(
                tipo=datos.tipo,
                username=datos.username,
                password_hash=hash_password(datos.password),
                nombre=datos.nombre,
                apellidos=datos.apellidos,
                email=datos.email,
            )
        except IntegrityError as exc:
            await self.repo.session.rollback()
            raise UsernameEnUso(datos.username) from exc
        except TipoUsuarioInvalido:
            raise

    async def actualizar(self, id: int, datos: EditarUsuarioRequest) -> Usuario:
        usuario = await self.repo.obtener_por_id(id)
        if usuario is None:
            raise UsuarioNoEncontrado(id)

        # Solo campos que el cliente ha enviado (no None → tocar; None → no tocar).
        cambios = datos.model_dump(exclude_unset=True)

        if "password" in cambios:
            cambios["password_hash"] = hash_password(cambios.pop("password"))

        try:
            return await self.repo.actualizar(usuario, cambios)
        except IntegrityError as exc:
            await self.repo.session.rollback()
            raise UsernameEnUso(cambios.get("username", "")) from exc
