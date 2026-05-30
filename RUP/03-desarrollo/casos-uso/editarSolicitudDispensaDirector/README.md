# CGU > editarSolicitudDispensa (Director) > Desarrollo

> | [🏠️](/README.md) | [Desarrollo](/RUP/03-desarrollo/README.md) | [Análisis](/RUP/01-analisis/casos-uso/editarSolicitudDispensaDirector/README.md) | [Diseño](/RUP/02-diseño/casos-uso/editarSolicitudDispensaDirector/README.md) | **Desarrollo** |
> |-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Construcción
- **Disciplina**: Desarrollo
- **Caso de uso**: `editarSolicitudDispensa()` (Director — emisión de veredicto)
- **Actor**: DirectorDeGrado
- **Versión**: 1.0
- **Fecha**: 2026-05-30

## trazabilidad código ↔ diseño

| Participante del diseño | Implementación |
|---|---|
| EmitirVeredictoPage (`/dispensas/{id}/veredicto`) | [src/frontend/src/pages/EmitirVeredictoPage.tsx](/src/frontend/src/pages/EmitirVeredictoPage.tsx) |
| dispensasService.actualizar | [src/frontend/src/services/dispensasService.ts](/src/frontend/src/services/dispensasService.ts) |
| DispensasRouter (`PATCH /dispensas/{id}`) | [src/backend/app/routers/dispensas.py](/src/backend/app/routers/dispensas.py) |
| SolicitudDispensaService.actualizar + state machine | [src/backend/app/services/solicitud_dispensa_service.py](/src/backend/app/services/solicitud_dispensa_service.py) |
| SolicitudDispensaRepository.actualizar | [src/backend/app/repositories/solicitud_dispensa_repository.py](/src/backend/app/repositories/solicitud_dispensa_repository.py) |
| Schema `EditarVeredictoRequest` + enum `EstadoSolicitud` | [src/backend/app/schemas/dispensas.py](/src/backend/app/schemas/dispensas.py) + [src/backend/app/models/solicitud_dispensa.py](/src/backend/app/models/solicitud_dispensa.py) |

## materialización de las decisiones de diseño

| Decisión del diseño | Cómo se materializa |
|---|---|
| State machine en el Service | Set `TRANSICIONES_DIRECTOR: {(PENDIENTE, EN_REVISION), (EN_REVISION, APROBADA), (EN_REVISION, RECHAZADA)}` |
| `responsable_id` se fija en `PENDIENTE → EN_REVISION` | `if nuevo is EN_REVISION: cambios["responsable_id"] = current_user.id` |
| `fecha_resolucion` se sella al alcanzar terminal | `if nuevo in ESTADOS_TERMINALES: cambios["fecha_resolucion"] = now()` |
| `observaciones` obligatorias al rechazar | `if nuevo is RECHAZADA and not datos.observaciones.strip(): raise ObservacionesRequeridas` |
| PATCH único endpoint para las 3 transiciones | El cliente envía el `estado` destino; el Service decide qué side effects aplica |
| State machine validada server-side | Cliente ramifica UX (botón correcto por estado actual), pero la BD es la autoridad: 422 si la transición no está en `TRANSICIONES_DIRECTOR` |
| EmitirVeredictoPage hace GET fresco | `useEffect` con `dispensasService.obtener(id)` al montar (mismo patrón que `EditarUsuarioPage`) |

## verificación end-to-end

Validado vía `curl` contra `localhost:8000`:

| Escenario | Resultado |
|---|---|
| `PATCH /dispensas/1` con `PENDIENTE → APROBADA` (salto inválido) | 422 `Transición pendiente → aprobada no permitida` |
| `PATCH /dispensas/1` con `PENDIENTE → EN_REVISION` | 200 + `responsable_id` fijado al Director, `fecha_resolucion: null` |
| `PATCH /dispensas/1` con `EN_REVISION → RECHAZADA` sin observaciones | 422 `Las observaciones son obligatorias al rechazar` |
| `PATCH /dispensas/2` con `EN_REVISION → APROBADA` sin observaciones | 200 + `fecha_resolucion` sellada (observaciones permitidas null al aprobar) |
| `PATCH /dispensas/3` desde terminal `APROBADA → EN_REVISION` | 422 `Transición aprobada → en_revision no permitida` |
| `PATCH /dispensas/9999` | 404 |
| `PATCH /dispensas/1` con `EN_REVISION → RECHAZADA` + observaciones | 200 + `fecha_resolucion` sellada + observaciones guardadas |

Tras las pruebas, los datos se resetearon vía `DELETE FROM solicitudes_dispensa` + `python -m scripts.seed` para dejar las 3 solicitudes en sus estados iniciales (`pendiente`, `en_revision`, `aprobada`).

## referencias

- [Análisis](/RUP/01-analisis/casos-uso/editarSolicitudDispensaDirector/README.md)
- [Diseño](/RUP/02-diseño/casos-uso/editarSolicitudDispensaDirector/README.md)
- [conversation-log.md](/conversation-log.md)
