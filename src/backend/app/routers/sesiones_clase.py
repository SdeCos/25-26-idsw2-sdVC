from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies import require_rol
from app.models.usuario import Usuario
from app.repositories.sesion_clase_repository import SesionClaseRepository
from app.schemas.asistencias import AsistenciaIn, AsistenciaOut
from app.schemas.sesiones_clase import (
    CrearSesionClaseRequest,
    EditarSesionClaseRequest,
    SesionDeClaseOut,
)
from app.services.asistencia_service import (
    AlumnoNoMatriculado,
    AsistenciaNoEditable,
    AsistenciaService,
    SesionClaseNoEncontradaParaAsistencia,
)
from app.services.sesion_clase_service import (
    SesionClaseInvalida,
    SesionClaseNoEditable,
    SesionClaseNoEncontrada,
    SesionClaseService,
)

router = APIRouter(prefix="/sesiones-clase", tags=["sesiones-clase"])

_require_profesor = require_rol(["profesor"])


@router.get("", response_model=list[SesionDeClaseOut])
async def listar_sesiones(
    usuario: Usuario = Depends(_require_profesor),
    db: AsyncSession = Depends(get_db),
):
    return await SesionClaseService(SesionClaseRepository(db)).listar(usuario)


@router.post(
    "",
    response_model=SesionDeClaseOut,
    status_code=status.HTTP_201_CREATED,
)
async def crear_sesion(
    req: CrearSesionClaseRequest,
    usuario: Usuario = Depends(_require_profesor),
    db: AsyncSession = Depends(get_db),
):
    service = SesionClaseService(SesionClaseRepository(db))
    try:
        return await service.crear(req, usuario)
    except SesionClaseInvalida as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)) from exc


@router.get("/{sesion_id}", response_model=SesionDeClaseOut)
async def obtener_sesion(
    sesion_id: int,
    usuario: Usuario = Depends(_require_profesor),
    db: AsyncSession = Depends(get_db),
):
    service = SesionClaseService(SesionClaseRepository(db))
    try:
        return await service.obtener(sesion_id, usuario)
    except SesionClaseNoEncontrada as exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "Sesión no encontrada"
        ) from exc
    except SesionClaseNoEditable as exc:
        raise HTTPException(status.HTTP_403_FORBIDDEN, str(exc)) from exc


@router.patch("/{sesion_id}", response_model=SesionDeClaseOut)
async def editar_sesion(
    sesion_id: int,
    req: EditarSesionClaseRequest,
    usuario: Usuario = Depends(_require_profesor),
    db: AsyncSession = Depends(get_db),
):
    service = SesionClaseService(SesionClaseRepository(db))
    try:
        return await service.actualizar(sesion_id, req, usuario)
    except SesionClaseNoEncontrada as exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "Sesión no encontrada"
        ) from exc
    except SesionClaseNoEditable as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)
        ) from exc
    except SesionClaseInvalida as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)
        ) from exc


# ──────────────────────────────────────────────
# Sub-recurso /sesiones-clase/{id}/asistencias
# ──────────────────────────────────────────────


@router.get(
    "/{sesion_id}/asistencias", response_model=list[AsistenciaOut]
)
async def listar_asistencias_de_sesion(
    sesion_id: int,
    usuario: Usuario = Depends(_require_profesor),
    db: AsyncSession = Depends(get_db),
):
    service = AsistenciaService(db)
    try:
        return await service.listar_por_sesion(sesion_id, usuario)
    except SesionClaseNoEncontradaParaAsistencia as exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "Sesión no encontrada"
        ) from exc
    except AsistenciaNoEditable as exc:
        raise HTTPException(status.HTTP_403_FORBIDDEN, str(exc)) from exc


@router.put(
    "/{sesion_id}/asistencias/{alumno_id}", response_model=AsistenciaOut
)
async def marcar_asistencia(
    sesion_id: int,
    alumno_id: int,
    req: AsistenciaIn,
    usuario: Usuario = Depends(_require_profesor),
    db: AsyncSession = Depends(get_db),
):
    service = AsistenciaService(db)
    try:
        return await service.marcar(sesion_id, alumno_id, req, usuario)
    except SesionClaseNoEncontradaParaAsistencia as exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "Sesión no encontrada"
        ) from exc
    except AsistenciaNoEditable as exc:
        # propietario / sesión cerrada → 403 si "no es tu sesión", 422 si "sesión cerrada"
        if "no es tu sesión" in str(exc):
            raise HTTPException(status.HTTP_403_FORBIDDEN, str(exc)) from exc
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)
        ) from exc
    except AlumnoNoMatriculado as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "El alumno no está matriculado en la asignatura de la sesión",
        ) from exc
