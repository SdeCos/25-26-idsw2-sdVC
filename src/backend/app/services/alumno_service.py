"""Orquestador de operaciones sobre Alumno con lógica propia (importación)."""

from __future__ import annotations

from app.core.security import hash_password
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.paginacion import (
    ErrorImportacionOut,
    InformeImportacionAlumnosOut,
)
from app.services.validador_archivo_listas_alumnos import (
    ValidadorArchivoListasAlumnos,
)


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
