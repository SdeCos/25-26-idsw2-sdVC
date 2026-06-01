# CGU > importarMatriculas > Desarrollo

> | [🏠️](/README.md) | [Desarrollo](/RUP/03-desarrollo/README.md) | [Análisis](/RUP/01-analisis/casos-uso/importarMatriculas/README.md) | [Diseño](/RUP/02-diseño/casos-uso/importarMatriculas/README.md) | **Desarrollo** |
> |-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Construcción
- **Disciplina**: Desarrollo
- **Caso de uso**: `importarMatriculas()`
- **Actor**: Secretaria
- **Versión**: 1.1 (refactor a Matricula agregado)
- **Fecha**: 2026-06-01

## trazabilidad código ↔ diseño

| Participante del diseño | Implementación |
|---|---|
| ImportarMatriculasPage (`/matriculas/importar`) | [src/frontend/src/pages/ImportarMatriculasPage.tsx](/src/frontend/src/pages/ImportarMatriculasPage.tsx) |
| matriculasService.importar | [src/frontend/src/services/matriculasService.ts](/src/frontend/src/services/matriculasService.ts) |
| MatriculasRouter (`POST /matriculas/importar`) | [src/backend/app/routers/matriculas.py](/src/backend/app/routers/matriculas.py) |
| MatriculaService.importar | [src/backend/app/services/matricula_service.py](/src/backend/app/services/matricula_service.py) |
| ValidadorArchivoMatriculas (FK lookup) | [src/backend/app/services/validador_archivo_matriculas.py](/src/backend/app/services/validador_archivo_matriculas.py) |
| AsignaturaRepository.obtener_por_codigos | [src/backend/app/repositories/asignatura_repository.py](/src/backend/app/repositories/asignatura_repository.py) |
| MatriculaRepository.get_or_create_header / crear_detalle | [src/backend/app/repositories/matricula_repository.py](/src/backend/app/repositories/matricula_repository.py) |
| Modelos `Matricula` + `AsignaturaMatriculada` | [src/backend/app/models/matricula.py](/src/backend/app/models/matricula.py) |
| Modelo `Asignatura` (catálogo) | [src/backend/app/models/asignatura.py](/src/backend/app/models/asignatura.py) |
| Schema `InformeImportacionMatriculasOut` | [src/backend/app/schemas/paginacion.py](/src/backend/app/schemas/paginacion.py) |
| Seed de Asignaturas + Matrícula de alumno1 | [src/backend/scripts/seed.py](/src/backend/scripts/seed.py) |

## verificación end-to-end

Validado con CSV de 5 filas (3 válidas + 1 alumno inexistente + 1 asignatura inexistente):

| Escenario | Resultado |
|---|---|
| `POST /matriculas/importar` con token Secretaria + CSV | 200 `{matriculas_creadas: 2, asignaturas_matriculadas_creadas: 3, errores: [{fila: 5, mensaje: "alumno desconocido: 'fantasma'"}, {fila: 6, mensaje: "asignatura desconocida: 'XYZ'"}]}` |
| Re-importar el mismo CSV | Detalles existentes detectados como `IntegrityError` (UNIQUE matricula_id+asignatura_id) → reportados como "asignatura ya matriculada" |

## decisiones materializadas

- **Validador resuelve FKs en batch** (`obtener_alumnos_por_usernames` + `obtener_por_codigos`), evitando N+1 lookups.
- **`get_or_create_header`** cachea por `(alumno_id, curso_academico)` durante el lote — un solo header se reutiliza para todas las asignaturas del mismo alumno.
- **Política FK estricta** materializada como filas al informe; no creación implícita de alumno.
- **`responsable_id`** se persiste por coherencia con `SolicitudDispensa` (memoria `feedback-auditoria-coherente-por-entidad`).

## referencias

- [Análisis](/RUP/01-analisis/casos-uso/importarMatriculas/README.md)
- [Diseño](/RUP/02-diseño/casos-uso/importarMatriculas/README.md)
- [conversation-log.md](/conversation-log.md)
