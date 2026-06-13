from pydantic import BaseModel, ConfigDict, EmailStr


class CrearAlumnoRequest(BaseModel):
    """Alta individual de Alumno por Secretaria (POST /alumnos).

    Materializa el value object `DatosPersonalesAlumno` del análisis. El
    `tipo` no aparece — está fijo en "alumno" y lo aplica el router antes de
    delegar en `UsuarioService.crear`. El alta usa el canal `/alumnos` (no
    `/usuarios`) para reforzar el reparto Administrador↔Secretaria.

    `grado_id` opcional: si viene, el alta crea además una Matrícula vacía
    para el curso académico vigente. El detalle (asignaturas) se carga después
    por `importarMatriculas` o por edición. Si no viene, el alumno queda sin
    matrícula y se le matricula más tarde.
    """

    username: str
    password: str
    nombre: str
    apellidos: str
    email: EmailStr
    grado_id: int | None = None


class AlumnoListaItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    nombre: str
    apellidos: str
    email: str
    activo: bool


class AsignaturaMatriculadaDelAlumnoOut(BaseModel):
    """Vista plana de una AsignaturaMatriculada para el selector de dispensa.

    Permite que `CrearSolicitudDispensaSecretariaPage` y `CrearSolicitudPage`
    (Alumno) consuman el mismo endpoint para listar las asignaturas en las que
    el alumno está matriculado.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    codigo: str
    nombre: str
    curso_academico: str
    n_matricula: int


class AsignaturaMatriculadaConAsistenciaOut(AsignaturaMatriculadaDelAlumnoOut):
    """Variante para la ficha del alumno (Profesor/Secretaria).

    Añade los contadores de asistencia (presentes / sesiones cerradas) y el
    porcentaje. Frontend lo usa para mostrar un badge con el umbral del 70%.
    `total_sesiones == 0` significa que aún no se ha pasado lista de ninguna
    sesión cerrada en esa asignatura — el porcentaje es None.
    """

    presentes: int = 0
    total_sesiones: int = 0
    porcentaje_asistencia: float | None = None


class AlumnoEnAsignaturaOut(BaseModel):
    """Listado del Profesor — alumnos matriculados en una asignatura.

    Derivado del join Matricula → AsignaturaMatriculada → Asignatura. La
    `Secretaria` usa `AlumnoListaItemOut` (sin contexto académico); el Profesor
    necesita `carnet`/`curso_academico`/`estado_matricula`.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    nombre: str
    apellidos: str
    email: str
    carnet: str  # alias de `username` por ahora (sin atributo separado)
    curso_academico: str
    estado_matricula: str = "activa"


class AsistenciaEnFichaOut(BaseModel):
    """Referencia mínima de una asistencia para mostrar en la ficha del Alumno."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    sesion_clase_id: int
    asignatura_codigo: str
    fecha: str
    estado: str


class AlumnoDetalleOut(BaseModel):
    """Ficha completa del Alumno para el Profesor / la Secretaria."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    nombre: str
    apellidos: str
    email: str
    activo: bool
    asignaturas_matriculadas: list[AsignaturaMatriculadaConAsistenciaOut] = []
    asistencias: list[AsistenciaEnFichaOut] = []
