"""SesionDeClase — una clase concreta de un profesor en una asignatura.

State machine:  ABIERTA → CERRADA  (irreversible en v1.0).
"""

from datetime import date, datetime, time
from enum import Enum

from sqlalchemy import JSON, Date, DateTime, ForeignKey, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.asignatura import Asignatura
from app.models.usuario import Usuario


class EstadoSesionClase(str, Enum):
    ABIERTA = "abierta"
    CERRADA = "cerrada"


class SesionDeClase(Base):
    __tablename__ = "sesiones_clase"

    id: Mapped[int] = mapped_column(primary_key=True)
    profesor_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), index=True)
    asignatura_id: Mapped[int] = mapped_column(
        ForeignKey("asignaturas.id"), index=True
    )
    # Una sesión puede servir a varios grupos a la vez (p.ej. Inglés con tres
    # titulaciones en el mismo aula). Lista de etiquetas libres serializada
    # como JSON; no es entidad porque no tiene identidad ni atributos propios.
    grupos: Mapped[list[str]] = mapped_column(JSON, default=list)
    aula: Mapped[str] = mapped_column(String(50))
    fecha: Mapped[date] = mapped_column(Date, index=True)
    hora_inicio: Mapped[time] = mapped_column(Time)
    hora_fin: Mapped[time] = mapped_column(Time)
    tema: Mapped[str] = mapped_column(String(200))
    estado: Mapped[str] = mapped_column(
        String(20), default=EstadoSesionClase.ABIERTA.value, index=True
    )
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    profesor: Mapped[Usuario] = relationship(
        Usuario, foreign_keys=[profesor_id], lazy="joined"
    )
    asignatura: Mapped[Asignatura] = relationship(Asignatura, lazy="joined")
