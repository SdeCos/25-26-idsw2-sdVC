# CGU > crearSolicitudDispensa (Alumno) > Desarrollo

> | [🏠️](/README.md) | [Desarrollo](/RUP/03-desarrollo/README.md) | [Análisis](/RUP/01-analisis/casos-uso/crearSolicitudDispensa/README.md) | [Diseño](/RUP/02-diseño/casos-uso/crearSolicitudDispensa/README.md) | **Desarrollo** |
> |-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Construcción
- **Disciplina**: Desarrollo
- **Caso de uso**: `crearSolicitudDispensa()` (Alumno)
- **Actor**: Alumno
- **Versión**: 1.0
- **Fecha**: 2026-05-30

## trazabilidad código ↔ diseño

| Participante del diseño | Implementación |
|---|---|
| CrearSolicitudPage (`/dispensas/nuevo`) | [src/frontend/src/pages/CrearSolicitudPage.tsx](/src/frontend/src/pages/CrearSolicitudPage.tsx) |
| dispensasService.crear | [src/frontend/src/services/dispensasService.ts](/src/frontend/src/services/dispensasService.ts) |
| Gate `RequireAuth roles={['alumno']}` | [src/frontend/src/App.tsx](/src/frontend/src/App.tsx) (helper `alumnoOnly`) |
| DispensasRouter (`POST /dispensas`) | [src/backend/app/routers/dispensas.py](/src/backend/app/routers/dispensas.py) |
| SolicitudDispensaService.crear | [src/backend/app/services/solicitud_dispensa_service.py](/src/backend/app/services/solicitud_dispensa_service.py) |
| SolicitudDispensaRepository.crear | [src/backend/app/repositories/solicitud_dispensa_repository.py](/src/backend/app/repositories/solicitud_dispensa_repository.py) |
| Schema `CrearSolicitudRequest` (sin `alumno_id`) | [src/backend/app/schemas/dispensas.py](/src/backend/app/schemas/dispensas.py) |

## verificación end-to-end

Validado vía `curl` contra `localhost:8000`:

| Escenario | Resultado |
|---|---|
| `POST /dispensas` con Director | 403 (solo Alumno crea) |
| `POST /dispensas` con Alumno + datos válidos | 201 + `SolicitudDispensaOut` con `alumno_id=alumno1` (auto desde sesión), `estado=pendiente`, `fecha_solicitud=now` |

## referencias

- [Análisis](/RUP/01-analisis/casos-uso/crearSolicitudDispensa/README.md)
- [Diseño](/RUP/02-diseño/casos-uso/crearSolicitudDispensa/README.md)
- [conversation-log.md](/conversation-log.md)
