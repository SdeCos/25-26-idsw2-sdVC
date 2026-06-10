from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies import get_current_user
from app.models.usuario import Usuario
from app.repositories.asignatura_repository import AsignaturaRepository
from app.schemas.asignaturas import AsignaturaOut

router = APIRouter(prefix="/asignaturas", tags=["asignaturas"])


@router.get("", response_model=list[AsignaturaOut])
async def listar_asignaturas(
    _: Usuario = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Catálogo completo de asignaturas. Lectura para cualquier usuario autenticado."""
    return await AsignaturaRepository(db).obtener_todas()
