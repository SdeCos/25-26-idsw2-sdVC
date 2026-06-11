from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.asignatura_grado import asignatura_grados
from app.models.grado import Grado
from app.models.matricula import Matricula
from app.models.usuario import Usuario


class GradoRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def listar(self) -> list[Grado]:
        result = await self.session.execute(select(Grado).order_by(Grado.codigo))
        return list(result.scalars().all())

    async def obtener_por_id(self, id: int) -> Grado | None:
        return await self.session.get(Grado, id)

    async def existe_codigo(self, codigo: str) -> bool:
        result = await self.session.execute(
            select(Grado.id).where(Grado.codigo == codigo)
        )
        return result.scalar() is not None

    async def crear(self, *, codigo: str, nombre: str, facultad: str) -> Grado:
        g = Grado(codigo=codigo, nombre=nombre, facultad=facultad)
        self.session.add(g)
        await self.session.commit()
        await self.session.refresh(g)
        return g

    async def actualizar(self, grado: Grado, cambios: dict) -> Grado:
        for campo, valor in cambios.items():
            setattr(grado, campo, valor)
        await self.session.commit()
        await self.session.refresh(grado)
        return grado

    async def referencias(self, grado_id: int) -> dict[str, int]:
        """Cuenta referencias por tipo. Vacío → se puede borrar."""
        refs: dict[str, int] = {}

        n_asig = await self.session.scalar(
            select(asignatura_grados.c.asignatura_id)
            .where(asignatura_grados.c.grado_id == grado_id)
            .limit(1)
        )
        if n_asig is not None:
            refs["asignaturas"] = 1

        n_mat = await self.session.scalar(
            select(Matricula.id).where(Matricula.grado_id == grado_id).limit(1)
        )
        if n_mat is not None:
            refs["matriculas"] = 1

        n_usr = await self.session.scalar(
            select(Usuario.id).where(Usuario.grado_id == grado_id).limit(1)
        )
        if n_usr is not None:
            refs["usuarios"] = 1

        return refs

    async def eliminar(self, grado: Grado) -> None:
        await self.session.delete(grado)
        await self.session.commit()
