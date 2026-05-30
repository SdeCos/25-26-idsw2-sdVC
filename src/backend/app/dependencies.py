from collections.abc import Callable, Coroutine
from typing import Any

import jwt as pyjwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> Usuario:
    if credentials is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token ausente")
    try:
        payload = decode_access_token(credentials.credentials)
        usuario_id = int(payload["sub"])
    except (pyjwt.PyJWTError, KeyError, ValueError) as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token inválido") from exc

    usuario = await UsuarioRepository(db).obtener_por_id(usuario_id)
    if usuario is None or not usuario.activo:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Usuario no válido")
    return usuario


def require_rol(
    roles: list[str],
) -> Callable[[Usuario], Coroutine[Any, Any, Usuario]]:
    """Factory de dependencies para proteger endpoints por rol.

    Uso: `Depends(require_rol(["administrador"]))`.
    """

    async def check(usuario: Usuario = Depends(get_current_user)) -> Usuario:
        if usuario.tipo not in roles:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN, "No autorizado para esta operación"
            )
        return usuario

    return check
