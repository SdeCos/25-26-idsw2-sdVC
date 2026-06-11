"""Tabla N:M profesor ↔ asignatura — docencia asignada.

Evolución desde el diseño M5: era un `Table` desnudo `(profesor_id, asignatura_id)`.
Tras añadir `responsable_id` (Secretaría que hizo la asignación) se reifica como
**Association Object** (idiom SQLAlchemy / Fowler). El acceso de lectura desde
Python sigue siendo `usuario.asignaturas_impartidas` (lista de `Asignatura`,
declarada `viewonly=True` en `Usuario` para que cualquier `append` no se cuele
saltándose la auditoría); las escrituras se hacen vía `UsuarioRepository`.
"""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class AsignaturaImpartida(Base):
    __tablename__ = "profesor_asignaturas"

    profesor_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"), primary_key=True
    )
    asignatura_id: Mapped[int] = mapped_column(
        ForeignKey("asignaturas.id"), primary_key=True
    )
    responsable_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id"), nullable=True, index=True
    )


# Alias retro-compatible: SQLAlchemy puede usar el `__table__` del modelo como
# `secondary` en otros `relationship`. Se mantiene el nombre antiguo para no
# romper imports en sitios donde solo se necesita la tabla.
profesor_asignaturas = AsignaturaImpartida.__table__
