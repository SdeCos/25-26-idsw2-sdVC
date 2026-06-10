from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies import require_rol
from app.models.matricula import Matricula
from app.models.usuario import Usuario
from app.repositories.matricula_repository import MatriculaRepository
from app.schemas.grados import GradoOut
from app.schemas.matriculas import (
    AlumnoMinOut,
    AsignaturaCatalogoEmbedOut,
    AsignaturaMatriculadaDetalleOut,
    MatriculaDetalleOut,
    MatriculaListaItemOut,
    ResponsableMinOut,
)
from app.schemas.paginacion import InformeImportacionMatriculasOut
from app.services.matricula_service import MatriculaService
from app.services.validador_archivo_matriculas import CabeceraInvalida

router = APIRouter(prefix="/matriculas", tags=["matriculas"])

_require_secretaria = require_rol(["secretaria"])


def _a_detalle(m: Matricula) -> MatriculaDetalleOut:
    return MatriculaDetalleOut(
        id=m.id,
        alumno=AlumnoMinOut.model_validate(m.alumno),
        curso_academico=m.curso_academico,
        fecha_importacion=m.fecha_importacion,
        responsable=ResponsableMinOut.model_validate(m.responsable),
        grado=GradoOut.model_validate(m.grado),
        asignaturas_matriculadas=[
            AsignaturaMatriculadaDetalleOut(
                id=am.id,
                n_matricula=am.n_matricula,
                asignatura=AsignaturaCatalogoEmbedOut.model_validate(am.asignatura),
            )
            for am in m.asignaturas_matriculadas
        ],
    )


def _a_item(m: Matricula) -> MatriculaListaItemOut:
    return MatriculaListaItemOut(
        id=m.id,
        alumno=AlumnoMinOut.model_validate(m.alumno),
        curso_academico=m.curso_academico,
        grado=GradoOut.model_validate(m.grado),
        fecha_importacion=m.fecha_importacion,
        num_asignaturas=len(m.asignaturas_matriculadas),
    )


@router.get("", response_model=list[MatriculaListaItemOut])
async def listar_matriculas(
    _: Usuario = Depends(_require_secretaria),
    db: AsyncSession = Depends(get_db),
) -> list[MatriculaListaItemOut]:
    return [_a_item(m) for m in await MatriculaRepository(db).listar()]


@router.post(
    "/importar", response_model=InformeImportacionMatriculasOut
)
async def importar_matriculas(
    archivos: list[UploadFile] = File(...),
    usuario: Usuario = Depends(_require_secretaria),
    db: AsyncSession = Depends(get_db),
) -> InformeImportacionMatriculasOut:
    contenidos: list[tuple[str, bytes]] = []
    for a in archivos:
        contenidos.append((a.filename or "matriculas.csv", await a.read()))
    try:
        return await MatriculaService(db).importar(
            contenidos, responsable_id=usuario.id
        )
    except CabeceraInvalida as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            f"Cabecera inválida en {exc.archivo}: {exc.mensaje}",
        ) from exc


@router.get("/{matricula_id}", response_model=MatriculaDetalleOut)
async def consultar_detalle_matricula(
    matricula_id: int,
    _: Usuario = Depends(_require_secretaria),
    db: AsyncSession = Depends(get_db),
) -> MatriculaDetalleOut:
    m = await MatriculaRepository(db).obtener_por_id(matricula_id)
    if m is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "Matrícula no encontrada"
        )
    return _a_detalle(m)
