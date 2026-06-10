# CGU > crearSesionClase > Desarrollo

> | [🏠️](/README.md) | [Desarrollo](/RUP/03-desarrollo/README.md) | [Análisis](/RUP/01-analisis/casos-uso/crearSesionClase/README.md) | [Diseño](/RUP/02-diseño/casos-uso/crearSesionClase/README.md) | **Desarrollo** |
> |-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Construcción
- **Disciplina**: Desarrollo
- **Caso de uso**: `crearSesionClase()`
- **Actor**: Profesor
- **Versión**: 1.0
- **Fecha**: 2026-06-02

## trazabilidad código ↔ diseño

| Participante del diseño | Implementación |
|---|---|
| CrearSesionClasePage (`/sesiones-clase/nuevo`) | [src/frontend/src/pages/CrearSesionClasePage.tsx](/src/frontend/src/pages/CrearSesionClasePage.tsx) |
| sesionesClaseService.crear | [src/frontend/src/services/sesionesClaseService.ts](/src/frontend/src/services/sesionesClaseService.ts) |
| profesoresService.misAsignaturas (carga del select) | [src/frontend/src/services/profesoresService.ts](/src/frontend/src/services/profesoresService.ts) |
| SesionesClaseRouter (`POST /sesiones-clase`) | [src/backend/app/routers/sesiones_clase.py](/src/backend/app/routers/sesiones_clase.py) |
| `require_rol(["profesor"])` | [src/backend/app/dependencies.py](/src/backend/app/dependencies.py) |
| SesionClaseService.crear (`profesor_id` desde sesión, valida horas) | [src/backend/app/services/sesion_clase_service.py](/src/backend/app/services/sesion_clase_service.py) |
| SesionClaseRepository.crear | [src/backend/app/repositories/sesion_clase_repository.py](/src/backend/app/repositories/sesion_clase_repository.py) |
| Modelo `SesionDeClase` + enum `EstadoSesionClase` | [src/backend/app/models/sesion_clase.py](/src/backend/app/models/sesion_clase.py) |
| Schemas `CrearSesionClaseRequest`, `SesionDeClaseOut` | [src/backend/app/schemas/sesiones_clase.py](/src/backend/app/schemas/sesiones_clase.py) |

## verificación end-to-end

| Escenario | Resultado |
|---|---|
| `POST /sesiones-clase` Profesor con datos válidos | 201 + estado `abierta` + profesor embebido |
| Cliente envía `profesor_id` en el body | Descartado por `extra="ignore"` — el Service usa `current_user.id` |
| `hora_fin <= hora_inicio` | 422 `SesionClaseInvalida` |
| Alumno intenta crear | 403 (require_rol) |
| Frontend: select de asignatura cargado vía `/profesores/yo/asignaturas` | 3 asignaturas (seed: IYA038, IYA040, IYA041) |

## decisiones materializadas

- **`profesor_id` auto-poblado desde la sesión** — patrón consolidado del proyecto.
- **`DatosSesionClase` del análisis → `CrearSesionClaseRequest` Pydantic** — Parameter Object como schema, sin dataclass interno adicional.
- **Estado inicial `ABIERTA`** — primera entrada del proyecto a la state machine `{ABIERTA, CERRADA}`.
- **Navegación tras 201 → `/sesiones-clase/{id}`** (vista activa con toma de asistencia).

## referencias

- [Análisis](/RUP/01-analisis/casos-uso/crearSesionClase/README.md)
- [Diseño](/RUP/02-diseño/casos-uso/crearSesionClase/README.md)
- [conversation-log.md](/conversation-log.md)
