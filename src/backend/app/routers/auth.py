from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.auth import LoginRequest, TokenResponse, UsuarioOut
from app.services.auth_service import AuthService, CredencialesInvalidas, UsuarioInactivo

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    service = AuthService(UsuarioRepository(db))
    try:
        usuario = await service.autenticar(req.username, req.password)
    except CredencialesInvalidas as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Credenciales no válidas") from exc
    except UsuarioInactivo as exc:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Usuario inactivo") from exc
    return service.emitir_token(usuario)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(_: Usuario = Depends(get_current_user)) -> None:
    # No-op futuro-proof — punto de extensión para blacklist o auditoría.
    return None


@router.get("/me", response_model=UsuarioOut)
async def me(usuario: Usuario = Depends(get_current_user)) -> Usuario:
    return usuario
