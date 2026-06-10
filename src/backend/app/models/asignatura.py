from enum import Enum

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
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
    grado_id: Mapped[int] = mapped_column(ForeignKey("grados.id"), index=True)

    grado: Mapped[Grado] = relationship(Grado, lazy="joined")
