from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.grados import GradoOut

CaracterLiteral = Literal["FB", "OB", "OP"]


class AsignaturaOut(BaseModel):
    """Asignatura del catálogo — lectura por GET /asignaturas y /profesores/yo."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    codigo: str
    nombre: str
    ects: float
    caracter: str
    curso_plan: int
    grados: list[GradoOut]


class CrearAsignaturaRequest(BaseModel):
    codigo: str
    nombre: str
    ects: float = Field(gt=0)
    caracter: CaracterLiteral
    curso_plan: int = Field(ge=1, le=6)
    grado_ids: list[int] = Field(min_length=1)


class EditarAsignaturaRequest(BaseModel):
    """Body parcial. `codigo` y `responsable_id` no editables (`extra="ignore"`).

    `grado_ids`, si viene, reemplaza el conjunto entero. Mandar `[]` está
    prohibido por el validador (longitud mínima 1).
    """

    model_config = ConfigDict(extra="ignore")

    nombre: str | None = None
    ects: float | None = Field(default=None, gt=0)
    caracter: CaracterLiteral | None = None
    curso_plan: int | None = Field(default=None, ge=1, le=6)
    grado_ids: list[int] | None = Field(default=None, min_length=1)


class AsignaturaImpartidaOut(BaseModel):
    """Fila de la N:M con auditoría (devuelta por POST /…/asignaturas-impartidas/…)."""

    model_config = ConfigDict(from_attributes=True)

    profesor_id: int
    asignatura_id: int
    responsable_id: int | None
