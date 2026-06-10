"""Crea usuarios, catálogo de asignaturas, matrícula y dispensas para desarrollo.

Idempotente: ejecutar varias veces no duplica.

Uso:
    python -m scripts.seed
"""

import asyncio
from datetime import date, datetime, time, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import AsyncSessionLocal, Base, engine
from app.core.security import hash_password
from app.models.asignatura import Asignatura
from app.models.asistencia import Asistencia, EstadoAsistencia
from app.models.matricula import AsignaturaMatriculada, Matricula
from app.models.sesion_clase import EstadoSesionClase, SesionDeClase
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


ASIGNATURAS_SEED: list[dict] = [
    {
        "codigo": "IYA038",
        "nombre": "Ingeniería de Software I",
        "ects": 6.0,
        "caracter": "OB",
        "curso_plan": 3,
        "plan_estudios": "Ingeniería Informática",
        "facultad": "Escuela Politécnica Superior",
    },
    {
        "codigo": "IYA040",
        "nombre": "Ingeniería de Software 2",
        "ects": 6.0,
        "caracter": "OB",
        "curso_plan": 3,
        "plan_estudios": "Ingeniería Informática",
        "facultad": "Escuela Politécnica Superior",
    },
    {
        "codigo": "IYA041",
        "nombre": "Diseño de Software",
        "ects": 6.0,
        "caracter": "OB",
        "curso_plan": 3,
        "plan_estudios": "Ingeniería Informática",
        "facultad": "Escuela Politécnica Superior",
    },
    {
        "codigo": "IYA010",
        "nombre": "Programación I",
        "ects": 6.0,
        "caracter": "FB",
        "curso_plan": 1,
        "plan_estudios": "Ingeniería Informática",
        "facultad": "Escuela Politécnica Superior",
    },
    {
        "codigo": "IYA020",
        "nombre": "Programación II",
        "ects": 6.0,
        "caracter": "OB",
        "curso_plan": 2,
        "plan_estudios": "Ingeniería Informática",
        "facultad": "Escuela Politécnica Superior",
    },
]


async def _seed_asignaturas(session) -> dict[str, Asignatura]:
    """Asegura el catálogo. Retorna el mapa código → entidad para el resto del seed."""
    mapa: dict[str, Asignatura] = {}
    for datos in ASIGNATURAS_SEED:
        ya_existe = await session.scalar(
            select(Asignatura).where(Asignatura.codigo == datos["codigo"])
        )
        if ya_existe is None:
            a = Asignatura(**datos)
            session.add(a)
            print(f"+ asignatura {datos['codigo']} ({datos['nombre']})")
            mapa[datos["codigo"]] = a
        else:
            mapa[datos["codigo"]] = ya_existe
            print(f"= asignatura {datos['codigo']} (ya existe)")
    await session.flush()
    return mapa


async def _seed_matricula_alumno1(
    session, asignaturas: dict[str, Asignatura]
) -> dict[str, AsignaturaMatriculada]:
    """Crea matrícula 2025/2026 para alumno1 con 4 asignaturas. Retorna el mapa
    código → AsignaturaMatriculada (para el seed de dispensas)."""
    alumno = await session.scalar(select(Alumno).where(Alumno.username == "alumno1"))
    secretaria = await session.scalar(
        select(SecretariaAcademica).where(SecretariaAcademica.username == "secretaria1")
    )
    if alumno is None or secretaria is None:
        print("! no se puede sembrar matrícula sin alumno1 y secretaria1")
        return {}

    matricula = await session.scalar(
        select(Matricula).where(
            Matricula.alumno_id == alumno.id,
            Matricula.curso_academico == "2025/2026",
        )
    )
    if matricula is None:
        matricula = Matricula(
            alumno_id=alumno.id,
            curso_academico="2025/2026",
            responsable_id=secretaria.id,
        )
        session.add(matricula)
        await session.flush()
        print(f"+ matrícula {alumno.username} 2025/2026")
    else:
        print(f"= matrícula {alumno.username} 2025/2026 (ya existe)")

    detalles_existentes = await session.execute(
        select(AsignaturaMatriculada).where(
            AsignaturaMatriculada.matricula_id == matricula.id
        )
    )
    existentes_por_asig = {
        am.asignatura_id: am for am in detalles_existentes.scalars().all()
    }

    mapa: dict[str, AsignaturaMatriculada] = {}
    for codigo in ["IYA040", "IYA041", "IYA010", "IYA020"]:
        asig = asignaturas[codigo]
        am = existentes_por_asig.get(asig.id)
        if am is None:
            am = AsignaturaMatriculada(
                matricula_id=matricula.id,
                asignatura_id=asig.id,
                n_matricula=1,
            )
            session.add(am)
            await session.flush()
            print(f"  + detalle matrícula {codigo}")
        else:
            print(f"  = detalle matrícula {codigo} (ya existe)")
        mapa[codigo] = am
    return mapa


