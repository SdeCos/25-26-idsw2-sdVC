from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies import require_rol
from app.models.usuario import Usuario
from app.repositories.usuario_repository import (
    TipoUsuarioInvalido,
    UsuarioRepository,
)
from app.schemas.usuarios import (
    CrearUsuarioRequest,
    EditarUsuarioRequest,
    UsuarioDetalleOut,
)
from app.services.usuario_service import (
    UsernameEnUso,
    UsuarioNoEncontrado,
    UsuarioService,
)

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
    dependencies=[Depends(require_rol(["administrador"]))],
)


@router.get("", response_model=list[UsuarioDetalleOut])
async def listar_usuarios(db: AsyncSession = Depends(get_db)) -> list[Usuario]:
    return await UsuarioRepository(db).obtener_todos()


@router.post("", response_model=UsuarioDetalleOut, status_code=status.HTTP_201_CREATED)
async def crear_usuario(
    req: CrearUsuarioRequest, db: AsyncSession = Depends(get_db)
) -> Usuario:
    service = UsuarioService(UsuarioRepository(db))
    try:
        return await service.crear(req)
    except UsernameEnUso as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, "El username ya está en uso") from exc
    except TipoUsuarioInvalido as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Tipo no válido: {exc}") from exc


@router.get("/{usuario_id}", response_model=UsuarioDetalleOut)
async def consultar_usuario(usuario_id: int, db: AsyncSession = Depends(get_db)) -> Usuario:
    usuario = await UsuarioRepository(db).obtener_por_id(usuario_id)
    if usuario is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuario no encontrado")
    return usuario


@router.patch("/{usuario_id}", response_model=UsuarioDetalleOut)
async def editar_usuario(
    usuario_id: int,
    req: EditarUsuarioRequest,
    db: AsyncSession = Depends(get_db),
) -> Usuario:
    service = UsuarioService(UsuarioRepository(db))
    try:
        return await service.actualizar(usuario_id, req)
    except UsuarioNoEncontrado as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuario no encontrado") from exc
    except UsernameEnUso as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, "El username ya está en uso") from exc
