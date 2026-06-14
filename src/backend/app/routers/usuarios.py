from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies import get_current_user, require_rol
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

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


def _autorizar_acceso_a(target: Usuario, actor: Usuario) -> None:
    """Política per-target para `GET/PATCH /usuarios/{id}`:
    - target.tipo == 'alumno' → Secretaria (Admin no opera sobre alumnos, M4).
    - target.tipo != 'alumno' → Administrador (cuentas de personal).
    """
    rol_requerido = "secretaria" if target.tipo == "alumno" else "administrador"
    if actor.tipo != rol_requerido:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "No autorizado para esta operación"
        )


@router.get(
    "",
    response_model=list[UsuarioDetalleOut],
    dependencies=[Depends(require_rol(["administrador"]))],
)
async def listar_usuarios(db: AsyncSession = Depends(get_db)) -> list[Usuario]:
    return await UsuarioRepository(db).obtener_todos()


@router.post(
    "",
    response_model=UsuarioDetalleOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_rol(["administrador"]))],
)
async def crear_usuario(
    req: CrearUsuarioRequest, db: AsyncSession = Depends(get_db)
) -> Usuario:
    if req.tipo == "alumno":
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "El alta de alumno corresponde a Secretaría (POST /alumnos).",
        )
    service = UsuarioService(UsuarioRepository(db))
    try:
        return await service.crear(req)
    except UsernameEnUso as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, "El username ya está en uso") from exc
    except TipoUsuarioInvalido as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Tipo no válido: {exc}") from exc


@router.get("/{usuario_id}", response_model=UsuarioDetalleOut)
async def consultar_usuario(
    usuario_id: int,
    db: AsyncSession = Depends(get_db),
    actor: Usuario = Depends(get_current_user),
) -> Usuario:
    usuario = await UsuarioRepository(db).obtener_por_id(usuario_id)
    if usuario is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuario no encontrado")
    _autorizar_acceso_a(usuario, actor)
    return usuario


@router.patch("/{usuario_id}", response_model=UsuarioDetalleOut)
async def editar_usuario(
    usuario_id: int,
    req: EditarUsuarioRequest,
    db: AsyncSession = Depends(get_db),
    actor: Usuario = Depends(get_current_user),
) -> Usuario:
    repo = UsuarioRepository(db)
    target = await repo.obtener_por_id(usuario_id)
    if target is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuario no encontrado")
    _autorizar_acceso_a(target, actor)
    service = UsuarioService(repo)
    try:
        return await service.actualizar(usuario_id, req)
    except UsuarioNoEncontrado as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuario no encontrado") from exc
    except UsernameEnUso as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, "El username ya está en uso") from exc
