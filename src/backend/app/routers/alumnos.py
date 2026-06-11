from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.core.database import get_db
from app.dependencies import require_rol
from app.models.matricula import AsignaturaMatriculada, Matricula
from app.models.usuario import Alumno, Usuario
from app.repositories.asistencia_repository import AsistenciaRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.alumnos import (
    AlumnoDetalleOut,
    AlumnoEnAsignaturaOut,
    AlumnoListaItemOut,
    AsignaturaMatriculadaDelAlumnoOut,
    AsistenciaEnFichaOut,
    CrearAlumnoRequest,
)
from app.schemas.paginacion import (
    InformeImportacionAlumnosOut,
    PaginaOut,
)
from app.schemas.usuarios import CrearUsuarioRequest, UsuarioDetalleOut
from app.services.alumno_service import (
    AlumnoNoEncontrado,
    AlumnoService,
    ProfesorNoCompetente,
)
from app.services.usuario_service import UsernameEnUso, UsuarioService
from app.services.validador_archivo_listas_alumnos import CabeceraInvalida

router = APIRouter(prefix="/alumnos", tags=["alumnos"])

_require_secretaria = require_rol(["secretaria"])
_require_alumno_o_secretaria = require_rol(["alumno", "secretaria"])
_require_profesor_o_secretaria = require_rol(["profesor", "secretaria"])


@router.get("")
async def listar_alumnos(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=25, ge=1, le=200),
    q: str | None = Query(default=None),
    asignatura_id: int | None = Query(default=None),
    usuario: Usuario = Depends(_require_profesor_o_secretaria),
    db: AsyncSession = Depends(get_db),
):
    """Listado de alumnos.

    - Secretaria: paginado con búsqueda libre `q`; `asignatura_id` opcional.
    - Profesor:   exige `asignatura_id`; defensa "Profesor competente"; sin `q`.

    Schemas distintos según rol:
      Secretaria → `PaginaOut[AlumnoListaItemOut]`
      Profesor   → `PaginaOut[AlumnoEnAsignaturaOut]` (con datos académicos)
    """
    repo = UsuarioRepository(db)
    service = AlumnoService(repo)

    if usuario.tipo == "profesor":
        if asignatura_id is None:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                "Falta el parámetro `asignatura_id`",
            )
        try:
            items, total = await service.listar_por_asignatura(
                asignatura_id, page, size, usuario
            )
        except ProfesorNoCompetente as exc:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN, "No impartes esta asignatura"
            ) from exc

        # Para cada alumno, derivar curso_academico de su matrícula que incluye
        # la asignatura. Una query batch a `matriculas + asignaturas_matriculadas`.
        cursos = await _cursos_por_alumno(db, [a.id for a in items], asignatura_id)
        salida = [
            AlumnoEnAsignaturaOut(
                id=a.id,
                username=a.username,
                nombre=a.nombre,
                apellidos=a.apellidos,
                email=a.email,
                carnet=a.username,
                curso_academico=cursos.get(a.id, ""),
            )
            for a in items
        ]
        return PaginaOut[AlumnoEnAsignaturaOut](
            items=salida, total=total, page=page, size=size
        )

    # Secretaria: sin scoping. Es un departamento colectivo, ve todos los alumnos.
    if asignatura_id is not None:
        items, total = await repo.buscar_por_asignatura(asignatura_id, page, size)
    else:
        items, total = await repo.buscar_alumnos(page, size, q)
    return PaginaOut[AlumnoListaItemOut](
        items=[AlumnoListaItemOut.model_validate(a) for a in items],
        total=total,
        page=page,
        size=size,
    )


async def _cursos_por_alumno(
    db: AsyncSession, alumno_ids: list[int], asignatura_id: int
) -> dict[int, str]:
    if not alumno_ids:
        return {}
    stmt = (
        select(Matricula.alumno_id, Matricula.curso_academico)
        .join(
            AsignaturaMatriculada,
            AsignaturaMatriculada.matricula_id == Matricula.id,
        )
        .where(
            Matricula.alumno_id.in_(alumno_ids),
            AsignaturaMatriculada.asignatura_id == asignatura_id,
        )
    )
    result = await db.execute(stmt)
    return {row[0]: row[1] for row in result.all()}


@router.post(
    "",
    response_model=UsuarioDetalleOut,
    status_code=status.HTTP_201_CREATED,
)
async def crear_alumno(
    req: CrearAlumnoRequest,
    _: Usuario = Depends(_require_secretaria),
    db: AsyncSession = Depends(get_db),
) -> Usuario:
    """Alta individual de Alumno por Secretaria.

    Canal separado de `POST /usuarios` (Administrador) — el reparto
    Administrador↔Secretaria también vive en la superficie HTTP. El polimorfismo
    de instanciación se delega en `UsuarioService.crear` con `tipo="alumno"`
    fijado aquí; el cliente no lo envía.
    """
    usuario_req = CrearUsuarioRequest(
        tipo="alumno",
        username=req.username,
        password=req.password,
        nombre=req.nombre,
        apellidos=req.apellidos,
        email=req.email,
        grado_id=None,
    )
    service = UsuarioService(UsuarioRepository(db))
    try:
        return await service.crear(usuario_req)
    except UsernameEnUso as exc:
        raise HTTPException(
            status.HTTP_409_CONFLICT, "El username ya está en uso"
        ) from exc


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


@router.get("/{alumno_id}", response_model=AlumnoDetalleOut)
async def obtener_alumno(
    alumno_id: int,
    usuario: Usuario = Depends(_require_profesor_o_secretaria),
    db: AsyncSession = Depends(get_db),
) -> AlumnoDetalleOut:
    service = AlumnoService(UsuarioRepository(db))
    try:
        alumno: Alumno = await service.obtener_detalle(alumno_id, usuario)
    except AlumnoNoEncontrado as exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "Alumno no encontrado"
        ) from exc
    except ProfesorNoCompetente as exc:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "No impartes ninguna asignatura de este alumno",
        ) from exc

    am_list: list[AsignaturaMatriculadaDelAlumnoOut] = []
    for m in getattr(alumno, "matriculas_cargadas", []):
        for am in m.asignaturas_matriculadas:
            am_list.append(
                AsignaturaMatriculadaDelAlumnoOut(
                    id=am.id,
                    codigo=am.asignatura.codigo,
                    nombre=am.asignatura.nombre,
                    curso_academico=m.curso_academico,
                    n_matricula=am.n_matricula,
                )
            )

    asistencia_repo = AsistenciaRepository(db)
    asistencias_raw = await asistencia_repo.listar_por_alumno(alumno_id)
    asistencias_out = [
        AsistenciaEnFichaOut(
            id=a.id,
            sesion_clase_id=a.sesion_clase_id,
            asignatura_codigo=a.sesion_clase.asignatura.codigo,
            fecha=a.sesion_clase.fecha.isoformat(),
            estado=a.estado,
        )
        for a in asistencias_raw
    ]

    return AlumnoDetalleOut(
        id=alumno.id,
        username=alumno.username,
        nombre=alumno.nombre,
        apellidos=alumno.apellidos,
        email=alumno.email,
        activo=alumno.activo,
        asignaturas_matriculadas=am_list,
        asistencias=asistencias_out,
    )
