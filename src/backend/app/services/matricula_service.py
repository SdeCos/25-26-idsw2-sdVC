"""Orquestador de operaciones sobre Matricula (importación masiva)."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.asignatura_repository import AsignaturaRepository
from app.repositories.matricula_repository import MatriculaRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.paginacion import (
    ErrorImportacionOut,
    InformeImportacionMatriculasOut,
)
from app.services.validador_archivo_matriculas import (
    ValidadorArchivoMatriculas,
)


class MatriculaService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.matricula_repo = MatriculaRepository(session)
        self.usuario_repo = UsuarioRepository(session)
        self.asignatura_repo = AsignaturaRepository(session)
        self.validador = ValidadorArchivoMatriculas(
            self.usuario_repo, self.asignatura_repo
        )

    async def importar(
        self,
        archivos: list[tuple[str, bytes]],
        responsable_id: int,
    ) -> InformeImportacionMatriculasOut:
        resultado = await self.validador.validar(archivos)

        headers_creados = 0
        detalles_creados = 0
        errores_out = [
            ErrorImportacionOut(
                archivo=e.archivo, fila=e.fila, mensaje=e.mensaje
            )
            for e in resultado.errores
        ]

        # Cache local de headers por (alumno_id, curso_academico) para no
        # consultar la BD por cada fila del lote.
        headers_cache: dict[tuple[int, str], int] = {}

        for registro in resultado.validos:
            clave = (registro.alumno_id, registro.curso_academico)
            matricula_id = headers_cache.get(clave)
            if matricula_id is None:
                header, was_created = await self.matricula_repo.get_or_create_header(
                    alumno_id=registro.alumno_id,
                    curso_academico=registro.curso_academico,
                    responsable_id=responsable_id,
                )
                if was_created:
                    headers_creados += 1
                headers_cache[clave] = header.id
                matricula_id = header.id

            am = await self.matricula_repo.crear_detalle(
                matricula_id=matricula_id,
                asignatura_id=registro.asignatura_id,
                n_matricula=registro.n_matricula,
            )
            if am is None:
                errores_out.append(
                    ErrorImportacionOut(
                        archivo="(lote)",
                        fila=0,
                        mensaje=(
                            "asignatura ya matriculada en este curso "
                            f"(alumno_id={registro.alumno_id}, "
                            f"asignatura_id={registro.asignatura_id})"
                        ),
                    )
                )
                continue
            detalles_creados += 1

        await self.session.commit()
        return InformeImportacionMatriculasOut(
            matriculas_creadas=headers_creados,
            asignaturas_matriculadas_creadas=detalles_creados,
            errores=errores_out,
        )
