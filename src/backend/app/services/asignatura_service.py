from sqlalchemy.exc import IntegrityError

from app.models.asignatura import Asignatura
from app.models.grado import Grado
from app.repositories.asignatura_repository import AsignaturaRepository
from app.repositories.grado_repository import GradoRepository
from app.schemas.asignaturas import (
    CrearAsignaturaRequest,
    EditarAsignaturaRequest,
)


class CodigoEnUso(Exception):
    pass


class AsignaturaNoEncontrada(Exception):
    pass


class GradoNoEncontrado(Exception):
    pass


class AsignaturaConReferencias(Exception):
    def __init__(self, refs: dict[str, int]) -> None:
        super().__init__(f"asignatura con referencias: {refs}")
        self.refs = refs


class AsignaturaService:
    """Reglas de negocio sobre el catálogo de asignaturas.

    Pre-valida cada `grado_id` consultando `grados` (vs. capturar el
    `IntegrityError` por FK, que en SQLite produce mensajes opacos). Para la
    unicidad de `codigo` sí confiamos en el `UNIQUE` de BD + captura → 409.
    """

    def __init__(
        self,
        repo: AsignaturaRepository,
        grado_repo: GradoRepository,
    ) -> None:
        self.repo = repo
        self.grado_repo = grado_repo

    async def listar(self) -> list[Asignatura]:
        return await self.repo.obtener_todas()

    async def obtener(self, id: int) -> Asignatura:
        a = await self.repo.obtener_por_id(id)
        if a is None:
            raise AsignaturaNoEncontrada(id)
        return a

    async def _resolver_grados(self, grado_ids: list[int]) -> list[Grado]:
        """Resuelve la lista de Grado validando cada id. Aborta con
        `GradoNoEncontrado` al primer id inexistente."""
        # Deduplicar manteniendo orden de entrada (UX: si el cliente envía
        # duplicados, el resultado no infla la N:M).
        vistos: set[int] = set()
        ids_unicos: list[int] = []
        for gid in grado_ids:
            if gid not in vistos:
                vistos.add(gid)
                ids_unicos.append(gid)
        grados: list[Grado] = []
        for gid in ids_unicos:
            g = await self.grado_repo.obtener_por_id(gid)
            if g is None:
                raise GradoNoEncontrado(gid)
            grados.append(g)
        return grados

    async def crear(
        self, datos: CrearAsignaturaRequest, responsable_id: int
    ) -> Asignatura:
        grados = await self._resolver_grados(datos.grado_ids)
        try:
            return await self.repo.crear(
                codigo=datos.codigo,
                nombre=datos.nombre,
                ects=datos.ects,
                caracter=datos.caracter,
                curso_plan=datos.curso_plan,
                grados=grados,
                responsable_id=responsable_id,
            )
        except IntegrityError as exc:
            await self.repo.session.rollback()
            raise CodigoEnUso(datos.codigo) from exc

    async def actualizar(
        self, id: int, datos: EditarAsignaturaRequest
    ) -> Asignatura:
        asignatura = await self.obtener(id)
        cambios = datos.model_dump(exclude_unset=True)
        if "grado_ids" in cambios and cambios["grado_ids"] is not None:
            cambios["grados"] = await self._resolver_grados(cambios.pop("grado_ids"))
        else:
            cambios.pop("grado_ids", None)
        if not cambios:
            return asignatura
        return await self.repo.actualizar(asignatura, cambios)

    async def eliminar(self, id: int) -> None:
        asignatura = await self.obtener(id)
        refs = await self.repo.referencias(id)
        if refs:
            raise AsignaturaConReferencias(refs)
        await self.repo.eliminar(asignatura)
