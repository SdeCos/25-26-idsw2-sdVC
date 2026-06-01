from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginaOut(BaseModel, Generic[T]):
    """Wrapper genérico para endpoints paginados.

    `items` lleva la página actual; `total` el conteo global para que el
    paginador del frontend pinte "página X de Y".
    """

    items: list[T]
    total: int
    page: int
    size: int


class ErrorImportacionOut(BaseModel):
    """Una incidencia detectada durante una importación masiva."""

    archivo: str
    fila: int
    mensaje: str


class InformeImportacionAlumnosOut(BaseModel):
    creados: int
    actualizados: int
    errores: list[ErrorImportacionOut]


class InformeImportacionMatriculasOut(BaseModel):
    matriculas_creadas: int
    asignaturas_matriculadas_creadas: int
    errores: list[ErrorImportacionOut]
