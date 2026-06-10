from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.solicitud_dispensa import EstadoSolicitud
from app.schemas.grados import GradoOut


class AlumnoMinOut(BaseModel):
    """Datos mínimos del alumno propietario embebidos en la solicitud."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    nombre: str
    apellidos: str


class ResponsableMinOut(BaseModel):
    """Datos mínimos del usuario que tomó la solicitud para revisión."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    apellidos: str


class AsignaturaEmbedOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    codigo: str
    nombre: str
    ects: float
    caracter: str
    curso_plan: int
    grado: GradoOut


class AsignaturaMatriculadaEmbedOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    n_matricula: int
    asignatura: AsignaturaEmbedOut


class SolicitudDispensaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    alumno: AlumnoMinOut
    asignatura_matriculada: AsignaturaMatriculadaEmbedOut
    motivo: str | None
    estado: EstadoSolicitud
    observaciones: str | None
    fecha_solicitud: datetime
    fecha_resolucion: datetime | None
    responsable: ResponsableMinOut | None


class CrearSolicitudRequest(BaseModel):
    """Alta de una solicitud.

    Para el Alumno: `alumno_id` se descarta (se resuelve desde la sesión, patrón
    propietario implícito).

    Para la Secretaria: `alumno_id` debe venir explícito (opera en nombre de).
    """

    model_config = ConfigDict(extra="ignore")

    alumno_id: int | None = None
    asignatura_matriculada_id: int
    motivo: str


class EditarSolicitudRequest(BaseModel):
    """PATCH unificado para Alumno, Secretaria y Director.

    Todos los campos son opcionales (`None` = no tocar). La `PoliticaAcceso`
    aplicable según el rol decide qué se permite tocar:

      - Alumno (sólo PENDIENTE):     motivo, asignatura_matriculada_id + estado→ANULADA
      - Secretaria (sólo PENDIENTE): motivo, asignatura_matriculada_id + estado→ANULADA
      - Director:                    observaciones + estado→EN_REVISION|APROBADA|RECHAZADA
    """

    model_config = ConfigDict(extra="ignore")

    estado: EstadoSolicitud | None = None
    motivo: str | None = None
    asignatura_matriculada_id: int | None = None
    observaciones: str | None = None


class ExportarDispensasFiltros(BaseModel):
    """Filtros opcionales del export CSV.

    Como query params en el endpoint — `BaseModel` sólo documenta el contrato.
    """

    estado: EstadoSolicitud | None = None
    alumno_id: int | None = None
    desde: datetime | None = None
    hasta: datetime | None = None
