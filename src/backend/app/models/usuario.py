from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.asignatura import Asignatura
from app.models.profesor_asignatura import profesor_asignaturas


class Usuario(Base):
    """Jerarquía polimórfica de actores autenticables.

    Single-Table Inheritance: todos los subtipos comparten la tabla `usuarios`
    discriminada por la columna `tipo`. La multi-herencia del Administrador
    (Alumno + Profesor + Director + Secretaria) no se materializa como herencia
    múltiple en ORM — el rol "administrador" abarca a los demás vía política
    en el servicio.
    """

    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    tipo: Mapped[str] = mapped_column(String(20), index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    nombre: Mapped[str] = mapped_column(String(100))
    apellidos: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relación N:M con asignaturas. Solo significa algo para Profesor/Director
    # (jerarquía); los demás tipos la tienen vacía. Se define aquí para que el
    # mapper la conozca para todos los subtipos sin polimorfismo extra.
    asignaturas_impartidas: Mapped[list[Asignatura]] = relationship(
        Asignatura,
        secondary=profesor_asignaturas,
        lazy="selectin",
    )

    __mapper_args__ = {
        "polymorphic_on": "tipo",
        "polymorphic_identity": "usuario",
    }


class Alumno(Usuario):
    __mapper_args__ = {"polymorphic_identity": "alumno"}


class Profesor(Usuario):
    __mapper_args__ = {"polymorphic_identity": "profesor"}


class DirectorDeGrado(Profesor):
    __mapper_args__ = {"polymorphic_identity": "director"}


class SecretariaAcademica(Usuario):
    __mapper_args__ = {"polymorphic_identity": "secretaria"}


class Administrador(Usuario):
    __mapper_args__ = {"polymorphic_identity": "administrador"}
