# CGU > consultarDetalleAlumno (Profesor) > Desarrollo

> | [🏠️](/README.md) | [Desarrollo](/RUP/03-desarrollo/README.md) | [Análisis](/RUP/01-analisis/casos-uso/consultarDetalleAlumno/README.md) | [Diseño](/RUP/02-diseño/casos-uso/consultarDetalleAlumno/README.md) | **Desarrollo** |
> |-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Construcción
- **Disciplina**: Desarrollo
- **Caso de uso**: `consultarDetalleAlumno()` (Profesor)
- **Actor**: Profesor
- **Versión**: 1.0
- **Fecha**: 2026-06-02

## trazabilidad código ↔ diseño

| Participante del diseño | Implementación |
|---|---|
| DetalleAlumnoPage (`/alumnos/{id}`) | [src/frontend/src/pages/DetalleAlumnoPage.tsx](/src/frontend/src/pages/DetalleAlumnoPage.tsx) |
| alumnosService.obtener | [src/frontend/src/services/alumnosService.ts](/src/frontend/src/services/alumnosService.ts) |
| AlumnosRouter (`GET /alumnos/{id}`) | [src/backend/app/routers/alumnos.py](/src/backend/app/routers/alumnos.py) |
| AlumnoService.obtener_detalle (verificación competente) | [src/backend/app/services/alumno_service.py](/src/backend/app/services/alumno_service.py) |
| UsuarioRepository.obtener_alumno_con_matricula (eager-load) | [src/backend/app/repositories/usuario_repository.py](/src/backend/app/repositories/usuario_repository.py) |
| Schema `AlumnoDetalleOut` con `asignaturas_matriculadas` y `asistencias` | [src/backend/app/schemas/alumnos.py](/src/backend/app/schemas/alumnos.py) |
| `AsignaturaMatriculadaConAsistenciaOut` (extiende el DTO base con `presentes`, `total_sesiones`, `porcentaje_asistencia`) | [src/backend/app/schemas/alumnos.py](/src/backend/app/schemas/alumnos.py) |
| `AsistenciaRepository.estadisticas_por_alumno` (presentes / sesiones cerradas por asignatura) | [src/backend/app/repositories/asistencia_repository.py](/src/backend/app/repositories/asistencia_repository.py) |

## verificación end-to-end

| Escenario | Resultado |
|---|---|
| Profesor con alumno cuya matrícula incluye una asignatura que imparte | 200 + ficha completa, `asistencias=[]` |
| Alumno inexistente | 404 `AlumnoNoEncontrado` |
| Profesor con alumno sin intersección de asignaturas | 403 `ProfesorNoCompetente` |
| Secretaria | 200 sin verificación competente |
| Frontend: secciones colapsables "Asignaturas matriculadas" y "Asistencias" | render funcional |

## decisiones materializadas

- **`Asistencia` diferida al ramillete actual** — el campo se llena cuando el Profesor ha marcado asistencias para el alumno (no se popula como agregado en este CU).
- **Verificación "Profesor competente" basada en intersección de asignaturas** entre `current_user.asignaturas_impartidas` y las matrículas del alumno.
- **Eager-load explícito** del agregado (`selectinload(matriculas).selectinload(asignaturas_matriculadas).joinedload(asignatura)`) para evitar lazy load async.
- **404 vs 403 distinguidos** — sin enmascaramiento por privacidad.
- **% de asistencia por asignatura** calculado en el router (presentes / sesiones CERRADAS) y proyectado en `AsignaturaMatriculadaConAsistenciaOut`. Umbral del 70% (reglamento académico) visualizado en la columna "Asistencia" con badge verde/rojo. Sin sesiones cerradas → `porcentaje_asistencia = null` y render `—`. El DTO base `AsignaturaMatriculadaDelAlumnoOut` se conserva intacto para el resto de consumidores (selector de dispensa del Alumno y de la Secretaría).

## referencias

- [Análisis](/RUP/01-analisis/casos-uso/consultarDetalleAlumno/README.md)
- [Diseño](/RUP/02-diseño/casos-uso/consultarDetalleAlumno/README.md)
- [conversation-log.md](/conversation-log.md)
