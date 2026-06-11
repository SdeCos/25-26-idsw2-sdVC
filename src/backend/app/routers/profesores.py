from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies import get_current_user, require_rol
from app.models.usuario import Profesor, Usuario
from app.schemas.asignaturas import AsignaturaOut
from app.schemas.usuarios import UsuarioDetalleOut

router = APIRouter(prefix="/profesores", tags=["profesores"])


@router.get("", response_model=list[UsuarioDetalleOut])
async def listar_profesores(
    _: Usuario = Depends(require_rol(["secretaria"])),
    db: AsyncSession = Depends(get_db),
) -> list[Usuario]:
    """Listado de profesores (y directores de grado) — selector para asignaciones."""
    result = await db.execute(
        select(Profesor).order_by(Profesor.apellidos, Profesor.nombre)
    )
    return list(result.scalars().all())


@router.get("/yo/asignaturas", response_model=list[AsignaturaOut])
async def asignaturas_impartidas_propias(
    usuario: Usuario = Depends(get_current_user),
):
    """Asignaturas que el Profesor logueado imparte (carga de pestañas)."""
    if usuario.tipo != "profesor":
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "Solo disponible para profesores"
        )
    return usuario.asignaturas_impartidas
