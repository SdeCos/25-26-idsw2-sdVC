from datetime import date, datetime, time

from pydantic import BaseModel, ConfigDict

from app.models.sesion_clase import EstadoSesionClase
from app.schemas.asignaturas import AsignaturaOut


class ProfesorMinOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    apellidos: str


class SesionDeClaseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    profesor: ProfesorMinOut
    asignatura: AsignaturaOut
    grupo: str
    aula: str
    fecha: date
    hora_inicio: time
    hora_fin: time
    tema: str
    estado: EstadoSesionClase
    fecha_creacion: datetime


class CrearSesionClaseRequest(BaseModel):
    """`DatosSesionClase` del análisis — Parameter Object materializado como schema.

    `profesor_id` no aparece: se auto-puebla desde la sesión (defensa contra
    suplantación). Si llega en el body, Pydantic lo ignora por `extra="ignore"`.
    """

    model_config = ConfigDict(extra="ignore")

    asignatura_id: int
    grupo: str
    aula: str
    fecha: date
    hora_inicio: time
    hora_fin: time
    tema: str


class EditarSesionClaseRequest(BaseModel):
    """PATCH unificado — edición de campos editables o transición de estado.

    Invariantes de edición materializadas por contrato:
    - `asignatura_id`, `grupo`, `profesor_id` ausentes → descartados por
      `extra="ignore"` si llegan.
    - `estado` solo admite transición a CERRADA (cierre); el Service valida.
    """

    model_config = ConfigDict(extra="ignore")

    fecha: date | None = None
    hora_inicio: time | None = None
    hora_fin: time | None = None
    aula: str | None = None
    tema: str | None = None
    estado: EstadoSesionClase | None = None
