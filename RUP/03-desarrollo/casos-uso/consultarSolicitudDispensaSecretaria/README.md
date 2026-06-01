# CGU > consultarSolicitudDispensa (Secretaria) > Desarrollo

> | [🏠️](/README.md) | [Desarrollo](/RUP/03-desarrollo/README.md) | [Análisis](/RUP/01-analisis/casos-uso/consultarSolicitudDispensaSecretaria/README.md) | [Diseño](/RUP/02-diseño/casos-uso/consultarSolicitudDispensaSecretaria/README.md) | **Desarrollo** |
> |-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Construcción
- **Disciplina**: Desarrollo
- **Caso de uso**: `consultarSolicitudDispensa()` (Secretaria)
- **Actor**: Secretaria
- **Versión**: 1.0
- **Fecha**: 2026-06-01

## trazabilidad código ↔ diseño

| Participante del diseño | Implementación |
|---|---|
| ConsultarDispensaPage (reutilizada con `lectura`) | [src/frontend/src/pages/ConsultarDispensaPage.tsx](/src/frontend/src/pages/ConsultarDispensaPage.tsx) |
| DispensasPage (reutilizada — Secretaria ve todas) | [src/frontend/src/pages/DispensasPage.tsx](/src/frontend/src/pages/DispensasPage.tsx) |
| dispensasService.obtener / listar | [src/frontend/src/services/dispensasService.ts](/src/frontend/src/services/dispensasService.ts) |
| DispensasRouter (`GET /dispensas{,/{id}}` con `require_rol(["alumno","secretaria","director"])`) | [src/backend/app/routers/dispensas.py](/src/backend/app/routers/dispensas.py) |
| SolicitudDispensaService.obtener / listar | [src/backend/app/services/solicitud_dispensa_service.py](/src/backend/app/services/solicitud_dispensa_service.py) |
| PoliticaSecretaria.puede_ver=True + .obtener_listado(sin filtro) | [src/backend/app/services/politica_acceso.py](/src/backend/app/services/politica_acceso.py) |
| Schema `SolicitudDispensaOut` con `asignatura_matriculada` embed | [src/backend/app/schemas/dispensas.py](/src/backend/app/schemas/dispensas.py) |

## verificación end-to-end

| Escenario | Resultado |
|---|---|
| `GET /dispensas` Secretaria | 200 — todas las dispensas (sin filtro de propiedad) |
| `GET /dispensas?alumno_id=3` Secretaria | 200 — filtradas por alumno (parámetro opcional) |
| `GET /dispensas/{id}` Secretaria de dispensa de otro alumno | 200 (puede ver cualquier ficha) |
| `GET /dispensas/9999` | 404 |

## decisiones materializadas

- **Schema único `SolicitudDispensaOut`** para los 4 roles — UI ramifica qué muestra.
- **Filtro `?alumno_id=`** soportado por `PoliticaSecretaria.obtener_listado(alumno_id_filtro)` cuando el cliente lo envía.
- **Ficha enriquecida** con datos del alumno + asignatura + responsable embebidos vía eager-load.

## referencias

- [Análisis](/RUP/01-analisis/casos-uso/consultarSolicitudDispensaSecretaria/README.md)
- [Diseño](/RUP/02-diseño/casos-uso/consultarSolicitudDispensaSecretaria/README.md)
- [conversation-log.md](/conversation-log.md)
