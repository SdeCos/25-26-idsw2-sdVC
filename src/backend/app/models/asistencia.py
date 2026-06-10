"""Asistencia — marca del Profesor para un alumno en una sesión de clase.

Unicidad compuesta `(sesion_clase_id, alumno_id)`: una marca por sesión y alumno.
Base del upsert idempotente (`INSERT ... ON CONFLICT DO UPDATE`).
"""

from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.sesion_clase import SesionDeClase
from app.models.usuario import Usuario


class EstadoAsistencia(str, Enum):
    PRESENTE = "presente"
    AUSENTE = "ausente"
    TARDE = "tarde"


class Asistencia(Base):
    __tablename__ = "asistencias"
    __table_args__ = (
        UniqueConstraint(
            "sesion_clase_id", "alumno_id", name="uq_sesion_alumno"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    sesion_clase_id: Mapped[int] = mapped_column(
        ForeignKey("sesiones_clase.id"), index=True
    )
    alumno_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), index=True)
    estado: Mapped[str] = mapped_column(String(20))
    justificacion: Mapped[str | None] = mapped_column(String(500), nullable=True)
    fecha_registro: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    sesion_clase: Mapped[SesionDeClase] = relationship(SesionDeClase, lazy="joined")
    alumno: Mapped[Usuario] = relationship(Usuario, lazy="joined")
