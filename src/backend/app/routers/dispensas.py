from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies import require_rol
from app.models.solicitud_dispensa import EstadoSolicitud, SolicitudDispensa
from app.models.usuario import Usuario
from app.repositories.solicitud_dispensa_repository import (
    SolicitudDispensaRepository,
)
from app.schemas.dispensas import (
    CrearSolicitudRequest,
    EditarSolicitudRequest,
    SolicitudDispensaOut,
)
from app.services.generador_archivo_dispensas import GeneradorArchivoDispensas
from app.services.solicitud_dispensa_service import (
    AsignaturaMatriculadaIncoherente,
    AsignaturaMatriculadaNoExiste,
    CampoNoEditable,
    NoAutorizado,
    ObservacionesRequeridas,
    SolicitudDispensaService,
    SolicitudNoEncontrada,
    TransicionNoValida,
)

router = APIRouter(prefix="/dispensas", tags=["dispensas"])

_require_lectura = require_rol(["director", "alumno", "secretaria", "profesor"])
_require_creacion = require_rol(["alumno", "secretaria"])
_require_secretaria = require_rol(["secretaria"])


@router.get("", response_model=list[SolicitudDispensaOut])
async def listar_dispensas(
    alumno_id: int | None = Query(default=None),
    usuario: Usuario = Depends(_require_lectura),
    db: AsyncSession = Depends(get_db),
) -> list[SolicitudDispensa]:
    return await SolicitudDispensaService(
        SolicitudDispensaRepository(db)
    ).listar(usuario, alumno_id_filtro=alumno_id)


@router.get("/exportar")
async def exportar_dispensas(
    estado: EstadoSolicitud | None = Query(default=None),
    alumno_id: int | None = Query(default=None),
    desde: datetime | None = Query(default=None),
    hasta: datetime | None = Query(default=None),
    _: Usuario = Depends(_require_secretaria),
    db: AsyncSession = Depends(get_db),
) -> Response:
    repo = SolicitudDispensaRepository(db)
    lista = await repo.obtener_por_filtros(
        estado=estado, alumno_id=alumno_id, desde=desde, hasta=hasta
    )
    contenido = GeneradorArchivoDispensas().generar_csv(lista)
    filename = f"dispensas-{date.today().isoformat()}.csv"
    return Response(
        content=contenido,
        media_type="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
        },
    )


@router.post(
    "",
    response_model=SolicitudDispensaOut,
    status_code=status.HTTP_201_CREATED,
)
async def crear_dispensa(
    req: CrearSolicitudRequest,
    usuario: Usuario = Depends(_require_creacion),
    db: AsyncSession = Depends(get_db),
) -> SolicitudDispensa:
    service = SolicitudDispensaService(SolicitudDispensaRepository(db))
    try:
        return await service.crear(req, usuario)
    except NoAutorizado as exc:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "No autorizado para crear esta solicitud"
        ) from exc
    except AsignaturaMatriculadaNoExiste as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Asignatura matriculada no encontrada",
        ) from exc
    except AsignaturaMatriculadaIncoherente as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "La asignatura matriculada no pertenece al alumno indicado",
        ) from exc


@router.get("/{solicitud_id}", response_model=SolicitudDispensaOut)
async def consultar_dispensa(
    solicitud_id: int,
    usuario: Usuario = Depends(_require_lectura),
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
    usuario: Usuario = Depends(_require_lectura),
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
    except AsignaturaMatriculadaNoExiste as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Asignatura matriculada no encontrada",
        ) from exc
    except AsignaturaMatriculadaIncoherente as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "La asignatura matriculada no pertenece al alumno",
        ) from exc
