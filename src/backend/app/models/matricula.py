from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.asignatura import Asignatura
from app.models.usuario import Usuario


class Matricula(Base):
    """Header del agregado Matrícula.

    Una matrícula = (alumno, curso académico). Agrupa las asignaturas que el
    alumno cursa en ese año académico. `facultad` y `plan_estudios` se derivan
    en la API tomándolos de las asignaturas matriculadas (decisión de diseño).
    """

    __tablename__ = "matriculas"
    __table_args__ = (
        UniqueConstraint("alumno_id", "curso_academico", name="uq_alumno_curso"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    alumno_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), index=True)
    curso_academico: Mapped[str] = mapped_column(String(20))
    responsable_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    fecha_importacion: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    alumno: Mapped[Usuario] = relationship(
        Usuario, foreign_keys=[alumno_id], lazy="joined"
    )
    responsable: Mapped[Usuario] = relationship(
        Usuario, foreign_keys=[responsable_id], lazy="joined"
    )
    asignaturas_matriculadas: Mapped[list["AsignaturaMatriculada"]] = relationship(
        "AsignaturaMatriculada",
        back_populates="matricula",
        lazy="selectin",
        cascade="all, delete-orphan",
    )


class AsignaturaMatriculada(Base):
    """Detalle del agregado Matrícula — una fila por asignatura cursada.

    `n_matricula` indica la convocatoria (1=primera, 2=segunda, ...).
    """

    __tablename__ = "asignaturas_matriculadas"
    __table_args__ = (
        UniqueConstraint(
            "matricula_id", "asignatura_id", name="uq_matricula_asignatura"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    matricula_id: Mapped[int] = mapped_column(
        ForeignKey("matriculas.id", ondelete="CASCADE"), index=True
    )
    asignatura_id: Mapped[int] = mapped_column(ForeignKey("asignaturas.id"))
    n_matricula: Mapped[int] = mapped_column(Integer, default=1)

    matricula: Mapped[Matricula] = relationship(
        Matricula, back_populates="asignaturas_matriculadas", lazy="joined"
    )
    asignatura: Mapped[Asignatura] = relationship(Asignatura, lazy="joined")
