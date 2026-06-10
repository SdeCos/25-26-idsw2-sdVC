from datetime import date

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sesion_clase import EstadoSesionClase, SesionDeClase
from app.schemas.sesiones_clase import CrearSesionClaseRequest


class SesionClaseRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def crear(
        self, *, profesor_id: int, datos: CrearSesionClaseRequest
    ) -> SesionDeClase:
        sesion = SesionDeClase(
            profesor_id=profesor_id,
            asignatura_id=datos.asignatura_id,
            grupos=datos.grupos,
            aula=datos.aula,
            fecha=datos.fecha,
            hora_inicio=datos.hora_inicio,
            hora_fin=datos.hora_fin,
            tema=datos.tema,
            estado=EstadoSesionClase.ABIERTA.value,
        )
        self.session.add(sesion)
        await self.session.commit()
        await self.session.refresh(sesion)
        return sesion

    async def obtener_por_id(self, id: int) -> SesionDeClase | None:
        return await self.session.get(SesionDeClase, id)

    async def listar_por_profesor(
        self,
        profesor_id: int,
        *,
        estado: EstadoSesionClase | None = None,
    ) -> list[SesionDeClase]:
        condiciones = [SesionDeClase.profesor_id == profesor_id]
        if estado is not None:
            condiciones.append(SesionDeClase.estado == estado.value)
        stmt = (
            select(SesionDeClase)
            .where(and_(*condiciones))
            .order_by(SesionDeClase.fecha.desc(), SesionDeClase.hora_inicio.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.unique().scalars().all())

    async def listar_por_asignatura_y_rango(
        self,
        asignatura_id: int,
        desde: date | None,
        hasta: date | None,
    ) -> list[SesionDeClase]:
        condiciones = [SesionDeClase.asignatura_id == asignatura_id]
        if desde is not None:
            condiciones.append(SesionDeClase.fecha >= desde)
        if hasta is not None:
            condiciones.append(SesionDeClase.fecha <= hasta)
        stmt = (
            select(SesionDeClase)
            .where(and_(*condiciones))
            .order_by(SesionDeClase.fecha, SesionDeClase.hora_inicio)
        )
        result = await self.session.execute(stmt)
        return list(result.unique().scalars().all())

    async def grupos_distintos(
        self, profesor_id: int, asignatura_id: int
    ) -> list[str]:
        """Grupos distintos que el profesor ha usado en esa asignatura.

        `grupos` es una lista JSON por fila — aplano en Python (escala
        pequeña, queries específicas a JSON_EACH añadirían acoplamiento al
        dialecto sin retorno aquí).
        """
        stmt = (
            select(SesionDeClase.grupos)
            .where(
                SesionDeClase.profesor_id == profesor_id,
                SesionDeClase.asignatura_id == asignatura_id,
            )
        )
        result = await self.session.execute(stmt)
        vistos: set[str] = set()
        for (lista,) in result.all():
            for g in lista or []:
                vistos.add(g)
        return sorted(vistos)

    async def actualizar(
        self, sesion: SesionDeClase, cambios: dict
    ) -> SesionDeClase:
        for campo, valor in cambios.items():
            setattr(sesion, campo, valor)
        await self.session.commit()
        await self.session.refresh(sesion)
        return sesion
