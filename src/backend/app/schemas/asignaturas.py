from pydantic import BaseModel, ConfigDict

from app.schemas.grados import GradoOut


class AsignaturaOut(BaseModel):
    """Asignatura del catálogo — lectura por GET /asignaturas y /profesores/yo."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    codigo: str
    nombre: str
    ects: float
    caracter: str
    curso_plan: int
    grado: GradoOut
