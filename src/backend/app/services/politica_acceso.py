"""Polimorfismo del Controller de SolicitudDispensa por rol del usuario.

Introducido en el ramillete Alumno tras tener dos casos concretos (Director y
Alumno) con políticas opuestas sobre la misma entidad. Materializa la decisión
abierta del análisis ("strategy `PoliticaAcceso`") sin tocar el orquestador.

Cuatro políticas vivas: Alumno, Secretaria, Director, Profesor.
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


def _grado_de_solicitud(solicitud: SolicitudDispensa) -> int | None:
    """Lee `grado_id` por la cadena dispensa → asignatura_matriculada → asignatura."""
    am = solicitud.asignatura_matriculada
    if am is None or am.asignatura is None:
        return None
    return am.asignatura.grado_id


class PoliticaSecretaria(PoliticaAcceso):
    """Secretaría es un departamento colectivo — cualquier cuenta de tipo
    secretaria opera sobre todos los grados. Misma capacidad de edición que
    el Alumno (cancelar una pendiente) pero sobre cualquier solicitud. No
    emite veredicto (eso es del Director, que sí está scopeado por grado).
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
    """El Director ve y resuelve las dispensas de su grado."""

    _TRANSICIONES = frozenset(
        {
            (EstadoSolicitud.PENDIENTE, EstadoSolicitud.EN_REVISION),
            (EstadoSolicitud.EN_REVISION, EstadoSolicitud.APROBADA),
            (EstadoSolicitud.EN_REVISION, EstadoSolicitud.RECHAZADA),
        }
    )
    _CAMPOS_EN_REVISION = frozenset({"observaciones"})

    async def obtener_listado(self, repo, usuario, alumno_id_filtro=None):
        if usuario.grado_id is None:
            return []
        if alumno_id_filtro is not None:
            por_alumno = await repo.obtener_por_alumno(alumno_id_filtro)
            return [s for s in por_alumno if _grado_de_solicitud(s) == usuario.grado_id]
        return await repo.obtener_por_grado(usuario.grado_id)

    def puede_ver(self, solicitud, usuario):
        if usuario.grado_id is None:
            return False
        return _grado_de_solicitud(solicitud) == usuario.grado_id

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


class PoliticaProfesor(PoliticaAcceso):
    """El Profesor ve las dispensas de las asignaturas que imparte. Read-only.

    No participa en el flujo de modificación (ni transiciones ni campos
    editables). El filtro por asignaturas impartidas se aplica en
    `obtener_listado` y en `puede_ver` cruzando con la relación
    `usuario.asignaturas_impartidas` (tabla N:M `profesor_asignaturas`).
    """

    async def obtener_listado(self, repo, usuario, alumno_id_filtro=None):
        ids = {a.id for a in usuario.asignaturas_impartidas}
        if not ids:
            return []
        return await repo.obtener_por_asignaturas(ids)

    def puede_ver(self, solicitud, usuario):
        am = solicitud.asignatura_matriculada
        if am is None or am.asignatura is None:
            return False
        return am.asignatura.id in {a.id for a in usuario.asignaturas_impartidas}

    def transiciones_permitidas(self):
        return frozenset()

    def campos_editables(self, solicitud):
        return frozenset()

    def side_effects(self, solicitud, nuevo_estado, usuario):
        return {}


def politica_para(usuario: Usuario) -> PoliticaAcceso:
    """Factory — devuelve la política aplicable al rol del usuario."""
    if usuario.tipo == "alumno":
        return PoliticaAlumno()
    if usuario.tipo == "secretaria":
        return PoliticaSecretaria()
    if usuario.tipo == "director":
        return PoliticaDirector()
    if usuario.tipo == "profesor":
        return PoliticaProfesor()
    raise ValueError(f"No hay PoliticaAcceso para el rol {usuario.tipo!r}")
