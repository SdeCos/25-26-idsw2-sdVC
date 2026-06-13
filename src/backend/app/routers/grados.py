from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies import require_rol
from app.models.usuario import Usuario
from app.repositories.grado_repository import GradoRepository
from app.schemas.grados import CrearGradoRequest, EditarGradoRequest, GradoOut
from app.services.grado_service import (
    CodigoEnUso,
    GradoConReferencias,
    GradoNoEncontrado,
    GradoService,
)

router = APIRouter(prefix="/grados", tags=["grados"])

_require_secretaria = require_rol(["secretaria"])
# GET es selector compartido: Secretaria lo usa en /grados, /asignaturas y
# /alumnos/nuevo; Administrador en /usuarios/nuevo para crear directores. El
# CRUD (POST/PATCH/DELETE) sigue siendo Secretaria.
_require_lectura_grados = require_rol(["secretaria", "administrador"])


@router.get("", response_model=list[GradoOut])
async def listar_grados(
    _: Usuario = Depends(_require_lectura_grados),
    db: AsyncSession = Depends(get_db),
) -> list[GradoOut]:
    grados = await GradoService(GradoRepository(db)).listar()
    return [GradoOut.model_validate(g) for g in grados]


@router.post("", response_model=GradoOut, status_code=status.HTTP_201_CREATED)
async def crear_grado(
    req: CrearGradoRequest,
    _: Usuario = Depends(_require_secretaria),
    db: AsyncSession = Depends(get_db),
) -> GradoOut:
    service = GradoService(GradoRepository(db))
    try:
        g = await service.crear(req)
    except CodigoEnUso as exc:
        raise HTTPException(
            status.HTTP_409_CONFLICT, f"Código de grado en uso: {exc}"
        ) from exc
    return GradoOut.model_validate(g)


@router.get("/{grado_id}", response_model=GradoOut)
async def obtener_grado(
    grado_id: int,
    _: Usuario = Depends(_require_secretaria),
    db: AsyncSession = Depends(get_db),
) -> GradoOut:
    try:
        g = await GradoService(GradoRepository(db)).obtener(grado_id)
    except GradoNoEncontrado as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Grado no encontrado") from exc
    return GradoOut.model_validate(g)


@router.patch("/{grado_id}", response_model=GradoOut)
async def actualizar_grado(
    grado_id: int,
    req: EditarGradoRequest,
    _: Usuario = Depends(_require_secretaria),
    db: AsyncSession = Depends(get_db),
) -> GradoOut:
    try:
        g = await GradoService(GradoRepository(db)).actualizar(grado_id, req)
    except GradoNoEncontrado as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Grado no encontrado") from exc
    return GradoOut.model_validate(g)


@router.delete("/{grado_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_grado(
    grado_id: int,
    _: Usuario = Depends(_require_secretaria),
    db: AsyncSession = Depends(get_db),
) -> None:
    try:
        await GradoService(GradoRepository(db)).eliminar(grado_id)
    except GradoNoEncontrado as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Grado no encontrado") from exc
    except GradoConReferencias as exc:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            f"No se puede eliminar: el grado tiene referencias en {list(exc.refs.keys())}",
        ) from exc
