from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_current_user
from app.models.usuario import Usuario
from app.schemas.asignaturas import AsignaturaOut

router = APIRouter(prefix="/profesores", tags=["profesores"])


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
