from app.core.security import create_access_token, verify_password
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.auth import TokenResponse, UsuarioOut


class CredencialesInvalidas(Exception):
    pass


class UsuarioInactivo(Exception):
    pass


class AuthService:
    def __init__(self, usuario_repo: UsuarioRepository) -> None:
        self.usuario_repo = usuario_repo

    async def autenticar(self, username: str, password: str) -> Usuario:
        usuario = await self.usuario_repo.obtener_por_username(username)
        if usuario is None or not verify_password(password, usuario.password_hash):
            raise CredencialesInvalidas
        if not usuario.activo:
            raise UsuarioInactivo
        return usuario

    def emitir_token(self, usuario: Usuario) -> TokenResponse:
        payload = {"sub": str(usuario.id), "tipo": usuario.tipo}
        token, expira_en = create_access_token(payload)
        return TokenResponse(
            access_token=token,
            expira_en=expira_en,
            usuario=UsuarioOut.model_validate(usuario),
        )
