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
        """Importa matrículas. El grado de cada matrícula se deriva como la
        intersección de los grados de sus asignaturas (post-M5 una asignatura
        puede pertenecer a varios grados). Reglas:
        - Intersección vacía → grados incompatibles, header rechazado.
        - Intersección con 1 grado → ese es el grado de la matrícula.
        - Intersección con 2+ grados → ambigua, header rechazado.
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

        # Pre-pasada: agrupar por (alumno, curso) para resolver el grado de
        # cada matrícula a partir de la intersección de grados de sus
        # asignaturas.
        from collections import defaultdict
        agrupados: dict[tuple[int, str], list] = defaultdict(list)
        for r in resultado.validos:
            agrupados[(r.alumno_id, r.curso_academico)].append(r)

        # Lookup batched: id de asignatura → set de grado_ids.
        asig_ids = {r.asignatura_id for r in resultado.validos}
        grados_por_asig: dict[int, set[int]] = {}
        if asig_ids:
            for aid in asig_ids:
                asig = await self.asignatura_repo.obtener_por_id(aid)
                if asig is not None:
                    grados_por_asig[aid] = {g.id for g in asig.grados}

        headers_cache: dict[tuple[int, str], int] = {}

        for clave, registros in agrupados.items():
            sets_grados = [
                grados_por_asig[r.asignatura_id]
                for r in registros
                if r.asignatura_id in grados_por_asig
            ]
            if not sets_grados:
                continue
            interseccion = set.intersection(*sets_grados)
            if not interseccion:
                errores_out.append(
                    ErrorImportacionOut(
                        archivo="(lote)",
                        fila=0,
                        mensaje=(
                            f"matrícula con asignaturas de grados "
                            f"incompatibles (alumno_id={clave[0]}, "
                            f"curso={clave[1]})"
                        ),
                    )
                )
                continue
            if len(interseccion) > 1:
                errores_out.append(
                    ErrorImportacionOut(
                        archivo="(lote)",
                        fila=0,
                        mensaje=(
                            f"matrícula ambigua — las asignaturas comparten "
                            f"varios grados {sorted(interseccion)}; añade "
                            f"alguna asignatura específica de un grado para "
                            f"desambiguar (alumno_id={clave[0]}, "
                            f"curso={clave[1]})"
                        ),
                    )
                )
                continue
            grado_id = next(iter(interseccion))

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
