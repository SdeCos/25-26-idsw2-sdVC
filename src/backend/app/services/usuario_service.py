from sqlalchemy.exc import IntegrityError

from app.core.security import hash_password
from app.models.asignatura import Asignatura
from app.models.profesor_asignatura import AsignaturaImpartida
from app.models.usuario import Profesor, Usuario
from app.repositories.asignatura_repository import AsignaturaRepository
from app.repositories.usuario_repository import (
    TipoUsuarioInvalido,
    UsuarioRepository,
)
from app.schemas.usuarios import CrearUsuarioRequest, EditarUsuarioRequest


class UsernameEnUso(Exception):
    pass


class UsuarioNoEncontrado(Exception):
    pass


class NoEsProfesor(Exception):
    pass


class AsignaturaNoEncontrada(Exception):
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
                grado_id=datos.grado_id,
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

    async def _exigir_profesor(self, profesor_id: int) -> Profesor:
        usuario = await self.repo.obtener_por_id(profesor_id)
        if usuario is None:
            raise UsuarioNoEncontrado(profesor_id)
        if not isinstance(usuario, Profesor):
            # Profesor incluye DirectorDeGrado (jerarquía). El resto no.
            raise NoEsProfesor(profesor_id)
        return usuario

    async def obtener_impartidas(self, profesor_id: int) -> list[Asignatura]:
        await self._exigir_profesor(profesor_id)
        return await self.repo.obtener_impartidas(profesor_id)

    async def asignar(
        self,
        profesor_id: int,
        asignatura_id: int,
        responsable_id: int,
        asignatura_repo: AsignaturaRepository,
    ) -> tuple[AsignaturaImpartida, bool]:
        await self._exigir_profesor(profesor_id)
        if not await asignatura_repo.obtener_por_id(asignatura_id):
            raise AsignaturaNoEncontrada(asignatura_id)
        return await self.repo.crear_imparte(
            profesor_id, asignatura_id, responsable_id
        )

    async def desasignar(self, profesor_id: int, asignatura_id: int) -> bool:
        await self._exigir_profesor(profesor_id)
        return await self.repo.eliminar_imparte(profesor_id, asignatura_id)
