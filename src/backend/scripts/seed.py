"""Crea grados, usuarios, asignaturas, matrículas y dispensas para desarrollo.

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
from app.models.grado import Grado
from app.models.matricula import AsignaturaMatriculada, Matricula
from app.models.profesor_asignatura import AsignaturaImpartida
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

# ──────────────────────────────────────────────────────────────────────────────
# Grados — entidad restaurada del SDR. Dos grados son necesarios para que las
# pruebas manuales del scoping muestren el efecto real (1 grado oculta el filtro).
# ──────────────────────────────────────────────────────────────────────────────

GRADOS_SEED: list[dict] = [
    {
        "codigo": "INF",
        "nombre": "Ingeniería Informática",
        "facultad": "Escuela Politécnica Superior",
    },
    {
        "codigo": "ADE",
        "nombre": "Administración y Dirección de Empresas",
        "facultad": "Facultad de Ciencias Económicas y Empresariales",
    },
]


ASIGNATURAS_SEED: list[dict] = [
    # INF
    {"codigo": "IYA038", "nombre": "Ingeniería de Software I", "ects": 6.0,
     "caracter": "OB", "curso_plan": 3, "grado_codigo": "INF"},
    {"codigo": "IYA040", "nombre": "Ingeniería de Software 2", "ects": 6.0,
     "caracter": "OB", "curso_plan": 3, "grado_codigo": "INF"},
    {"codigo": "IYA041", "nombre": "Diseño de Software", "ects": 6.0,
     "caracter": "OB", "curso_plan": 3, "grado_codigo": "INF"},
    {"codigo": "IYA010", "nombre": "Programación I", "ects": 6.0,
     "caracter": "FB", "curso_plan": 1, "grado_codigo": "INF"},
    {"codigo": "IYA020", "nombre": "Programación II", "ects": 6.0,
     "caracter": "OB", "curso_plan": 2, "grado_codigo": "INF"},
    # ADE
    {"codigo": "ADE101", "nombre": "Microeconomía", "ects": 6.0,
     "caracter": "FB", "curso_plan": 1, "grado_codigo": "ADE"},
    {"codigo": "ADE202", "nombre": "Contabilidad financiera", "ects": 6.0,
     "caracter": "OB", "curso_plan": 2, "grado_codigo": "ADE"},
    # Multi-grado — Inglés se imparte simultáneamente a INF + ADE
    {"codigo": "IDIO1", "nombre": "Inglés I", "ects": 3.0,
     "caracter": "FB", "curso_plan": 1, "grado_codigo": ["INF", "ADE"]},
]


async def _seed_grados(session) -> dict[str, Grado]:
    mapa: dict[str, Grado] = {}
    for datos in GRADOS_SEED:
        ya_existe = await session.scalar(
            select(Grado).where(Grado.codigo == datos["codigo"])
        )
        if ya_existe is None:
            g = Grado(**datos)
            session.add(g)
            print(f"+ grado {datos['codigo']} ({datos['nombre']})")
            mapa[datos["codigo"]] = g
        else:
            mapa[datos["codigo"]] = ya_existe
            print(f"= grado {datos['codigo']} (ya existe)")
    await session.flush()
    return mapa


def _construir_usuarios_seed(grados: dict[str, Grado]) -> list[Usuario]:
    return [
        Administrador(
            username="admin", password_hash=hash_password("admin123"),
            nombre="Admin", apellidos="CGU", email="admin@cgu.es",
        ),
        Profesor(
            username="profesor1", password_hash=hash_password("profe123"),
            nombre="Juan", apellidos="Pérez", email="juan@cgu.es",
        ),
        # Secretaría — departamento colectivo, sin grado. Una cuenta basta para
        # demo; añadir más es solo "más usuarios en el mismo rol".
        SecretariaAcademica(
            username="secretaria1", password_hash=hash_password("secre123"),
            nombre="Ana", apellidos="Gómez", email="ana@cgu.es",
        ),
        # INF — Director y alumno
        DirectorDeGrado(
            username="director1", password_hash=hash_password("director123"),
            nombre="Carlos", apellidos="Ruiz", email="carlos@cgu.es",
            grado_id=grados["INF"].id,
        ),
        Alumno(
            username="alumno1", password_hash=hash_password("alumno123"),
            nombre="María", apellidos="López", email="maria@cgu.es",
        ),
        # ADE — Director y alumno (para validar scoping del Director)
        DirectorDeGrado(
            username="director2", password_hash=hash_password("director123"),
            nombre="Elena", apellidos="Soto", email="elena@cgu.es",
            grado_id=grados["ADE"].id,
        ),
        Alumno(
            username="alumno2", password_hash=hash_password("alumno123"),
            nombre="Luis", apellidos="García", email="luis@cgu.es",
        ),
    ]


async def _seed_asignaturas(
    session, grados: dict[str, Grado]
) -> dict[str, Asignatura]:
    """Las asignaturas seed van a un grado cada una excepto IDIO1 ("Inglés"),
    que se imparte a INF + ADE simultáneamente — caso canónico multi-grado."""
    secretaria1 = await session.scalar(
        select(SecretariaAcademica).where(SecretariaAcademica.username == "secretaria1")
    )
    responsable_id = secretaria1.id if secretaria1 is not None else None
    mapa: dict[str, Asignatura] = {}
    for datos in ASIGNATURAS_SEED:
        ya_existe = await session.scalar(
            select(Asignatura).where(Asignatura.codigo == datos["codigo"])
        )
        if ya_existe is None:
            data = {k: v for k, v in datos.items() if k != "grado_codigo"}
            grados_codigos = datos["grado_codigo"]
            if isinstance(grados_codigos, str):
                grados_codigos = [grados_codigos]
            data["grados"] = [grados[c] for c in grados_codigos]
            data["responsable_id"] = responsable_id
            a = Asignatura(**data)
            session.add(a)
            etiqueta = "+".join(grados_codigos)
            print(f"+ asignatura {datos['codigo']} ({datos['nombre']}) → {etiqueta}")
            mapa[datos["codigo"]] = a
        else:
            mapa[datos["codigo"]] = ya_existe
            print(f"= asignatura {datos['codigo']} (ya existe)")
    await session.flush()
    return mapa


async def _seed_matriculas(
    session,
    asignaturas: dict[str, Asignatura],
    grados: dict[str, Grado],
) -> dict[str, AsignaturaMatriculada]:
    """Una matrícula INF para alumno1 (4 asignaturas) y otra ADE para alumno2 (2 asignaturas).
    Retorna mapa codigo_asig → AsignaturaMatriculada usado por el seed de dispensas."""
    secretaria1 = await session.scalar(
        select(SecretariaAcademica).where(SecretariaAcademica.username == "secretaria1")
    )
    alumno1 = await session.scalar(select(Alumno).where(Alumno.username == "alumno1"))
    alumno2 = await session.scalar(select(Alumno).where(Alumno.username == "alumno2"))
    if not all([secretaria1, alumno1, alumno2]):
        print("! faltan dependencias para sembrar matrículas")
        return {}

    mapa: dict[str, AsignaturaMatriculada] = {}

    async def _asegurar(alumno, secretaria, grado, codigos_asig):
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
                grado_id=grado.id,
                responsable_id=secretaria.id,
            )
            session.add(matricula)
            await session.flush()
            print(f"+ matrícula {alumno.username} 2025/2026 → {grado.codigo}")
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
        for codigo in codigos_asig:
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

    await _asegurar(alumno1, secretaria1, grados["INF"], ["IYA040", "IYA041", "IYA010", "IYA020"])
    await _asegurar(alumno2, secretaria1, grados["ADE"], ["ADE101", "ADE202"])
    return mapa


async def _seed_dispensas(
    session, asignaturas_matriculadas: dict[str, AsignaturaMatriculada]
) -> None:
    ya_hay = await session.scalar(select(SolicitudDispensa).limit(1))
    if ya_hay is not None:
        print("= dispensas (ya existen)")
        return

    alumno1 = await session.scalar(select(Alumno).where(Alumno.username == "alumno1"))
    alumno2 = await session.scalar(select(Alumno).where(Alumno.username == "alumno2"))
    director1 = await session.scalar(
        select(DirectorDeGrado).where(DirectorDeGrado.username == "director1")
    )
    if not all([alumno1, alumno2, director1, asignaturas_matriculadas]):
        print("! no se puede sembrar dispensas: faltan dependencias")
        return

    ahora = datetime.now(timezone.utc)
    dispensas = [
        # INF — alumno1
        SolicitudDispensa(
            alumno_id=alumno1.id,
            asignatura_matriculada_id=asignaturas_matriculadas["IYA040"].id,
            motivo="Solapamiento con prácticas de empresa",
            estado=EstadoSolicitud.PENDIENTE.value,
            fecha_solicitud=ahora - timedelta(days=2),
        ),
        SolicitudDispensa(
            alumno_id=alumno1.id,
            asignatura_matriculada_id=asignaturas_matriculadas["IYA041"].id,
            motivo="Compatibilización con trabajo a tiempo parcial",
            estado=EstadoSolicitud.EN_REVISION.value,
            fecha_solicitud=ahora - timedelta(days=5),
            responsable_id=director1.id,
        ),
        SolicitudDispensa(
            alumno_id=alumno1.id,
            asignatura_matriculada_id=asignaturas_matriculadas["IYA010"].id,
            motivo="Asignatura ya cursada en programa anterior",
            estado=EstadoSolicitud.APROBADA.value,
            observaciones="Reconocimiento por equivalencia de plan de estudios",
            fecha_solicitud=ahora - timedelta(days=20),
            fecha_resolucion=ahora - timedelta(days=15),
            responsable_id=director1.id,
        ),
        # ADE — alumno2 (para validar que director2/secretaria2 solo ven la suya)
        SolicitudDispensa(
            alumno_id=alumno2.id,
            asignatura_matriculada_id=asignaturas_matriculadas["ADE101"].id,
            motivo="Convalidación parcial",
            estado=EstadoSolicitud.PENDIENTE.value,
            fecha_solicitud=ahora - timedelta(days=1),
        ),
    ]
    for d in dispensas:
        session.add(d)
        codigo = next(
            (c for c, a in asignaturas_matriculadas.items() if a.id == d.asignatura_matriculada_id),
            "?",
        )
        print(f"+ dispensa {codigo} ({d.estado})")


async def _seed_profesor_asignaturas(
    session, asignaturas: dict[str, Asignatura]
) -> None:
    """Asocia profesor1 → IYA038, IYA040, IYA041 (3 asignaturas que imparte).

    Inserta filas en `AsignaturaImpartida` directamente. La `relationship`
    `Usuario.asignaturas_impartidas` es `viewonly=True` (decisión de M5: las
    escrituras deben pasar por el repositorio para registrar `responsable_id`).
    Aquí, en el seed, lo escribimos a mano replicando el patrón del repo.
    """
    profesor = await session.scalar(
        select(Profesor)
        .where(Profesor.username == "profesor1")
        .options(selectinload(Profesor.asignaturas_impartidas))
    )
    if profesor is None:
        print("! no se puede sembrar profesor_asignaturas sin profesor1")
        return

    secretaria1 = await session.scalar(
        select(SecretariaAcademica).where(SecretariaAcademica.username == "secretaria1")
    )
    responsable_id = secretaria1.id if secretaria1 is not None else None

    codigos_imparte = ["IYA038", "IYA040", "IYA041"]
    existentes = {a.codigo for a in profesor.asignaturas_impartidas}
    for codigo in codigos_imparte:
        if codigo in existentes:
            print(f"= profesor1 ya imparte {codigo}")
            continue
        session.add(
            AsignaturaImpartida(
                profesor_id=profesor.id,
                asignatura_id=asignaturas[codigo].id,
                responsable_id=responsable_id,
            )
        )
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
            grupos=["3A"],
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
            grupos=["3A"],
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
        grados = await _seed_grados(session)
        await session.commit()

        for usuario in _construir_usuarios_seed(grados):
            ya_existe = await session.scalar(
                select(Usuario).where(Usuario.username == usuario.username)
            )
            if ya_existe is None:
                session.add(usuario)
                marca_grado = f" ({usuario.grado_id})" if usuario.grado_id else ""
                print(f"+ {usuario.username} ({usuario.tipo}){marca_grado}")
            else:
                print(f"= {usuario.username} (ya existe)")
        await session.commit()

        asignaturas = await _seed_asignaturas(session, grados)
        await session.commit()

        await _seed_profesor_asignaturas(session, asignaturas)
        await session.commit()

        asignaturas_matriculadas = await _seed_matriculas(session, asignaturas, grados)
        await session.commit()

        await _seed_dispensas(session, asignaturas_matriculadas)
        await session.commit()

        await _seed_sesiones_clase(session, asignaturas)
        await session.commit()

        await _seed_asistencias_demo(session)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
