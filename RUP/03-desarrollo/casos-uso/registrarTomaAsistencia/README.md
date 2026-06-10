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
| Re-marcar el mismo alumno con `tarde` + justificación | 200 (upsert) — misma `id`, nuevo estado |
| Sesión `CERRADA` | 422 "sesión cerrada — no se puede marcar" |
| Sesión de otro Profesor | 403 "no es tu sesión" |
| Alumno no matriculado en la asignatura | 422 `AlumnoNoMatriculado` |
| Frontend: tres botones (presente/tarde/ausente), el activo queda resaltado | comportamiento esperado |

## decisiones materializadas

- **`Asistencia` debuta como entidad** con UNIQUE `(sesion_clase_id, alumno_id)`.
- **`sqlite_insert(...).on_conflict_do_update(...)`** — upsert nativo SQLite. Si migramos a Postgres se cambia el import a `postgresql_insert`.
- **Sub-recurso `/sesiones-clase/{id}/asistencias`** — refleja la jerarquía conceptual.
- **`Asistencia ↔ SolicitudDispensa`: opción A** (independientes); el cliente cruza si lo necesita visualmente.
- **`fecha_registro` con `server_default=now()` y `onupdate=now()`** — auditoría temporal sin código adicional.

## referencias

- [Análisis](/RUP/01-analisis/casos-uso/registrarTomaAsistencia/README.md)
- [Diseño](/RUP/02-diseño/casos-uso/registrarTomaAsistencia/README.md)
- [conversation-log.md](/conversation-log.md)
