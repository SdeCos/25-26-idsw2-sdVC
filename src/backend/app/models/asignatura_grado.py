"""Tabla N:M asignatura ↔ grado.

Una asignatura puede pertenecer a varios grados (caso canónico: "Inglés" que se
imparte a ADE + INF + Org. Industrial simultáneamente). En el caso común la
lista tiene un solo elemento y el coste es despreciable; soportar el caso
multi-grado evita duplicar la asignatura por grado.

Sin atributos propios — no hay metadata por par. Si en el futuro hiciera falta
(por ejemplo "carácter distinto según el grado"), se reificaría como
Association Object (mismo movimiento que `AsignaturaImpartida`).
"""

from sqlalchemy import Column, ForeignKey, Integer, Table

from app.core.database import Base

asignatura_grados = Table(
    "asignatura_grados",
    Base.metadata,
    Column(
        "asignatura_id", Integer, ForeignKey("asignaturas.id"), primary_key=True
    ),
    Column("grado_id", Integer, ForeignKey("grados.id"), primary_key=True),
)
