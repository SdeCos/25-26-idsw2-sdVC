from enum import Enum

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.asignatura_grado import asignatura_grados
from app.models.grado import Grado


class CaracterAsignatura(str, Enum):
    OB = "OB"  # Obligatoria
    OP = "OP"  # Optativa
    FB = "FB"  # Formación Básica


class Asignatura(Base):
    __tablename__ = "asignaturas"

    id: Mapped[int] = mapped_column(primary_key=True)
    codigo: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    nombre: Mapped[str] = mapped_column(String(150))
    ects: Mapped[float] = mapped_column(Float)
    caracter: Mapped[str] = mapped_column(String(2))
    curso_plan: Mapped[int] = mapped_column(Integer)
    responsable_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id"), nullable=True, index=True
    )

    # Cardinalidad 1 → N: una asignatura puede pertenecer a varios grados
    # (caso canónico: Inglés impartido a ADE + INF + Org. Industrial). En el
    # caso común la lista tiene un solo elemento. `lazy="joined"` mantiene el
    # patrón de carga eager que tenía `grado` singular antes del refactor.
    grados: Mapped[list[Grado]] = relationship(
        Grado,
        secondary=asignatura_grados,
        lazy="joined",
    )
