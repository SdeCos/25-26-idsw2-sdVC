"""Crea usuarios iniciales para desarrollo.

Idempotente: ejecutar varias veces no duplica usuarios.

Uso:
    python -m scripts.seed
"""

import asyncio

from sqlalchemy import select

from app.core.database import AsyncSessionLocal, Base, engine
from app.core.security import hash_password
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


if __name__ == "__main__":
    asyncio.run(main())
