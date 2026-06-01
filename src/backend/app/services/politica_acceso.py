"""Polimorfismo del Controller de SolicitudDispensa por rol del usuario.

Introducido en el ramillete Alumno tras tener dos casos concretos (Director y
Alumno) con políticas opuestas sobre la misma entidad. Materializa la decisión
abierta del análisis ("strategy `PoliticaAcceso`") sin tocar el orquestador.

Cuatro políticas vivas: Alumno, Secretaria, Director. (Profesor llegará en
su ramillete; hoy levanta ValueError.)
"""

from abc import ABC, abstractmethod
from datetime import datetime, timezone

from app.models.solicitud_dispensa import (
    ESTADOS_TERMINALES,
    EstadoSolicitud,
    SolicitudDispensa,
)
from app.models.usuario import Usuario
from app.repositories.solicitud_dispensa_repository import (
    SolicitudDispensaRepository,
)


class PoliticaAcceso(ABC):
    """Contrato común de las políticas. Cada subclase encapsula la regla de un rol."""

    @abstractmethod
    async def obtener_listado(
        self,
        repo: SolicitudDispensaRepository,
        usuario: Usuario,
        alumno_id_filtro: int | None = None,
    ) -> list[SolicitudDispensa]: ...

    @abstractmethod
    def puede_ver(self, solicitud: SolicitudDispensa, usuario: Usuario) -> bool: ...

    @abstractmethod
    def transiciones_permitidas(self) -> frozenset[tuple[EstadoSolicitud, EstadoSolicitud]]: ...

    @abstractmethod
    def campos_editables(self, solicitud: SolicitudDispensa) -> frozenset[str]: ...

    @abstractmethod
    def side_effects(
        self,
        solicitud: SolicitudDispensa,
        nuevo_estado: EstadoSolicitud,
        usuario: Usuario,
    ) -> dict: ...


class PoliticaAlumno(PoliticaAcceso):
    """El Alumno solo ve y modifica sus propias solicitudes en estado PENDIENTE."""

    _TRANSICIONES = frozenset(
        {(EstadoSolicitud.PENDIENTE, EstadoSolicitud.ANULADA)}
    )
    _CAMPOS_EN_PENDIENTE = frozenset({"motivo", "asignatura_matriculada_id"})

    async def obtener_listado(self, repo, usuario, alumno_id_filtro=None):
        return await repo.obtener_por_alumno(usuario.id)

    def puede_ver(self, solicitud, usuario):
        return solicitud.alumno_id == usuario.id

    def transiciones_permitidas(self):
        return self._TRANSICIONES

    def campos_editables(self, solicitud):
        if EstadoSolicitud(solicitud.estado) != EstadoSolicitud.PENDIENTE:
            return frozenset()
        return self._CAMPOS_EN_PENDIENTE

    def side_effects(self, solicitud, nuevo_estado, usuario):
        return {}


class PoliticaSecretaria(PoliticaAcceso):
    """La Secretaria es operadora global — sin filtro de propiedad.

    Misma capacidad de edición que el Alumno (modificar campos básicos cuando
    está PENDIENTE; cancelar) pero sobre cualquier solicitud, no solo las
    propias. No emite veredicto (eso es del Director).
    """

    _TRANSICIONES = frozenset(
        {(EstadoSolicitud.PENDIENTE, EstadoSolicitud.ANULADA)}
    )
    _CAMPOS_EN_PENDIENTE = frozenset({"motivo", "asignatura_matriculada_id"})

    async def obtener_listado(self, repo, usuario, alumno_id_filtro=None):
        if alumno_id_filtro is not None:
            return await repo.obtener_por_alumno(alumno_id_filtro)
        return await repo.obtener_todas()

    def puede_ver(self, solicitud, usuario):
        return True

    def transiciones_permitidas(self):
        return self._TRANSICIONES

    def campos_editables(self, solicitud):
        if EstadoSolicitud(solicitud.estado) != EstadoSolicitud.PENDIENTE:
            return frozenset()
        return self._CAMPOS_EN_PENDIENTE

    def side_effects(self, solicitud, nuevo_estado, usuario):
        return {}


class PoliticaDirector(PoliticaAcceso):
    """El Director ve y resuelve cualquier solicitud."""

    _TRANSICIONES = frozenset(
        {
            (EstadoSolicitud.PENDIENTE, EstadoSolicitud.EN_REVISION),
            (EstadoSolicitud.EN_REVISION, EstadoSolicitud.APROBADA),
            (EstadoSolicitud.EN_REVISION, EstadoSolicitud.RECHAZADA),
        }
    )
    _CAMPOS_EN_REVISION = frozenset({"observaciones"})

    async def obtener_listado(self, repo, usuario, alumno_id_filtro=None):
        if alumno_id_filtro is not None:
            return await repo.obtener_por_alumno(alumno_id_filtro)
        return await repo.obtener_todas()

    def puede_ver(self, solicitud, usuario):
        return True

    def transiciones_permitidas(self):
        return self._TRANSICIONES

    def campos_editables(self, solicitud):
        if EstadoSolicitud(solicitud.estado) == EstadoSolicitud.EN_REVISION:
            return self._CAMPOS_EN_REVISION
        return frozenset()

    def side_effects(self, solicitud, nuevo_estado, usuario):
        cambios: dict = {}
        if nuevo_estado is EstadoSolicitud.EN_REVISION:
            cambios["responsable_id"] = usuario.id
        if nuevo_estado in ESTADOS_TERMINALES:
            cambios["fecha_resolucion"] = datetime.now(timezone.utc)
        return cambios


def politica_para(usuario: Usuario) -> PoliticaAcceso:
    """Factory — devuelve la política aplicable al rol del usuario."""
    if usuario.tipo == "alumno":
        return PoliticaAlumno()
    if usuario.tipo == "secretaria":
        return PoliticaSecretaria()
    if usuario.tipo == "director":
        return PoliticaDirector()
    raise ValueError(f"No hay PoliticaAcceso para el rol {usuario.tipo!r}")
