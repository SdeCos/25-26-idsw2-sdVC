from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.matricula import AsignaturaMatriculada, Matricula
from app.models.usuario import (
    Administrador,
    Alumno,
    DirectorDeGrado,
    Profesor,
    SecretariaAcademica,
    Usuario,
)

# Mapa explícito tipo → clase concreta. SQLAlchemy hace lo mismo por debajo
# vía `polymorphic_map`, pero hacerlo explícito mantiene la decisión visible
# en código y obliga a actualizarlo al añadir un subtipo nuevo.
TIPO_A_CLASE: dict[str, type[Usuario]] = {
    "alumno": Alumno,
    "profesor": Profesor,
    "director": DirectorDeGrado,
    "secretaria": SecretariaAcademica,
    "administrador": Administrador,
}


class TipoUsuarioInvalido(Exception):
    pass


class UsuarioRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def obtener_por_username(self, username: str) -> Usuario | None:
        result = await self.session.execute(
            select(Usuario).where(Usuario.username == username)
        )
        return result.scalar_one_or_none()

    async def obtener_por_id(self, id: int) -> Usuario | None:
        return await self.session.get(Usuario, id)

    async def obtener_todos(self) -> list[Usuario]:
        result = await self.session.execute(select(Usuario).order_by(Usuario.id))
        return list(result.scalars().all())

    async def obtener_alumnos_por_usernames(
        self, usernames: list[str]
    ) -> dict[str, Alumno]:
        if not usernames:
            return {}
        result = await self.session.execute(
            select(Alumno).where(Alumno.username.in_(usernames))
        )
        return {a.username: a for a in result.scalars().all()}

    async def buscar_alumnos(
        self, page: int, size: int, q: str | None = None
    ) -> tuple[list[Alumno], int]:
        stmt = select(Alumno)
        if q:
            patron = f"%{q.lower()}%"
            stmt = stmt.where(
                or_(
                    func.lower(Alumno.username).like(patron),
                    func.lower(Alumno.nombre).like(patron),
                    func.lower(Alumno.apellidos).like(patron),
                    func.lower(Alumno.email).like(patron),
                )
            )
        total_stmt = select(func.count()).select_from(stmt.subquery())
        total = (await self.session.execute(total_stmt)).scalar_one()
        result = await self.session.execute(
            stmt.order_by(Alumno.apellidos, Alumno.nombre)
            .limit(size)
            .offset((page - 1) * size)
        )
        return list(result.scalars().all()), total

    async def buscar_por_asignatura(
        self,
        asignatura_id: int,
        page: int,
        size: int,
    ) -> tuple[list[Alumno], int]:
        """Alumnos matriculados en una asignatura concreta.

        Join con `matriculas` + `asignaturas_matriculadas`. Una fila por
        alumno (un alumno puede estar en varios cursos académicos; tomamos
        cualquiera — el listado del Profesor no distingue curso).
        """
        subq = (
            select(Matricula.alumno_id)
            .join(
                AsignaturaMatriculada,
                AsignaturaMatriculada.matricula_id == Matricula.id,
            )
            .where(AsignaturaMatriculada.asignatura_id == asignatura_id)
            .distinct()
            .subquery()
        )
        stmt = select(Alumno).where(Alumno.id.in_(select(subq.c.alumno_id)))
        total_stmt = select(func.count()).select_from(stmt.subquery())
        total = (await self.session.execute(total_stmt)).scalar_one()
        result = await self.session.execute(
            stmt.order_by(Alumno.apellidos, Alumno.nombre)
            .limit(size)
            .offset((page - 1) * size)
        )
        return list(result.scalars().all()), total

    async def obtener_alumno_con_matricula(self, alumno_id: int) -> Alumno | None:
        """Alumno con su agregado de matrículas/asignaturas-matriculadas eager-loaded.

        Necesario para (a) validar "Profesor competente" (intersección de
        asignaturas) y (b) componer la ficha del Alumno.
        """
        # Carga del propio alumno
        result = await self.session.execute(
            select(Alumno).where(Alumno.id == alumno_id)
        )
        alumno = result.scalars().first()
        if alumno is None:
            return None
        # Eager-load de las matrículas del alumno
        stmt_mat = (
            select(Matricula)
            .where(Matricula.alumno_id == alumno_id)
            .options(
                selectinload(Matricula.asignaturas_matriculadas).joinedload(
                    AsignaturaMatriculada.asignatura
                )
            )
        )
        mat_result = await self.session.execute(stmt_mat)
        alumno.matriculas_cargadas = list(mat_result.unique().scalars().all())  # type: ignore[attr-defined]
        return alumno

    async def asignaturas_impartidas_ids(self, profesor_id: int) -> set[int]:
        """Conjunto de `asignatura_id` que el Profesor imparte (relación N:M)."""
        prof = await self.session.get(Usuario, profesor_id)
        if prof is None:
            return set()
        return {a.id for a in prof.asignaturas_impartidas}

    async def crear(
        self,
        tipo: str,
        username: str,
        password_hash: str,
        nombre: str,
        apellidos: str,
        email: str,
    ) -> Usuario:
        cls = TIPO_A_CLASE.get(tipo)
        if cls is None:
            raise TipoUsuarioInvalido(tipo)
        usuario = cls(
            username=username,
            password_hash=password_hash,
            nombre=nombre,
            apellidos=apellidos,
            email=email,
        )
        self.session.add(usuario)
        await self.session.commit()
        await self.session.refresh(usuario)
        return usuario

    async def actualizar(self, usuario: Usuario, cambios: dict) -> Usuario:
        for campo, valor in cambios.items():
            setattr(usuario, campo, valor)
        await self.session.commit()
        await self.session.refresh(usuario)
        return usuario

    async def upsert_lote_alumnos(
        self, registros: list[dict]
    ) -> tuple[int, int]:
        """Upsert por `username`. No toca `password_hash` si el alumno ya existe.

        Cada `registro` es un dict con: username, password_hash, nombre,
        apellidos, email, telefono (opcional, ignorado por ahora).

        Retorna (creados, actualizados).
        """
        if not registros:
            return 0, 0

        usernames = [r["username"] for r in registros]
        existentes = await self.obtener_alumnos_por_usernames(usernames)

        creados = 0
        actualizados = 0
        for r in registros:
            existente = existentes.get(r["username"])
            if existente is None:
                self.session.add(
                    Alumno(
                        username=r["username"],
                        password_hash=r["password_hash"],
                        nombre=r["nombre"],
                        apellidos=r["apellidos"],
                        email=r["email"],
                    )
                )
                creados += 1
            else:
                existente.nombre = r["nombre"]
                existente.apellidos = r["apellidos"]
                existente.email = r["email"]
                actualizados += 1
        await self.session.commit()
        return creados, actualizados
