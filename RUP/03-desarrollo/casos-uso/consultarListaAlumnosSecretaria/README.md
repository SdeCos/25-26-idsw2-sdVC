# CGU > consultarListaAlumnos (Secretaria) > Desarrollo

> | [🏠️](/README.md) | [Desarrollo](/RUP/03-desarrollo/README.md) | [Análisis](/RUP/01-analisis/casos-uso/consultarListaAlumnosSecretaria/README.md) | [Diseño](/RUP/02-diseño/casos-uso/consultarListaAlumnosSecretaria/README.md) | **Desarrollo** |
> |-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Construcción
- **Disciplina**: Desarrollo
- **Caso de uso**: `consultarListaAlumnos()` (Secretaria)
- **Actor**: Secretaria
- **Versión**: 1.0
- **Fecha**: 2026-06-01

## trazabilidad código ↔ diseño

| Participante del diseño | Implementación |
|---|---|
| AlumnosPage (`/alumnos`) | [src/frontend/src/pages/AlumnosPage.tsx](/src/frontend/src/pages/AlumnosPage.tsx) |
| alumnosService.listar | [src/frontend/src/services/alumnosService.ts](/src/frontend/src/services/alumnosService.ts) |
| Schemas `PaginaOut<T>` + `AlumnoListaItem` | [src/frontend/src/types/paginacion.ts](/src/frontend/src/types/paginacion.ts), [src/frontend/src/types/alumnos.ts](/src/frontend/src/types/alumnos.ts) |
| AlumnosRouter (`GET /alumnos?page&size&q`) | [src/backend/app/routers/alumnos.py](/src/backend/app/routers/alumnos.py) |
| UsuarioRepository.buscar_alumnos | [src/backend/app/repositories/usuario_repository.py](/src/backend/app/repositories/usuario_repository.py) |
| Schema `PaginaOut[T]` + `AlumnoListaItemOut` | [src/backend/app/schemas/paginacion.py](/src/backend/app/schemas/paginacion.py), [src/backend/app/schemas/alumnos.py](/src/backend/app/schemas/alumnos.py) |

## verificación end-to-end

| Escenario | Resultado |
|---|---|
| `GET /alumnos` con token Alumno | 403 |
| `GET /alumnos?page=1&size=10` con Secretaria (sólo alumno1 seed) | 200 `{items:[{username:"alumno1",...}], total:1, page:1, size:10}` |
| `GET /alumnos?q=López` | 200 — filtro `LIKE %López%` sobre nombre+apellidos+username+email |
| Tras importar listas → reload | total sube de 1 a 3 |

## decisiones materializadas

- **Sin capa de Service** — Router llama directo al Repository (regla "Service solo donde hay lógica").
- **`UsuarioRepository.buscar_alumnos`** filtra por `tipo='alumno'` y aplica `LIKE %q%` lowercase sobre 4 columnas. `total` calculado vía subconsulta `count()`.
- **`PaginaOut[T]` genérico** reutilizable para futuros listados paginados.

## referencias

- [Análisis](/RUP/01-analisis/casos-uso/consultarListaAlumnosSecretaria/README.md)
- [Diseño](/RUP/02-diseño/casos-uso/consultarListaAlumnosSecretaria/README.md)
- [conversation-log.md](/conversation-log.md)
