# CGU > editarSolicitudDispensa (Secretaria) > Desarrollo

> | [🏠️](/README.md) | [Desarrollo](/RUP/03-desarrollo/README.md) | [Análisis](/RUP/01-analisis/casos-uso/editarSolicitudDispensaSecretaria/README.md) | [Diseño](/RUP/02-diseño/casos-uso/editarSolicitudDispensaSecretaria/README.md) | **Desarrollo** |
> |-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Construcción
- **Disciplina**: Desarrollo
- **Caso de uso**: `editarSolicitudDispensa()` (Secretaria)
- **Actor**: Secretaria
- **Versión**: 1.0
- **Fecha**: 2026-06-01

## trazabilidad código ↔ diseño

| Participante del diseño | Implementación |
|---|---|
| EditarSolicitudPage (reutilizada con `alumnoOSecretaria`) | [src/frontend/src/pages/EditarSolicitudPage.tsx](/src/frontend/src/pages/EditarSolicitudPage.tsx) |
| dispensasService.actualizar (con diff cliente-side) | [src/frontend/src/services/dispensasService.ts](/src/frontend/src/services/dispensasService.ts) |
| DispensasRouter (`PATCH /dispensas/{id}` con `require_rol(["alumno","secretaria","director"])`) | [src/backend/app/routers/dispensas.py](/src/backend/app/routers/dispensas.py) |
| SolicitudDispensaService.actualizar | [src/backend/app/services/solicitud_dispensa_service.py](/src/backend/app/services/solicitud_dispensa_service.py) |
| PoliticaSecretaria.transiciones_permitidas + .campos_editables | [src/backend/app/services/politica_acceso.py](/src/backend/app/services/politica_acceso.py) |
| Schema `EditarSolicitudRequest` con `asignatura_matriculada_id` opcional | [src/backend/app/schemas/dispensas.py](/src/backend/app/schemas/dispensas.py) |

## verificación end-to-end

| Escenario | Resultado |
|---|---|
| `PATCH /dispensas/{id}` Secretaria cambia motivo en PENDIENTE | 200 |
| Secretaria cancela `{estado:"anulada"}` en PENDIENTE | 200, transición legal |
| Secretaria intenta emitir veredicto `{estado:"aprobada"}` | 422 TransicionNoValida (eso es del Director) |
| Secretaria intenta `{observaciones:"..."}` (campo del Director) | 422 CampoNoEditable |
| Secretaria edita en EN_REVISION | 422 CampoNoEditable (campos editables vacíos) |

## decisiones materializadas

- **Misma signatura que `editar` Alumno** — la Strategy `PoliticaSecretaria` decide qué se permite. Coherente con la regla emergente del análisis: "métodos por rol solo cuando la signatura difiere".
- **Frontend reutiliza `EditarSolicitudPage`** sin cambios — la página ya consulta la solicitud y aplica diff; el back rechaza lo no permitido por política.
- **Botón "Editar" condicional** en `ConsultarDispensaPage` para Secretaria igual que para Alumno.

## referencias

- [Análisis](/RUP/01-analisis/casos-uso/editarSolicitudDispensaSecretaria/README.md)
- [Diseño](/RUP/02-diseño/casos-uso/editarSolicitudDispensaSecretaria/README.md)
- [conversation-log.md](/conversation-log.md)
