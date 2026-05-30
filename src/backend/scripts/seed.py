"""Crea usuarios iniciales y solicitudes de dispensa para desarrollo.

Idempotente: ejecutar varias veces no duplica.

Uso:
    python -m scripts.seed
"""

import asyncio
from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from app.core.database import AsyncSessionLocal, Base, engine
from app.core.security import hash_password
from app.models.solicitud_dispensa import EstadoSolicitud, SolicitudDispensa
from app.models.usuario import (
    Administrador,
    Alumno,
    DirectorDeGrado,
    Profesor,
    SecretariaAcademica,
    Usuario,
)

USUARIOS_SEED: list[Usuario] = [
    Administrador(
        username="admin",
        password_hash=hash_password("admin123"),
        nombre="Admin",
        apellidos="CGU",
        email="admin@cgu.es",
    ),
    Profesor(
        username="profesor1",
        password_hash=hash_password("profe123"),
        nombre="Juan",
        apellidos="Pérez",
        email="juan@cgu.es",
    ),
    Alumno(
        username="alumno1",
        password_hash=hash_password("alumno123"),
        nombre="María",
        apellidos="López",
        email="maria@cgu.es",
    ),
    DirectorDeGrado(
        username="director1",
        password_hash=hash_password("director123"),
        nombre="Carlos",
        apellidos="Ruiz",
        email="carlos@cgu.es",
    ),
    SecretariaAcademica(
        username="secretaria1",
        password_hash=hash_password("secre123"),
        nombre="Ana",
        apellidos="Gómez",
        email="ana@cgu.es",
    ),
]


async def _seed_dispensas(session) -> None:
    """Crea 3 solicitudes en estados distintos atribuidas a alumno1.

    Idempotente: si ya hay dispensas en la BD, no hace nada.
    """
    ya_hay = await session.scalar(select(SolicitudDispensa).limit(1))
    if ya_hay is not None:
        print("= dispensas (ya existen)")
        return

    alumno = await session.scalar(select(Alumno).where(Alumno.username == "alumno1"))
    director = await session.scalar(
        select(DirectorDeGrado).where(DirectorDeGrado.username == "director1")
    )
    if alumno is None or director is None:
        print("! no se puede sembrar dispensas sin alumno1 y director1")
        return

    ahora = datetime.now(timezone.utc)

    dispensas = [
        SolicitudDispensa(
            alumno_id=alumno.id,
            asignatura="Ingeniería de Software 2",
            periodo="2026-Q2",
            horario="Lunes 10:00-12:00",
            motivo="Solapamiento con prácticas de empresa",
            estado=EstadoSolicitud.PENDIENTE.value,
            fecha_solicitud=ahora - timedelta(days=2),
        ),
        SolicitudDispensa(
            alumno_id=alumno.id,
            asignatura="Diseño de Software",
            periodo="2026-Q1",
            horario="Martes 14:00-16:00",
            motivo="Compatibilización con trabajo a tiempo parcial",
            estado=EstadoSolicitud.EN_REVISION.value,
            fecha_solicitud=ahora - timedelta(days=5),
            responsable_id=director.id,
        ),
        SolicitudDispensa(
            alumno_id=alumno.id,
            asignatura="Programación I",
            periodo="2026-Q1",
            horario="Miércoles 09:00-11:00",
            motivo="Asignatura ya cursada en programa anterior",
            estado=EstadoSolicitud.APROBADA.value,
            observaciones="Reconocimiento por equivalencia de plan de estudios",
            fecha_solicitud=ahora - timedelta(days=20),
            fecha_resolucion=ahora - timedelta(days=15),
            responsable_id=director.id,
        ),
    ]

    for d in dispensas:
        session.add(d)
        print(f"+ dispensa {d.asignatura} ({d.estado})")


async def main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        for usuario in USUARIOS_SEED:
            ya_existe = await session.scalar(
                select(Usuario).where(Usuario.username == usuario.username)
            )
            if ya_existe is None:
                session.add(usuario)
                print(f"+ {usuario.username} ({usuario.tipo})")
            else:
                print(f"= {usuario.username} (ya existe)")
        await session.commit()

        await _seed_dispensas(session)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