async def _seed_dispensas(
    session, asignaturas_matriculadas: dict[str, AsignaturaMatriculada]
) -> None:
    ya_hay = await session.scalar(select(SolicitudDispensa).limit(1))
    if ya_hay is not None:
        print("= dispensas (ya existen)")
        return

    alumno = await session.scalar(select(Alumno).where(Alumno.username == "alumno1"))
    director = await session.scalar(
        select(DirectorDeGrado).where(DirectorDeGrado.username == "director1")
    )
    if alumno is None or director is None or not asignaturas_matriculadas:
        print("! no se puede sembrar dispensas: faltan dependencias")
        return

    ahora = datetime.now(timezone.utc)
    dispensas = [
        SolicitudDispensa(
            alumno_id=alumno.id,
            asignatura_matriculada_id=asignaturas_matriculadas["IYA040"].id,
            motivo="Solapamiento con prácticas de empresa",
            estado=EstadoSolicitud.PENDIENTE.value,
            fecha_solicitud=ahora - timedelta(days=2),
        ),
        SolicitudDispensa(
            alumno_id=alumno.id,
            asignatura_matriculada_id=asignaturas_matriculadas["IYA041"].id,
            motivo="Compatibilización con trabajo a tiempo parcial",
            estado=EstadoSolicitud.EN_REVISION.value,
            fecha_solicitud=ahora - timedelta(days=5),
            responsable_id=director.id,
        ),
        SolicitudDispensa(
            alumno_id=alumno.id,
            asignatura_matriculada_id=asignaturas_matriculadas["IYA010"].id,
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
        am = asignaturas_matriculadas
        # Reverse-lookup del codigo para el print
        codigo = next(
            (c for c, a in am.items() if a.id == d.asignatura_matriculada_id),
            "?",
        )
        print(f"+ dispensa {codigo} ({d.estado})")


async def _seed_profesor_asignaturas(
    session, asignaturas: dict[str, Asignatura]
) -> None:
    """Asocia profesor1 → IYA038, IYA040, IYA041 (3 asignaturas que imparte)."""
    profesor = await session.scalar(
        select(Profesor)
        .where(Profesor.username == "profesor1")
        .options(selectinload(Profesor.asignaturas_impartidas))
    )
    if profesor is None:
        print("! no se puede sembrar profesor_asignaturas sin profesor1")
        return

    codigos_imparte = ["IYA038", "IYA040", "IYA041"]
    existentes = {a.codigo for a in profesor.asignaturas_impartidas}
    for codigo in codigos_imparte:
        if codigo in existentes:
            print(f"= profesor1 ya imparte {codigo}")
            continue
        profesor.asignaturas_impartidas.append(asignaturas[codigo])
        print(f"+ profesor1 imparte {codigo}")


async def _seed_sesiones_clase(
    session, asignaturas: dict[str, Asignatura]
) -> None:
    """Dos sesiones de clase de profesor1: una ABIERTA hoy, una CERRADA ayer."""
    ya_hay = await session.scalar(select(SesionDeClase).limit(1))
    if ya_hay is not None:
        print("= sesiones de clase (ya existen)")
        return
    profesor = await session.scalar(
        select(Profesor).where(Profesor.username == "profesor1")
    )
    if profesor is None:
        print("! no se puede sembrar sesiones sin profesor1")
        return

    hoy = date.today()
    ayer = hoy - timedelta(days=1)
    sesiones = [
        SesionDeClase(
            profesor_id=profesor.id,
            asignatura_id=asignaturas["IYA040"].id,
            grupo="3A",
            aula="Aula 201",
            fecha=hoy,
            hora_inicio=time(10, 0),
            hora_fin=time(11, 30),
            tema="Patrones de diseño: introducción",
            estado=EstadoSesionClase.ABIERTA.value,
        ),
        SesionDeClase(
            profesor_id=profesor.id,
            asignatura_id=asignaturas["IYA040"].id,
            grupo="3A",
            aula="Aula 201",
            fecha=ayer,
            hora_inicio=time(10, 0),
            hora_fin=time(11, 30),
            tema="UML — repaso",
            estado=EstadoSesionClase.CERRADA.value,
        ),
    ]
    for s in sesiones:
        session.add(s)
        print(f"+ sesión IYA040 {s.fecha} ({s.estado})")


async def _seed_asistencias_demo(session) -> None:
    """Una asistencia de alumno1 en la sesión CERRADA de ayer (datos demo)."""
    ya_hay = await session.scalar(select(Asistencia).limit(1))
    if ya_hay is not None:
        print("= asistencias (ya existen)")
        return
    alumno = await session.scalar(
        select(Alumno).where(Alumno.username == "alumno1")
    )
    sesion = await session.scalar(
        select(SesionDeClase)
        .where(SesionDeClase.estado == EstadoSesionClase.CERRADA.value)
        .limit(1)
    )
    if alumno is None or sesion is None:
        return
    session.add(
        Asistencia(
            sesion_clase_id=sesion.id,
            alumno_id=alumno.id,
            estado=EstadoAsistencia.PRESENTE.value,
        )
    )
    print(f"+ asistencia demo alumno1 → sesión {sesion.id}")


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

        asignaturas = await _seed_asignaturas(session)
        await session.commit()

        await _seed_profesor_asignaturas(session, asignaturas)
        await session.commit()

        asignaturas_matriculadas = await _seed_matricula_alumno1(session, asignaturas)
        await session.commit()

        await _seed_dispensas(session, asignaturas_matriculadas)
        await session.commit()

        await _seed_sesiones_clase(session, asignaturas)
        await session.commit()

        await _seed_asistencias_demo(session)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
