# CGU > crearSolicitudDispensa (Secretaria) > Desarrollo

> | [🏠️](/README.md) | [Desarrollo](/RUP/03-desarrollo/README.md) | [Análisis](/RUP/01-analisis/casos-uso/crearSolicitudDispensaSecretaria/README.md) | [Diseño](/RUP/02-diseño/casos-uso/crearSolicitudDispensaSecretaria/README.md) | **Desarrollo** |
> |-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Construcción
- **Disciplina**: Desarrollo
- **Caso de uso**: `crearSolicitudDispensa()` (Secretaria)
- **Actor**: Secretaria
- **Versión**: 1.0
- **Fecha**: 2026-06-01

## trazabilidad código ↔ diseño

| Participante del diseño | Implementación |
|---|---|
| CrearSolicitudDispensaSecretariaPage (`/dispensas/nuevo-en-nombre-de`) | [src/frontend/src/pages/CrearSolicitudDispensaSecretariaPage.tsx](/src/frontend/src/pages/CrearSolicitudDispensaSecretariaPage.tsx) |
| dispensasService.crear (extendido) | [src/frontend/src/services/dispensasService.ts](/src/frontend/src/services/dispensasService.ts) |
| alumnosService.asignaturasMatriculadas (selector cascada) | [src/frontend/src/services/alumnosService.ts](/src/frontend/src/services/alumnosService.ts) |
| DispensasRouter (`POST /dispensas` con `require_rol(["alumno","secretaria"])`) | [src/backend/app/routers/dispensas.py](/src/backend/app/routers/dispensas.py) |
| SolicitudDispensaService.crear (dispatch por rol) | [src/backend/app/services/solicitud_dispensa_service.py](/src/backend/app/services/solicitud_dispensa_service.py) |
| PoliticaSecretaria (debut) | [src/backend/app/services/politica_acceso.py](/src/backend/app/services/politica_acceso.py) |
| Migración FK `asignatura_matriculada_id` en SolicitudDispensa | [src/backend/app/models/solicitud_dispensa.py](/src/backend/app/models/solicitud_dispensa.py), [src/backend/app/schemas/dispensas.py](/src/backend/app/schemas/dispensas.py) |
| Schema `CrearSolicitudRequest` con `alumno_id` opcional | [src/backend/app/schemas/dispensas.py](/src/backend/app/schemas/dispensas.py) |

## verificación end-to-end

| Escenario | Resultado |
|---|---|
| `POST /dispensas` Secretaria con `alumno_id` válido + AM coherente | 201 + `SolicitudDispensaOut` con alumno embebido y `estado=pendiente` |
| `POST /dispensas` Secretaria con AM que NO pertenece al alumno | 422 "La asignatura matriculada no pertenece al alumno indicado" |
| `POST /dispensas` Alumno con `alumno_id` distinto al propio | Body descartado, alumno_id resuelto desde sesión (defensa contra suplantación) |
| Frontend: buscar alumno por nombre → seleccionar → ver asignaturas matriculadas cascada → crear | 201 → navigate a ficha |

## decisiones materializadas

- **Endpoint único `POST /dispensas`** con dispatch interno por rol — no `POST /dispensas/en-nombre-de` separado.
- **Service comprueba coherencia FK** vía `_asignatura_matriculada()` con `joinedload(matricula)` antes de persistir.
- **Defensa contra suplantación**: si `current_user.tipo=="alumno"`, `alumno_id` se sobrescribe con `current_user.id` (silenciosamente).
- **`PoliticaSecretaria`** añadida a factory `politica_para` y al módulo `politica_acceso.py`.

## referencias

- [Análisis](/RUP/01-analisis/casos-uso/crearSolicitudDispensaSecretaria/README.md)
- [Diseño](/RUP/02-diseño/casos-uso/crearSolicitudDispensaSecretaria/README.md)
- [conversation-log.md](/conversation-log.md)
