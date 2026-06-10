from sqlalchemy.exc import IntegrityError

from app.models.grado import Grado
from app.repositories.grado_repository import GradoRepository
from app.schemas.grados import CrearGradoRequest, EditarGradoRequest


class CodigoEnUso(Exception):
    pass


class GradoNoEncontrado(Exception):
    pass


class GradoConReferencias(Exception):
    def __init__(self, refs: dict[str, int]) -> None:
        super().__init__(f"grado con referencias: {refs}")
        self.refs = refs


class GradoService:
    def __init__(self, repo: GradoRepository) -> None:
        self.repo = repo

    async def listar(self) -> list[Grado]:
        return await self.repo.listar()

    async def obtener(self, id: int) -> Grado:
        g = await self.repo.obtener_por_id(id)
        if g is None:
            raise GradoNoEncontrado(id)
        return g

    async def crear(self, datos: CrearGradoRequest) -> Grado:
        try:
            return await self.repo.crear(
                codigo=datos.codigo,
                nombre=datos.nombre,
                facultad=datos.facultad,
            )
        except IntegrityError as exc:
            await self.repo.session.rollback()
            raise CodigoEnUso(datos.codigo) from exc

    async def actualizar(self, id: int, datos: EditarGradoRequest) -> Grado:
        grado = await self.obtener(id)
        cambios = datos.model_dump(exclude_unset=True)
        if not cambios:
            return grado
        return await self.repo.actualizar(grado, cambios)

    async def eliminar(self, id: int) -> None:
        grado = await self.obtener(id)
        refs = await self.repo.referencias(id)
        if refs:
            raise GradoConReferencias(refs)
        await self.repo.eliminar(grado)
