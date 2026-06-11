from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies import get_current_user, require_rol
from app.models.usuario import Usuario
from app.repositories.asignatura_repository import AsignaturaRepository
from app.repositories.grado_repository import GradoRepository
from app.schemas.asignaturas import (
    AsignaturaOut,
    CrearAsignaturaRequest,
    EditarAsignaturaRequest,
)
from app.services.asignatura_service import (
    AsignaturaConReferencias,
    AsignaturaNoEncontrada,
    AsignaturaService,
    CodigoEnUso,
    GradoNoEncontrado,
)

router = APIRouter(prefix="/asignaturas", tags=["asignaturas"])

_require_secretaria = require_rol(["secretaria"])


def _service(db: AsyncSession) -> AsignaturaService:
    return AsignaturaService(AsignaturaRepository(db), GradoRepository(db))


@router.get("", response_model=list[AsignaturaOut])
async def listar_asignaturas(
    _: Usuario = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Catálogo completo de asignaturas. Lectura para cualquier usuario autenticado."""
    return await _service(db).listar()


@router.post(
    "", response_model=AsignaturaOut, status_code=status.HTTP_201_CREATED
)
async def crear_asignatura(
    req: CrearAsignaturaRequest,
    usuario: Usuario = Depends(_require_secretaria),
    db: AsyncSession = Depends(get_db),
) -> AsignaturaOut:
    try:
        a = await _service(db).crear(req, responsable_id=usuario.id)
    except GradoNoEncontrado as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            f"El grado {exc} no existe",
        ) from exc
    except CodigoEnUso as exc:
        raise HTTPException(
            status.HTTP_409_CONFLICT, f"Código de asignatura en uso: {exc}"
        ) from exc
    return AsignaturaOut.model_validate(a)


@router.get("/{asignatura_id}", response_model=AsignaturaOut)
async def obtener_asignatura(
    asignatura_id: int,
    _: Usuario = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> AsignaturaOut:
    try:
        a = await _service(db).obtener(asignatura_id)
    except AsignaturaNoEncontrada as exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "Asignatura no encontrada"
        ) from exc
    return AsignaturaOut.model_validate(a)


@router.patch("/{asignatura_id}", response_model=AsignaturaOut)
async def actualizar_asignatura(
    asignatura_id: int,
    req: EditarAsignaturaRequest,
    _: Usuario = Depends(_require_secretaria),
    db: AsyncSession = Depends(get_db),
) -> AsignaturaOut:
    try:
        a = await _service(db).actualizar(asignatura_id, req)
    except AsignaturaNoEncontrada as exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "Asignatura no encontrada"
        ) from exc
    except GradoNoEncontrado as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            f"El grado {exc} no existe",
        ) from exc
    return AsignaturaOut.model_validate(a)


@router.delete("/{asignatura_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_asignatura(
    asignatura_id: int,
    _: Usuario = Depends(_require_secretaria),
    db: AsyncSession = Depends(get_db),
) -> None:
    try:
        await _service(db).eliminar(asignatura_id)
    except AsignaturaNoEncontrada as exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "Asignatura no encontrada"
        ) from exc
    except AsignaturaConReferencias as exc:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            f"No se puede eliminar: la asignatura tiene referencias en {list(exc.refs.keys())}",
        ) from exc
