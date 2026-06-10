# CGU > consultarListaAlumnos (Profesor) > Desarrollo

> | [🏠️](/README.md) | [Desarrollo](/RUP/03-desarrollo/README.md) | [Análisis](/RUP/01-analisis/casos-uso/consultarListaAlumnos/README.md) | [Diseño](/RUP/02-diseño/casos-uso/consultarListaAlumnos/README.md) | **Desarrollo** |
> |-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Construcción
- **Disciplina**: Desarrollo
- **Caso de uso**: `consultarListaAlumnos()` (Profesor)
- **Actor**: Profesor
- **Versión**: 1.0
- **Fecha**: 2026-06-02

## trazabilidad código ↔ diseño

| Participante del diseño | Implementación |
|---|---|
| ListaAlumnosPage (con pestañas por asignatura) | [src/frontend/src/pages/ListaAlumnosPage.tsx](/src/frontend/src/pages/ListaAlumnosPage.tsx) |
| `BifurcacionAlumnos` en `/alumnos` (Profesor ve `ListaAlumnosPage`; Secretaria ve `AlumnosPage`) | [src/frontend/src/App.tsx](/src/frontend/src/App.tsx) |
| alumnosService.listarPorAsignatura | [src/frontend/src/services/alumnosService.ts](/src/frontend/src/services/alumnosService.ts) |
| AlumnosRouter (`GET /alumnos?asignatura_id`) extendido a `["profesor","secretaria"]` | [src/backend/app/routers/alumnos.py](/src/backend/app/routers/alumnos.py) |
| AlumnoService.listar_por_asignatura (defensa "Profesor competente") | [src/backend/app/services/alumno_service.py](/src/backend/app/services/alumno_service.py) |
| UsuarioRepository.buscar_por_asignatura (join con `matriculas`+`asignaturas_matriculadas`) | [src/backend/app/repositories/usuario_repository.py](/src/backend/app/repositories/usuario_repository.py) |
| Tabla N:M `profesor_asignaturas` + relación `Usuario.asignaturas_impartidas` | [src/backend/app/models/profesor_asignatura.py](/src/backend/app/models/profesor_asignatura.py), [src/backend/app/models/usuario.py](/src/backend/app/models/usuario.py) |
| GET `/profesores/yo/asignaturas` (carga de pestañas) | [src/backend/app/routers/profesores.py](/src/backend/app/routers/profesores.py) |

## verificación end-to-end

| Escenario | Resultado |
|---|---|
| Profesor sin `asignatura_id` | 422 "Falta el parámetro `asignatura_id`" |
| Profesor con asignatura impartida (IYA040) | 200 + `PaginaOut[AlumnoEnAsignaturaOut]` con curso_academico embebido |
| Profesor con asignatura NO impartida (IYA010) | 403 `ProfesorNoCompetente` |
| Secretaria con o sin `asignatura_id` | 200 (comportamiento previo preservado) |
| Frontend: pestañas por asignatura, click cambia el filtro | comportamiento esperado |

## decisiones materializadas

- **Tabla N:M `profesor_asignaturas`** introducida ahora (cierre de la deuda diferida en `crearSesionClase`).
- **Endpoint único `GET /alumnos`** con dispatch interno por rol — Service ramifica.
- **Schema `AlumnoEnAsignaturaOut`** distinto de `AlumnoListaItemOut` de Secretaria (campos académicos derivados del join con `Matricula`).
- **Defensa "Profesor competente"** en el Service comparando `asignatura_id` contra `current_user.asignaturas_impartidas`.
- **`BifurcacionAlumnos`** en `/alumnos` decide qué página renderizar según el rol — evita rutas duplicadas.

## referencias

- [Análisis](/RUP/01-analisis/casos-uso/consultarListaAlumnos/README.md)
- [Diseño](/RUP/02-diseño/casos-uso/consultarListaAlumnos/README.md)
- [conversation-log.md](/conversation-log.md)
