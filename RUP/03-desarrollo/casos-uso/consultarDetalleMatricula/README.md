# CGU > consultarDetalleMatricula > Desarrollo

> | [🏠️](/README.md) | [Desarrollo](/RUP/03-desarrollo/README.md) | [Análisis](/RUP/01-analisis/casos-uso/consultarDetalleMatricula/README.md) | [Diseño](/RUP/02-diseño/casos-uso/consultarDetalleMatricula/README.md) | **Desarrollo** |
> |-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Construcción
- **Disciplina**: Desarrollo
- **Caso de uso**: `consultarDetalleMatricula()`
- **Actor**: Secretaria
- **Versión**: 1.0
- **Fecha**: 2026-06-01

## trazabilidad código ↔ diseño

| Participante del diseño | Implementación |
|---|---|
| ConsultarDetalleMatriculaPage (`/matriculas/{id}`) | [src/frontend/src/pages/ConsultarDetalleMatriculaPage.tsx](/src/frontend/src/pages/ConsultarDetalleMatriculaPage.tsx) |
| MatriculasPage (`/matriculas` lista) | [src/frontend/src/pages/MatriculasPage.tsx](/src/frontend/src/pages/MatriculasPage.tsx) |
| matriculasService.obtener / listar | [src/frontend/src/services/matriculasService.ts](/src/frontend/src/services/matriculasService.ts) |
| MatriculasRouter (`GET /matriculas/{id}` + `GET /matriculas`) | [src/backend/app/routers/matriculas.py](/src/backend/app/routers/matriculas.py) |
| MatriculaRepository.obtener_por_id (eager-load) | [src/backend/app/repositories/matricula_repository.py](/src/backend/app/repositories/matricula_repository.py) |
| Schemas `MatriculaDetalleOut` con `plan_estudios`/`facultad` derivados | [src/backend/app/schemas/matriculas.py](/src/backend/app/schemas/matriculas.py) |

## verificación end-to-end

| Escenario | Resultado |
|---|---|
| `GET /matriculas` con Secretaria | 200 — lista con 1 fila (alumno1, 4 asignaturas) |
| `GET /matriculas/1` con Secretaria | 200 con `plan_estudios`=Ingeniería Informática (derivado), `facultad` derivado, 4 `asignaturas_matriculadas` con `codigo/ects/caracter/curso_plan` |
| `GET /matriculas/9999` | 404 |

## decisiones materializadas

- **Eager load del agregado** vía `selectinload(asignaturas_matriculadas).joinedload(asignatura)` + `joinedload(alumno)` + `joinedload(responsable)` — una sola consulta devuelve la ficha completa.
- **`plan_estudios` y `facultad` derivados en el Router** desde la primera asignatura matriculada.
- **Sin Service** — `consultar` read-only va Router→Repository.

## referencias

- [Análisis](/RUP/01-analisis/casos-uso/consultarDetalleMatricula/README.md)
- [Diseño](/RUP/02-diseño/casos-uso/consultarDetalleMatricula/README.md)
- [conversation-log.md](/conversation-log.md)
