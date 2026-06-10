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
        """Importa matrículas. El grado de cada matrícula se deriva de las
        asignaturas matriculadas: todas deben pertenecer al mismo grado o se
        rechaza el header.
        """
        resultado = await self.validador.validar(archivos)

        headers_creados = 0
        detalles_creados = 0
        errores_out = [
            ErrorImportacionOut(
                archivo=e.archivo, fila=e.fila, mensaje=e.mensaje
            )
            for e in resultado.errores
        ]

        # Pre-pasada: agrupar por (alumno, curso) y verificar coherencia de
        # grado entre todas las asignaturas del header.
        from collections import defaultdict
        agrupados: dict[tuple[int, str], list] = defaultdict(list)
        for r in resultado.validos:
            agrupados[(r.alumno_id, r.curso_academico)].append(r)

        # Lookup batched: ids únicos de asignaturas → grado_id.
        asig_ids = {r.asignatura_id for r in resultado.validos}
        grados_por_asig: dict[int, int] = {}
        if asig_ids:
            for aid in asig_ids:
                asig = await self.asignatura_repo.obtener_por_id(aid)
                if asig is not None:
                    grados_por_asig[aid] = asig.grado_id

        headers_cache: dict[tuple[int, str], int] = {}

        for clave, registros in agrupados.items():
            grados_distintos = {
                grados_por_asig.get(r.asignatura_id) for r in registros
            }
            grados_distintos.discard(None)
            if len(grados_distintos) != 1:
                errores_out.append(
                    ErrorImportacionOut(
                        archivo="(lote)",
                        fila=0,
                        mensaje=(
                            f"matrícula con asignaturas de grados distintos "
                            f"(alumno_id={clave[0]}, curso={clave[1]}): "
                            f"{sorted(grados_distintos)}"
                        ),
                    )
                )
                continue
            grado_id = next(iter(grados_distintos))

            header, was_created = await self.matricula_repo.get_or_create_header(
                alumno_id=clave[0],
                curso_academico=clave[1],
                responsable_id=responsable_id,
                grado_id=grado_id,
            )
            if was_created:
                headers_creados += 1
            headers_cache[clave] = header.id

            for registro in registros:
                am = await self.matricula_repo.crear_detalle(
                    matricula_id=header.id,
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
                                f"(alumno_id={clave[0]}, "
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
