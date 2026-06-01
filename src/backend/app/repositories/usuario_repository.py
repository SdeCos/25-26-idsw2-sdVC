from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

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
