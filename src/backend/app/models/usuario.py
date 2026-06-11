from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.asignatura import Asignatura
from app.models.grado import Grado
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

    # Solo significa algo para DirectorDeGrado y SecretariaAcademica. STI: la
    # columna vive en `usuarios` y queda NULL para los demás subtipos.
    grado_id: Mapped[int | None] = mapped_column(
        ForeignKey("grados.id"), nullable=True, index=True
    )
    grado: Mapped[Grado | None] = relationship(Grado, lazy="joined")

    # Relación N:M con asignaturas. Solo significa algo para Profesor/Director
    # (jerarquía); los demás tipos la tienen vacía. Lectura `viewonly=True` para
    # que las escrituras pasen obligatoriamente por `UsuarioRepository` y se
    # pueda registrar el `responsable_id` de auditoría en `AsignaturaImpartida`
    # — un `usuario.asignaturas_impartidas.append(asignatura)` se saltaría esa
    # auditoría, así que el camino queda deshabilitado.
    #
    # `primaryjoin`/`secondaryjoin` explícitos porque `profesor_asignaturas`
    # tiene dos FKs a `usuarios` (profesor_id + responsable_id de auditoría) y
    # SQLAlchemy no puede inferir cuál usar.
    asignaturas_impartidas: Mapped[list[Asignatura]] = relationship(
        Asignatura,
        secondary=profesor_asignaturas,
        primaryjoin="Usuario.id == profesor_asignaturas.c.profesor_id",
        secondaryjoin="Asignatura.id == profesor_asignaturas.c.asignatura_id",
        viewonly=True,
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
