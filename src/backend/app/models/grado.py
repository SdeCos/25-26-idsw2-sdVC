"""Grado — entidad de dominio del SDR restaurada post-base.

Modela un grado universitario (Ingeniería Informática, ADE, etc.). Referenciada
por `Asignatura`, `Matricula`, `DirectorDeGrado` y `SecretariaAcademica`. El
catálogo se gestiona vía CU `gestionarCatalogoGrados`.
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Grado(Base):
    __tablename__ = "grados"

    id: Mapped[int] = mapped_column(primary_key=True)
    codigo: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    nombre: Mapped[str] = mapped_column(String(150))
    facultad: Mapped[str] = mapped_column(String(150))
