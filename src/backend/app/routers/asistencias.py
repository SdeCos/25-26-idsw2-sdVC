from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies import require_rol
from app.models.usuario import Usuario
from app.repositories.asistencia_repository import AsistenciaRepository
from app.services.alumno_service import ProfesorNoCompetente
from app.services.generador_archivo_asistencias import GeneradorArchivoAsistencias

router = APIRouter(prefix="/asistencias", tags=["asistencias"])

_require_profesor = require_rol(["profesor"])


@router.get("/exportar")
async def exportar_historial_asistencias(
    asignatura_id: int = Query(...),
    desde: date | None = Query(default=None),
    hasta: date | None = Query(default=None),
    usuario: Usuario = Depends(_require_profesor),
    db: AsyncSession = Depends(get_db),
) -> Response:
    # Defensa "Profesor competente": solo asignaturas que imparte.
    ids = {a.id for a in usuario.asignaturas_impartidas}
    if asignatura_id not in ids:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "No impartes esta asignatura"
        ) from ProfesorNoCompetente()

    repo = AsistenciaRepository(db)
    lista = await repo.obtener_por_rango(asignatura_id, desde, hasta)
    contenido = GeneradorArchivoAsistencias().generar_csv(lista)
    filename = f"asistencias-{asignatura_id}-{date.today().isoformat()}.csv"
    return Response(
        content=contenido,
        media_type="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
        },
    )
