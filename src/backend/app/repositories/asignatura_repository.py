from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.asignatura import Asignatura
from app.models.grado import Grado
from app.models.matricula import AsignaturaMatriculada
from app.models.sesion_clase import SesionDeClase
from app.models.solicitud_dispensa import SolicitudDispensa
from app.models.profesor_asignatura import profesor_asignaturas


class AsignaturaRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def obtener_por_codigos(
        self, codigos: list[str]
    ) -> dict[str, Asignatura]:
        if not codigos:
            return {}
        result = await self.session.execute(
            select(Asignatura).where(Asignatura.codigo.in_(codigos))
        )
        # `.unique()` por el `lazy="joined"` en `Asignatura.grados`: códigos
        # multi-grado producirían filas duplicadas (mismo bug que
        # `usuario_repository.obtener_impartidas`).
        return {a.codigo: a for a in result.scalars().unique().all()}

    async def obtener_todas(self) -> list[Asignatura]:
        result = await self.session.execute(
            select(Asignatura).order_by(Asignatura.codigo)
        )
        return list(result.scalars().unique().all())

    async def obtener_por_id(self, id: int) -> Asignatura | None:
        return await self.session.get(Asignatura, id)

    async def crear(
        self,
        *,
        codigo: str,
        nombre: str,
        ects: float,
        caracter: str,
        curso_plan: int,
        grados: list[Grado],
        responsable_id: int | None,
    ) -> Asignatura:
        a = Asignatura(
            codigo=codigo,
            nombre=nombre,
            ects=ects,
            caracter=caracter,
            curso_plan=curso_plan,
            responsable_id=responsable_id,
            grados=list(grados),
        )
        self.session.add(a)
        await self.session.commit()
        await self.session.refresh(a)
        return a

    async def actualizar(self, asignatura: Asignatura, cambios: dict) -> Asignatura:
        # `grados` puede venir en `cambios` (lista de Grado ya resueltos por el
        # service). Se asigna como reemplazo entero — SQLAlchemy gestiona el
        # diff en la N:M `asignatura_grados`.
        for campo, valor in cambios.items():
            setattr(asignatura, campo, valor)
        await self.session.commit()
        await self.session.refresh(asignatura)
        return asignatura

    async def referencias(self, asignatura_id: int) -> dict[str, int]:
        """Cuenta referencias por tipo. Vacío → se puede borrar."""
        refs: dict[str, int] = {}

        n_am = await self.session.scalar(
            select(AsignaturaMatriculada.id)
            .where(AsignaturaMatriculada.asignatura_id == asignatura_id)
            .limit(1)
        )
        if n_am is not None:
            refs["matriculas"] = 1

        n_sc = await self.session.scalar(
            select(SesionDeClase.id)
            .where(SesionDeClase.asignatura_id == asignatura_id)
            .limit(1)
        )
        if n_sc is not None:
            refs["sesiones_clase"] = 1

        n_sd = await self.session.scalar(
            select(SolicitudDispensa.id)
            .where(SolicitudDispensa.asignatura_matriculada_id.in_(
                select(AsignaturaMatriculada.id).where(
                    AsignaturaMatriculada.asignatura_id == asignatura_id
                )
            ))
            .limit(1)
        )
        if n_sd is not None:
            refs["dispensas"] = 1

        n_pa = await self.session.scalar(
            select(profesor_asignaturas.c.profesor_id)
            .where(profesor_asignaturas.c.asignatura_id == asignatura_id)
            .limit(1)
        )
        if n_pa is not None:
            refs["profesores_que_imparten"] = 1

        return refs

    async def eliminar(self, asignatura: Asignatura) -> None:
        await self.session.delete(asignatura)
        await self.session.commit()
