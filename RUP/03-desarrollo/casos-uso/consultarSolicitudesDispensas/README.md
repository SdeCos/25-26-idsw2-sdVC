# CGU > consultarSolicitudesDispensas > Desarrollo

> | [🏠️](/README.md) | [Desarrollo](/RUP/03-desarrollo/README.md) | [Análisis](/RUP/01-analisis/casos-uso/consultarSolicitudesDispensas/README.md) | [Diseño](/RUP/02-diseño/casos-uso/consultarSolicitudesDispensas/README.md) | **Desarrollo** |
> |-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Construcción
- **Disciplina**: Desarrollo
- **Caso de uso**: `consultarSolicitudesDispensas()`
- **Actor**: DirectorDeGrado
- **Versión**: 1.0
- **Fecha**: 2026-05-30

## trazabilidad código ↔ diseño

| Participante del diseño | Implementación |
|---|---|
| DispensasPage (`/dispensas`) | [src/frontend/src/pages/DispensasPage.tsx](/src/frontend/src/pages/DispensasPage.tsx) |
| ConsultarDispensaPage (`/dispensas/{id}`) | [src/frontend/src/pages/ConsultarDispensaPage.tsx](/src/frontend/src/pages/ConsultarDispensaPage.tsx) |
| dispensasService.listar + obtener | [src/frontend/src/services/dispensasService.ts](/src/frontend/src/services/dispensasService.ts) |
| Tipos (`SolicitudDispensa`, `EstadoSolicitud`) | [src/frontend/src/types/dispensas.ts](/src/frontend/src/types/dispensas.ts) |
| Gate `RequireAuth roles={['director']}` | [src/frontend/src/App.tsx](/src/frontend/src/App.tsx) (helper `directorOnly`) |
| Layout link "Dispensas" (solo Director) | [src/frontend/src/components/Layout.tsx](/src/frontend/src/components/Layout.tsx) |
| DispensasRouter (`GET /dispensas`, `GET /dispensas/{id}`) | [src/backend/app/routers/dispensas.py](/src/backend/app/routers/dispensas.py) |
| SolicitudDispensaRepository.obtener_todas + obtener_por_id | [src/backend/app/repositories/solicitud_dispensa_repository.py](/src/backend/app/repositories/solicitud_dispensa_repository.py) |
| Modelo `SolicitudDispensa` con FKs `alumno_id`/`responsable_id` y relación `lazy="joined"` | [src/backend/app/models/solicitud_dispensa.py](/src/backend/app/models/solicitud_dispensa.py) |
| Schemas `SolicitudDispensaOut` + `AlumnoMinOut` + `ResponsableMinOut` | [src/backend/app/schemas/dispensas.py](/src/backend/app/schemas/dispensas.py) |
| Seed con 3 dispensas en estados distintos | [src/backend/scripts/seed.py](/src/backend/scripts/seed.py) (`_seed_dispensas`) |

## verificación end-to-end

Validado vía `curl` contra `localhost:8000`:

| Escenario | Resultado |
|---|---|
| `GET /dispensas` sin token | 401 |
| `GET /dispensas` con token Alumno | 403 |
| `GET /dispensas` con token Admin | 403 (no es director) |
| `GET /dispensas` con token Director | 200 + lista de 3 solicitudes con alumno embebido |
| `GET /dispensas/1` | 200 + `SolicitudDispensaOut` con `alumno.nombre`/`apellidos`, `responsable: null` (PENDIENTE) |
| `GET /dispensas/9999` | 404 |
| Proxy `/api/dispensas` desde Vite | 200, 3 solicitudes |

## referencias

- [Análisis](/RUP/01-analisis/casos-uso/consultarSolicitudesDispensas/README.md)
- [Diseño](/RUP/02-diseño/casos-uso/consultarSolicitudesDispensas/README.md)
- [conversation-log.md](/conversation-log.md)
