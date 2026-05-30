from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.usuario import Usuario


class EstadoSolicitud(str, Enum):
    """State machine de SolicitudDispensa.

    Transiciones legales:
      PENDIENTE   → EN_REVISION   (Director)
      PENDIENTE   → ANULADA       (Alumno propietario — ramillete futuro)
      EN_REVISION → APROBADA      (Director)
      EN_REVISION → RECHAZADA     (Director)

    Terminales: APROBADA, RECHAZADA, ANULADA.
    """

    PENDIENTE = "pendiente"
    EN_REVISION = "en_revision"
    APROBADA = "aprobada"
    RECHAZADA = "rechazada"
    ANULADA = "anulada"


ESTADOS_TERMINALES = {
    EstadoSolicitud.APROBADA,
    EstadoSolicitud.RECHAZADA,
    EstadoSolicitud.ANULADA,
}


class SolicitudDispensa(Base):
    __tablename__ = "solicitudes_dispensa"

    id: Mapped[int] = mapped_column(primary_key=True)
    alumno_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), index=True)
    asignatura: Mapped[str] = mapped_column(String(100))
    periodo: Mapped[str] = mapped_column(String(50))
    horario: Mapped[str] = mapped_column(String(100))
    motivo: Mapped[str | None] = mapped_column(String(500), nullable=True)
    estado: Mapped[str] = mapped_column(
        String(20), default=EstadoSolicitud.PENDIENTE.value, index=True
    )
    observaciones: Mapped[str | None] = mapped_column(String(500), nullable=True)
    fecha_solicitud: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    fecha_resolucion: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    responsable_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id"), nullable=True
    )

    alumno: Mapped[Usuario] = relationship(
        Usuario, foreign_keys=[alumno_id], lazy="joined"
    )
    responsable: Mapped[Usuario | None] = relationship(
        Usuario, foreign_keys=[responsable_id], lazy="joined"
    )
