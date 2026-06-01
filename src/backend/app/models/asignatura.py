from enum import Enum

from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


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
    plan_estudios: Mapped[str] = mapped_column(String(150))
    facultad: Mapped[str] = mapped_column(String(150))
