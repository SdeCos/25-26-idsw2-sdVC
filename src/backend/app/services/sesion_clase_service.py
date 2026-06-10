from datetime import time

from app.models.sesion_clase import EstadoSesionClase, SesionDeClase
from app.models.usuario import Usuario
from app.repositories.sesion_clase_repository import SesionClaseRepository
from app.schemas.sesiones_clase import (
    CrearSesionClaseRequest,
    EditarSesionClaseRequest,
)


class SesionClaseNoEncontrada(Exception):
    pass


class SesionClaseInvalida(Exception):
    """Datos de creación/edición inválidos (p.ej. hora_fin <= hora_inicio)."""


class SesionClaseNoEditable(Exception):
    """No se puede editar/cerrar — no propietario, estado != ABIERTA, transición ilegal."""


class SesionClaseService:
    def __init__(self, repo: SesionClaseRepository) -> None:
        self.repo = repo

    @staticmethod
    def _validar_horas(hi: time, hf: time) -> None:
        if hf <= hi:
            raise SesionClaseInvalida("hora_fin debe ser posterior a hora_inicio")

    async def crear(
        self, datos: CrearSesionClaseRequest, usuario: Usuario
    ) -> SesionDeClase:
        self._validar_horas(datos.hora_inicio, datos.hora_fin)
        return await self.repo.crear(profesor_id=usuario.id, datos=datos)

    async def listar(self, usuario: Usuario) -> list[SesionDeClase]:
        return await self.repo.listar_por_profesor(usuario.id)

    async def obtener(self, id: int, usuario: Usuario) -> SesionDeClase:
        sesion = await self.repo.obtener_por_id(id)
        if sesion is None:
            raise SesionClaseNoEncontrada(id)
        if sesion.profesor_id != usuario.id:
            raise SesionClaseNoEditable("no es tu sesión")
        return sesion

    async def actualizar(
        self,
        id: int,
        datos: EditarSesionClaseRequest,
        usuario: Usuario,
    ) -> SesionDeClase:
        sesion = await self.repo.obtener_por_id(id)
        if sesion is None:
            raise SesionClaseNoEncontrada(id)
        if sesion.profesor_id != usuario.id:
            raise SesionClaseNoEditable("no es tu sesión")

        enviados = datos.model_dump(exclude_unset=True)
        cambios: dict = {}

        # Transición de estado (única transición legal: ABIERTA → CERRADA)
        nuevo_estado = enviados.pop("estado", None)
        if nuevo_estado is not None:
            actual = EstadoSesionClase(sesion.estado)
            nueva = nuevo_estado
            if not (actual is EstadoSesionClase.ABIERTA and nueva is EstadoSesionClase.CERRADA):
                raise SesionClaseNoEditable(
                    f"transición {actual.value} → {nueva.value} no permitida"
                )
            cambios["estado"] = nueva.value

        # Resto de campos editables: solo si la sesión está ABIERTA
        if enviados:
            if EstadoSesionClase(sesion.estado) is EstadoSesionClase.CERRADA:
                raise SesionClaseNoEditable("sesión cerrada — no se puede editar")
            # Si el body cambia ambas horas, valida con los nuevos valores.
            nuevo_hi = enviados.get("hora_inicio", sesion.hora_inicio)
            nuevo_hf = enviados.get("hora_fin", sesion.hora_fin)
            if "estado" not in cambios:
                self._validar_horas(nuevo_hi, nuevo_hf)
            for campo, valor in enviados.items():
                cambios[campo] = valor

        if not cambios:
            return sesion
        return await self.repo.actualizar(sesion, cambios)
