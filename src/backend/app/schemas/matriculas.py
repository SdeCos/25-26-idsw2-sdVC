from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AsignaturaCatalogoEmbedOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    codigo: str
    nombre: str
    ects: float
    caracter: str
    curso_plan: int


class AsignaturaMatriculadaDetalleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    n_matricula: int
    asignatura: AsignaturaCatalogoEmbedOut


class AlumnoMinOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    nombre: str
    apellidos: str
    email: str


class ResponsableMinOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    apellidos: str


class MatriculaDetalleOut(BaseModel):
    """Agregado completo de matrícula con sus asignaturas y datos derivados."""

    id: int
    alumno: AlumnoMinOut
    curso_academico: str
    fecha_importacion: datetime
    responsable: ResponsableMinOut
    plan_estudios: str
    facultad: str
    asignaturas_matriculadas: list[AsignaturaMatriculadaDetalleOut]


class MatriculaListaItemOut(BaseModel):
    id: int
    alumno: AlumnoMinOut
    curso_academico: str
    plan_estudios: str
    grado: str  # alias visible (= plan_estudios) por compatibilidad con el prototipo
    fecha_importacion: datetime
    num_asignaturas: int
