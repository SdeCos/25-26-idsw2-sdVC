from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.asistencia import EstadoAsistencia


class AlumnoEnAsistenciaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    nombre: str
    apellidos: str


class AsistenciaOut(BaseModel):
    """Una asistencia individual (devuelta tras PUT y por GET de la sesión)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    sesion_clase_id: int
    alumno: AlumnoEnAsistenciaOut
    estado: EstadoAsistencia
    justificacion: str | None
    fecha_registro: datetime


class AsistenciaIn(BaseModel):
    """Body del PUT. La sesión y el alumno van en path."""

    model_config = ConfigDict(extra="ignore")

    estado: EstadoAsistencia
    justificacion: str | None = None


class AsistenciaResumenOut(BaseModel):
    """Resumen embebido en la ficha del alumno — referencia placeholder.

    Hoy las listas siempre vienen vacías ([]); se rellenarán cuando entren
    las consultas que las usen (consultarDetalleAlumno extendido).
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    sesion_clase_id: int
    estado: EstadoAsistencia
    justificacion: str | None
    fecha_registro: datetime
