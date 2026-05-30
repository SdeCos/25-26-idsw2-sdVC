from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies import require_rol
from app.models.solicitud_dispensa import SolicitudDispensa
from app.models.usuario import Usuario
from app.repositories.solicitud_dispensa_repository import (
    SolicitudDispensaRepository,
)
from app.schemas.dispensas import (
    CrearSolicitudRequest,
    EditarSolicitudRequest,
    SolicitudDispensaOut,
)
from app.services.solicitud_dispensa_service import (
    CampoNoEditable,
    NoAutorizado,
    ObservacionesRequeridas,
    SolicitudDispensaService,
    SolicitudNoEncontrada,
    TransicionNoValida,
)

router = APIRouter(prefix="/dispensas", tags=["dispensas"])

_require_director_o_alumno = require_rol(["director", "alumno"])
_require_alumno = require_rol(["alumno"])


@router.get("", response_model=list[SolicitudDispensaOut])
async def listar_dispensas(
    usuario: Usuario = Depends(_require_director_o_alumno),
    db: AsyncSession = Depends(get_db),
) -> list[SolicitudDispensa]:
    return await SolicitudDispensaService(
        SolicitudDispensaRepository(db)
    ).listar(usuario)


@router.post(
    "",
    response_model=SolicitudDispensaOut,
    status_code=status.HTTP_201_CREATED,
)
async def crear_dispensa(
    req: CrearSolicitudRequest,
    alumno: Usuario = Depends(_require_alumno),
    db: AsyncSession = Depends(get_db),
) -> SolicitudDispensa:
    return await SolicitudDispensaService(
        SolicitudDispensaRepository(db)
    ).crear(req, alumno)


@router.get("/{solicitud_id}", response_model=SolicitudDispensaOut)
async def consultar_dispensa(
    solicitud_id: int,
    usuario: Usuario = Depends(_require_director_o_alumno),
    db: AsyncSession = Depends(get_db),
) -> SolicitudDispensa:
    service = SolicitudDispensaService(SolicitudDispensaRepository(db))
    try:
        return await service.obtener(solicitud_id, usuario)
    except SolicitudNoEncontrada as exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "Solicitud no encontrada"
        ) from exc
    except NoAutorizado as exc:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "No autorizado para esta solicitud"
        ) from exc


@router.patch("/{solicitud_id}", response_model=SolicitudDispensaOut)
async def editar_dispensa(
    solicitud_id: int,
    req: EditarSolicitudRequest,
    usuario: Usuario = Depends(_require_director_o_alumno),
    db: AsyncSession = Depends(get_db),
) -> SolicitudDispensa:
    service = SolicitudDispensaService(SolicitudDispensaRepository(db))
    try:
        return await service.actualizar(solicitud_id, req, usuario)
    except SolicitudNoEncontrada as exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "Solicitud no encontrada"
        ) from exc
    except NoAutorizado as exc:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "No autorizado para esta solicitud"
        ) from exc
    except TransicionNoValida as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            f"Transición no permitida: {exc.actual} → {exc.nuevo}",
        ) from exc
    except ObservacionesRequeridas as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Las observaciones son obligatorias al rechazar",
        ) from exc
    except CampoNoEditable as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            f"Campo no editable: {exc.campo}",
        ) from exc
