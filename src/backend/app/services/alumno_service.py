"""Orquestador de operaciones sobre Alumno.

Tres funciones:
- `importar`: validación + upsert masivo (CSV de Secretaria).
- `listar_por_asignatura`: aplica "Profesor competente" antes del listado.
- `obtener_detalle`: ficha del alumno con verificación de acceso del Profesor.
"""

from __future__ import annotations

from app.core.security import hash_password
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.paginacion import (
    ErrorImportacionOut,
    InformeImportacionAlumnosOut,
)
from app.services.validador_archivo_listas_alumnos import (
    ValidadorArchivoListasAlumnos,
)


class ProfesorNoCompetente(Exception):
    """El Profesor no imparte la asignatura solicitada."""


class AlumnoNoEncontrado(Exception):
    pass


class AsignaturaRequerida(Exception):
    """El rol Profesor exige `asignatura_id` en el listado."""


class AlumnoService:
    def __init__(self, repo: UsuarioRepository) -> None:
        self.repo = repo
        self.validador = ValidadorArchivoListasAlumnos()

    async def importar(
        self, archivos: list[tuple[str, bytes]]
    ) -> InformeImportacionAlumnosOut:
        resultado = self.validador.validar(archivos)
        if not resultado.validos:
            return InformeImportacionAlumnosOut(
                creados=0,
                actualizados=0,
                errores=[
                    ErrorImportacionOut(
                        archivo=e.archivo, fila=e.fila, mensaje=e.mensaje
                    )
                    for e in resultado.errores
                ],
            )

        registros = [
            {
                "username": r.username,
                "password_hash": hash_password(r.password),
                "nombre": r.nombre,
                "apellidos": r.apellidos,
                "email": r.email,
            }
            for r in resultado.validos
        ]
        creados, actualizados = await self.repo.upsert_lote_alumnos(registros)

        return InformeImportacionAlumnosOut(
            creados=creados,
            actualizados=actualizados,
            errores=[
                ErrorImportacionOut(
                    archivo=e.archivo, fila=e.fila, mensaje=e.mensaje
                )
                for e in resultado.errores
            ],
        )

    async def listar_por_asignatura(
        self,
        asignatura_id: int,
        page: int,
        size: int,
        usuario: Usuario,
    ) -> tuple[list, int]:
        """Lista alumnos matriculados en la asignatura.

        Defensa "Profesor competente": si el rol es Profesor, exige que la
        asignatura esté en sus impartidas.
        """
        if usuario.tipo == "profesor":
            ids = {a.id for a in usuario.asignaturas_impartidas}
            if asignatura_id not in ids:
                raise ProfesorNoCompetente
        # Secretaria: sin restricción.
        return await self.repo.buscar_por_asignatura(asignatura_id, page, size)

    async def obtener_detalle(self, alumno_id: int, usuario: Usuario):
        """Ficha del alumno con verificación 'Profesor competente'.

        Devuelve el `Alumno` con su agregado de matrículas cargado en
        `matriculas_cargadas`. Si el rol es Profesor, exige al menos una
        asignatura compartida con el alumno; 403 `ProfesorNoCompetente` si no.
        """
        alumno = await self.repo.obtener_alumno_con_matricula(alumno_id)
        if alumno is None:
            raise AlumnoNoEncontrado(alumno_id)
        if usuario.tipo == "profesor":
            impartidas = {a.id for a in usuario.asignaturas_impartidas}
            matriculadas = {
                am.asignatura_id
                for m in getattr(alumno, "matriculas_cargadas", [])
                for am in m.asignaturas_matriculadas
            }
            if not (impartidas & matriculadas):
                raise ProfesorNoCompetente
        return alumno
