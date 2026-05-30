from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.solicitud_dispensa import EstadoSolicitud


class AlumnoMinOut(BaseModel):
    """Datos mínimos del alumno propietario embebidos en la solicitud."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    nombre: str
    apellidos: str


class ResponsableMinOut(BaseModel):
    """Datos mínimos del Director que tomó la solicitud para revisión."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    apellidos: str


class SolicitudDispensaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    alumno: AlumnoMinOut
    asignatura: str
    periodo: str
    horario: str
    motivo: str | None
    estado: EstadoSolicitud
    observaciones: str | None
    fecha_solicitud: datetime
    fecha_resolucion: datetime | None
    responsable: ResponsableMinOut | None


class CrearSolicitudRequest(BaseModel):
    """Alta de una solicitud por el Alumno.

    `alumno_id` no aparece: se resuelve desde `Sesion.usuario.id` en el Service
    (propietario implícito, evita suplantación).
    """

    model_config = ConfigDict(extra="ignore")

    asignatura: str
    periodo: str
    horario: str
    motivo: str


class EditarSolicitudRequest(BaseModel):
    """PATCH unificado para Alumno y Director.

    Todos los campos son opcionales (`None` = no tocar). La `PoliticaAcceso`
    aplicable según el rol decide qué se permite tocar:

      - Alumno (sólo PENDIENTE): motivo, horario, asignatura, periodo + estado→ANULADA
      - Director: observaciones + estado→EN_REVISION|APROBADA|RECHAZADA
    """

    model_config = ConfigDict(extra="ignore")

    estado: EstadoSolicitud | None = None
    motivo: str | None = None
    horario: str | None = None
    asignatura: str | None = None
    periodo: str | None = None
    observaciones: str | None = None
