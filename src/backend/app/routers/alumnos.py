from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.core.database import get_db
from app.dependencies import require_rol
from app.models.matricula import AsignaturaMatriculada, Matricula
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.alumnos import (
    AlumnoListaItemOut,
    AsignaturaMatriculadaDelAlumnoOut,
)
from app.schemas.paginacion import (
    InformeImportacionAlumnosOut,
    PaginaOut,
)
from app.services.alumno_service import AlumnoService
from app.services.validador_archivo_listas_alumnos import CabeceraInvalida

router = APIRouter(prefix="/alumnos", tags=["alumnos"])

_require_secretaria = require_rol(["secretaria"])
_require_alumno_o_secretaria = require_rol(["alumno", "secretaria"])


@router.get("", response_model=PaginaOut[AlumnoListaItemOut])
async def listar_alumnos(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=25, ge=1, le=200),
    q: str | None = Query(default=None),
    _: Usuario = Depends(_require_secretaria),
    db: AsyncSession = Depends(get_db),
) -> PaginaOut[AlumnoListaItemOut]:
    items, total = await UsuarioRepository(db).buscar_alumnos(page, size, q)
    return PaginaOut[AlumnoListaItemOut](
        items=[AlumnoListaItemOut.model_validate(a) for a in items],
        total=total,
        page=page,
        size=size,
    )


@router.post(
    "/importar",
    response_model=InformeImportacionAlumnosOut,
)
async def importar_listas_alumnos(
    archivos: list[UploadFile] = File(...),
    _: Usuario = Depends(_require_secretaria),
    db: AsyncSession = Depends(get_db),
) -> InformeImportacionAlumnosOut:
    contenidos: list[tuple[str, bytes]] = []
    for a in archivos:
        contenidos.append((a.filename or "archivo.csv", await a.read()))
    service = AlumnoService(UsuarioRepository(db))
    try:
        return await service.importar(contenidos)
    except CabeceraInvalida as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            f"Cabecera inválida en {exc.archivo}: {exc.mensaje}",
        ) from exc


@router.get(
    "/{alumno_id}/asignaturas-matriculadas",
    response_model=list[AsignaturaMatriculadaDelAlumnoOut],
)
async def asignaturas_matriculadas_del_alumno(
    alumno_id: int,
    usuario: Usuario = Depends(_require_alumno_o_secretaria),
    db: AsyncSession = Depends(get_db),
) -> list[AsignaturaMatriculadaDelAlumnoOut]:
    # El Alumno solo puede consultar las suyas (defensa contra escaneo).
    if usuario.tipo == "alumno" and usuario.id != alumno_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "No autorizado")
    stmt = (
        select(AsignaturaMatriculada)
        .join(AsignaturaMatriculada.matricula)
        .where(Matricula.alumno_id == alumno_id)
        .options(
            joinedload(AsignaturaMatriculada.asignatura),
            joinedload(AsignaturaMatriculada.matricula),
        )
        .order_by(Matricula.curso_academico.desc())
    )
    result = await db.execute(stmt)
    salida: list[AsignaturaMatriculadaDelAlumnoOut] = []
    for am in result.unique().scalars().all():
        salida.append(
            AsignaturaMatriculadaDelAlumnoOut(
                id=am.id,
                codigo=am.asignatura.codigo,
                nombre=am.asignatura.nombre,
                curso_academico=am.matricula.curso_academico,
                n_matricula=am.n_matricula,
            )
        )
    return salida
