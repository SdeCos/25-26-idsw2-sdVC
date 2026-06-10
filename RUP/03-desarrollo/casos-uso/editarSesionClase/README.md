# CGU > editarSesionClase > Desarrollo

> | [🏠️](/README.md) | [Desarrollo](/RUP/03-desarrollo/README.md) | [Análisis](/RUP/01-analisis/casos-uso/editarSesionClase/README.md) | [Diseño](/RUP/02-diseño/casos-uso/editarSesionClase/README.md) | **Desarrollo** |
> |-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Construcción
- **Disciplina**: Desarrollo
- **Caso de uso**: `editarSesionClase()`
- **Actor**: Profesor
- **Versión**: 1.0
- **Fecha**: 2026-06-02

## trazabilidad código ↔ diseño

| Participante del diseño | Implementación |
|---|---|
| SesionClaseActivaPage (modo edición in-situ) | [src/frontend/src/pages/SesionClaseActivaPage.tsx](/src/frontend/src/pages/SesionClaseActivaPage.tsx) |
| Diff cliente-side + `window.confirm` al cancelar | mismo archivo, función `cancelarEdicion` |
| sesionesClaseService.actualizar (PATCH parcial) | [src/frontend/src/services/sesionesClaseService.ts](/src/frontend/src/services/sesionesClaseService.ts) |
| SesionesClaseRouter (`PATCH /sesiones-clase/{id}`) | [src/backend/app/routers/sesiones_clase.py](/src/backend/app/routers/sesiones_clase.py) |
| Defensa de propiedad + estado en Service | [src/backend/app/services/sesion_clase_service.py](/src/backend/app/services/sesion_clase_service.py) |
| Schema `EditarSesionClaseRequest` con `extra="ignore"` | [src/backend/app/schemas/sesiones_clase.py](/src/backend/app/schemas/sesiones_clase.py) |

## verificación end-to-end

| Escenario | Resultado |
|---|---|
| `PATCH /sesiones-clase/{id}` con `{tema, aula}` (ABIERTA) | 200 con los nuevos valores |
| Cliente envía `asignatura_id`/`grupo`/`profesor_id` | Descartados por `extra="ignore"` — invariantes preservadas |
| Profesor distinto al propietario | 403 `SesionClaseNoEditable` |
| Sesión `CERRADA` | 422 "sesión cerrada — no se puede editar" |
| `hora_fin <= hora_inicio` en el PATCH | 422 `SesionClaseInvalida` |
| Frontend: editar in-situ + Cancelar con cambios pide confirmación | `window.confirm` aplicado |

## decisiones materializadas

- **Edición in-situ sobre `/sesiones-clase/{id}`** — `SesionClaseActivaPage` ramifica entre modo "ver" y modo "editar" en la misma ruta.
- **`extra="ignore"` materializa las invariantes** — `asignatura_id`, `grupo`, `profesor_id` descartados antes de llegar al Service.
- **PATCH parcial con diff cliente-side** — solo se envía lo cambiado, mismo patrón que `EditarUsuarioPage` y `EditarSolicitudPage`.
- **Cancelación con `window.confirm`** si hay cambios pendientes (resuelve la deuda del análisis).

## referencias

- [Análisis](/RUP/01-analisis/casos-uso/editarSesionClase/README.md)
- [Diseño](/RUP/02-diseño/casos-uso/editarSesionClase/README.md)
- [conversation-log.md](/conversation-log.md)
