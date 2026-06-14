# CGU > registrarTomaAsistencia > Desarrollo

> | [🏠️](/README.md) | [Desarrollo](/RUP/03-desarrollo/README.md) | [Análisis](/RUP/01-analisis/casos-uso/registrarTomaAsistencia/README.md) | [Diseño](/RUP/02-diseño/casos-uso/registrarTomaAsistencia/README.md) | **Desarrollo** |
> |-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Construcción
- **Disciplina**: Desarrollo
- **Caso de uso**: `registrarTomaAsistencia()`
- **Actor**: Profesor
- **Versión**: 1.0
- **Fecha**: 2026-06-02

## trazabilidad código ↔ diseño

| Participante del diseño | Implementación |
|---|---|
| SesionClaseActivaPage — sección "Toma de asistencia" | [src/frontend/src/pages/SesionClaseActivaPage.tsx](/src/frontend/src/pages/SesionClaseActivaPage.tsx) función `marcar` |
| sesionesClaseService.marcarAsistencia (PUT por alumno) | [src/frontend/src/services/sesionesClaseService.ts](/src/frontend/src/services/sesionesClaseService.ts) |
| sesionesClaseService.listarAsistencias (carga inicial) | mismo archivo |
| SesionesClaseRouter (`PUT /sesiones-clase/{id}/asistencias/{alumno_id}` + `GET .../asistencias`) | [src/backend/app/routers/sesiones_clase.py](/src/backend/app/routers/sesiones_clase.py) |
| AsistenciaService.marcar (propietario + estado + matriculado) | [src/backend/app/services/asistencia_service.py](/src/backend/app/services/asistencia_service.py) |
| AsistenciaRepository.upsert (`INSERT ... ON CONFLICT DO UPDATE`) | [src/backend/app/repositories/asistencia_repository.py](/src/backend/app/repositories/asistencia_repository.py) |
| Modelo `Asistencia` + UNIQUE compuesto + enum `EstadoAsistencia` | [src/backend/app/models/asistencia.py](/src/backend/app/models/asistencia.py) |

## verificación end-to-end

| Escenario | Resultado |
|---|---|
| Profesor marca presente | 200 + `Asistencia` con `fecha_registro` |
| Re-marcar el mismo alumno con `justificado` + justificación | 200 (upsert) — misma `id`, nuevo estado |
| Sesión `CERRADA` | 422 "sesión cerrada — no se puede marcar" |
| Sesión de otro Profesor | 403 "no es tu sesión" |
| Alumno no matriculado en la asignatura | 422 `AlumnoNoMatriculado` |
| Frontend: tres botones (presente/justificado/ausente), el activo queda resaltado | comportamiento esperado |
| Frontend: sesión cerrada → tabla read-only con badge por alumno (no botones) | comportamiento esperado (fix 2026-06-14) |

## decisiones materializadas

- **`Asistencia` debuta como entidad** con UNIQUE `(sesion_clase_id, alumno_id)`.
- **`sqlite_insert(...).on_conflict_do_update(...)`** — upsert nativo SQLite. Si migramos a Postgres se cambia el import a `postgresql_insert`.
- **Sub-recurso `/sesiones-clase/{id}/asistencias`** — refleja la jerarquía conceptual.
- **`Asistencia ↔ SolicitudDispensa`: opción A** (independientes); el cliente cruza si lo necesita visualmente.
- **`fecha_registro` con `server_default=now()` y `onupdate=now()`** — auditoría temporal sin código adicional.

## evolución post-base (2026-06-14)

Dos cambios detectados en pruebas manuales pre-entrega:

1. **`EstadoAsistencia.TARDE` → `JUSTIFICADO`** — `TARDE` no contaba para el % del 70% (la cuenta del repositorio era `estado == PRESENTE`) y no representaba un concepto académico claro. `JUSTIFICADO` es ausencia documentada que **cuenta como `PRESENTE`** para el umbral. Archivos tocados: `models/asistencia.py` (enum), `repositories/asistencia_repository.py` (`estado IN (PRESENTE, JUSTIFICADO)` en el contador), `types/asistencias.ts` y `pages/SesionClaseActivaPage.tsx` (botón). Migración SQL: `UPDATE asistencias SET estado='justificado' WHERE estado='tarde'`. Decisión documentada en `02-diseño/.../README.md`.

2. **Tabla read-only tras cerrar la sesión** — antes la página solo mostraba "Sesión cerrada — no admite más cambios" y ocultaba la tabla entera; el Profesor que acababa de cerrar no veía qué había marcado. Ahora la sección se renderiza siempre, con `<h2>` distinto ("Asistencia registrada" vs "Toma de asistencia") y la columna Estado pinta `<span className="estado-badge">` en lugar de los 3 botones cuando `!abierta`. Archivo único: `pages/SesionClaseActivaPage.tsx`.

## referencias

- [Análisis](/RUP/01-analisis/casos-uso/registrarTomaAsistencia/README.md)
- [Diseño](/RUP/02-diseño/casos-uso/registrarTomaAsistencia/README.md)
- [conversation-log.md](/conversation-log.md)
