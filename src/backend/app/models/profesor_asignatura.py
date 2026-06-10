"""Tabla N:M profesor ↔ asignatura — docencia asignada.

Sin atributos propios (la asignación de docencia es binaria). El acceso desde
Python es `usuario.asignaturas_impartidas` (definido en `usuario.py`).
"""

from sqlalchemy import Column, ForeignKey, Integer, Table

from app.core.database import Base

profesor_asignaturas = Table(
    "profesor_asignaturas",
    Base.metadata,
    Column("profesor_id", Integer, ForeignKey("usuarios.id"), primary_key=True),
    Column("asignatura_id", Integer, ForeignKey("asignaturas.id"), primary_key=True),
)
