# Plan de mejoras post-base

Tras la primera ronda de pruebas manuales sobre el sistema base (26 CUs implementados), surgieron 5 huecos: 1 bug, 2 mejoras de UX y 2 funcionalidades faltantes. Este plan los aborda en orden de coste creciente.

**Principio de reparto que guía el plan:** la Secretaría es la operadora académica del sistema (alumnos, matrículas, asignaturas, planes); el Administrador es el operador del sistema (cuentas de personal: profesores, directores, secretarias, administradores). Esto justifica mover a Secretaria las altas que hoy hace el Administrador y darle también el catálogo de asignaturas.

## Resumen

| # | Item | Alcance RUP | Coste estimado | Estado |
|---|------|-------------|----------------|--------|
| M1 | Asistencias en la ficha del alumno | 03 (backend + pequeño frontend) | bajo | hecho (2026-06-10) |
| M2 | Filtro de asignatura en `/sesiones-clase` | 03 (solo frontend) | bajo | pendiente |
| M3 | Grupo en sesión: desplegable derivado del historial | 03 (backend + frontend) | bajo | pendiente |
| M4 | Alta individual de alumno por Secretaria; el Administrador deja de poder crear alumnos | 01 + 02 + 03 | medio | pendiente |
| M5 | Catálogo de asignaturas + asignar profesor↔asignatura por Secretaria | 01 + 02 + 03 | alto | pendiente |

Orden recomendado: M1 → M2 → M3 → M4 → M5. Los tres primeros son arreglos contenidos que no tocan diseño; M4 y M5 son CUs nuevos y siguen el ciclo RUP completo.

---

## M1 — Asistencias en la ficha del alumno  ·  **hecho (2026-06-10)**

**Síntoma.** En `/alumnos/:id`, la sección "Asistencias" siempre mostraba `(0) Sin asistencias registradas`, aun cuando había asistencias persistidas tras cerrar sesiones de clase.

**Causa raíz.** `src/backend/app/routers/alumnos.py:214-224` devuelve `asistencias=[]` hardcodeado, con un comentario explícito de que está pendiente conectarse a la entidad `Asistencia`. Las asistencias **sí se persisten** correctamente al cerrar sesión.

**Pasos.**
1. Verificar que el schema `AlumnoDetalleOut.asistencias` admite la forma final esperada (revisar `schemas/alumnos.py`). Si no existe un DTO `AsistenciaDelAlumnoOut` con `sesion_id`, `asignatura_codigo`, `fecha`, `estado`, definirlo.
2. En `repositories/asistencia_repository.py`, añadir `listar_por_alumno(alumno_id)` que devuelva las asistencias con joinedload a `SesionDeClase` y `Asignatura`.
3. En `routers/alumnos.py::obtener_alumno`, sustituir `asistencias=[]` por la llamada al repositorio, ordenando por `sesion.fecha DESC`.
4. Borrar el comentario "Se rellenará cuando el ramillete conecte…".
5. Probar manualmente con `profesor1`: abrir una sesión, marcar a `alumno1` como presente, cerrar la sesión, ir a `/alumnos/{id}` como Secretaria o Profesor y confirmar que aparece.

**Cambios en frontend:** la página `DetalleAlumnoPage.tsx` tenía solo rama para `asistencias.length === 0`. Se añadió la tabla para el caso `length > 0` (columnas Fecha, Asignatura, Estado con `estado-badge`).

**Sin tocar 01/02:** es un fix de implementación de un CU ya analizado/diseñado (`consultarDetalleAlumno`).

**Resumen de la ejecución.** Cambios en 4 archivos:
- `src/backend/app/repositories/asistencia_repository.py` — nuevo método `listar_por_alumno`.
- `src/backend/app/routers/alumnos.py` — usa el repositorio, construye `AsistenciaEnFichaOut` por fila, borra el comentario "placeholder".
- `src/backend/app/schemas/alumnos.py` — quita la nota de placeholder del docstring de `AsistenciaEnFichaOut`.
- `src/frontend/src/pages/DetalleAlumnoPage.tsx` — añade la tabla cuando hay asistencias.

Verificado con `curl` (4 asistencias devueltas para `alumno1`, ordenadas por fecha desc) y con la UI (tabla rendizada en la ficha del alumno).

---

## M2 — Filtro de asignatura en el listado de sesiones

**Síntoma.** El `<select>` de la cabecera de `/sesiones-clase` parece un filtro pero solo alimenta la exportación. Confuso.

**Decisión.** Mantener el selector de exportación (es necesario para `exportarHistorialAsistencias`) y **añadir un filtro distinto**, con opción "Todas" por defecto, que sí restrinja la tabla.

**Pasos.**
1. En `src/frontend/src/pages/SesionesClasePage.tsx`:
   - Añadir estado `asigFiltro: number | null` (null = todas).
   - Renderizar un segundo `<select>` con etiqueta "Filtrar por asignatura:", opción "Todas" + las del profesor.
   - Etiquetar explícitamente el `<select>` existente como "Asignatura a exportar:".
   - Derivar `sesionesFiltradas = asigFiltro ? sesiones.filter(s => s.asignatura.id === asigFiltro) : sesiones` y usarlo en el `<tbody>`.
2. Verificar visualmente que (a) "Todas" muestra todo, (b) seleccionar una asignatura reduce la tabla, (c) la exportación sigue funcionando independiente del filtro.

**Sin cambios en backend.** Sin tocar 01/02.

---

## M3 — Grupo en sesión: desplegable derivado

**Síntoma.** El campo "Grupo" al crear sesión es un `<input>` de texto libre. Fácil teclear inconsistencias (`3A` vs `3-A` vs `3 A`).

**Decisión.** Opción ligera: el desplegable se rellena dinámicamente con los grupos distintos que **ese profesor** ha usado en **esa asignatura**, más una opción "Nuevo grupo…" que abre un input de texto. **Sin entidad `Grupo` ni CU nuevo**: aprovecha que `SesionDeClase.grupo` ya es persistente.

(Si en el futuro se quiere subir esto a entidad `Grupo` con CRUD por Secretaria, M3 no se desperdicia: el `<select>` se reconectaría a `/asignaturas/{id}/grupos` en lugar de derivarlo.)

**Pasos.**
1. Backend: añadir endpoint `GET /sesiones-clase/grupos?asignatura_id=N` que devuelva `list[str]` con los grupos distintos del profesor actual en esa asignatura. Implementar en `routers/sesiones_clase.py` apoyado en una query `DISTINCT s.grupo` filtrada por `profesor_id=usuario.id` y `asignatura_id`.
2. Frontend: en `CrearSesionClasePage.tsx`:
   - Al cambiar `form.asignatura_id`, llamar al endpoint anterior y guardar la lista.
   - Sustituir el `<input type="text">` actual por un `<select>` con esas opciones + opción "Nuevo grupo…".
   - Si elige "Nuevo grupo…", mostrar el `<input>` debajo.
3. Probar: primera vez sin sesiones para una asignatura → solo opción "Nuevo"; tras crear una sesión con `grupo=3A`, volver al formulario y verificar que `3A` aparece como opción.

**Sin tocar 01/02:** es refinamiento de UX de un CU existente (`crearSesionClase`).

---

## M4 — Alta individual de alumno por Secretaria

**Decisión.** Coherencia con el principio del plan: el alta individual de alumnos (incorporación a mitad de curso, becarios tardíos, etc.) es operación académica, le toca a Secretaria. El Administrador deja de poder crear alumnos desde su formulario; queda restringido a cuentas de personal.

**Cambios en disciplinas RUP.**

### 01-analisis
- Nuevo CU `crearAlumno` en `RUP/01-analisis/casos-uso/crearAlumno/` con su README y diagrama de secuencia (espejo de `crearUsuario`, ajustado a actor Secretaria y tipo fijo Alumno). Seguir [[feedback_scope_minimo_disciplinas]] y [[feedback_secuencia_sin_detalles_internos]].
- Actualizar el CU `crearUsuario` para indicar que su alcance ya no incluye `tipo=alumno`.

### 02-diseño
- Espejar lo anterior bajo `RUP/02-diseño/casos-uso/crearAlumno/`.

### 03-desarrollo
- Backend:
  - Nuevo endpoint `POST /alumnos` (no `/usuarios`) protegido por `require_rol(["secretaria"])`. Schema `CrearAlumnoRequest` con los campos de Alumno (sin `tipo` — fijo en `alumno`). Reusar `UsuarioService.crear` con `tipo="alumno"`, o crear `AlumnoService.crear` si conviene.
  - Modificar `UsuarioService.crear` o el router `POST /usuarios` para **rechazar** `tipo=alumno` con `422` y mensaje explícito ("Use POST /alumnos como Secretaria").
- Frontend:
  - Nueva ruta `/alumnos/nuevo` accesible solo a Secretaria, con formulario sencillo (username, password, nombre, apellidos, email, teléfono opcional).
  - Botón "+ Nuevo alumno" en `/alumnos` (junto al "Importar listas" actual) — solo para Secretaria.
  - En `CrearUsuarioPage` (Administrador): quitar la opción `alumno` del `<select>` de tipo.
- Nuevo README en `RUP/03-desarrollo/casos-uso/crearAlumno/`.

**Pruebas manuales:** logueado como Secretaria, crear `alumno9` desde `/alumnos/nuevo`; aparece en `/alumnos`; intentar como Administrador crear un alumno desde `/usuarios/nuevo` y comprobar que ya no es opción.

---

## M5 — Catálogo de asignaturas + asignar profesor↔asignatura

**Decisión.** La gestión del catálogo de asignaturas (alta/edición/baja) y la asignación de qué profesor imparte qué pasan a ser responsabilidad de la Secretaria. Hoy ambas cosas las hace el `seed.py` y no son editables en runtime — limitación seria del sistema.

**Cambios en disciplinas RUP.** Dos CUs nuevos:
- `gestionarCatalogoAsignaturas` (Secretaria): CRUD sobre la entidad `Asignatura`.
- `asignarAsignaturasAProfesor` (Secretaria): añadir/quitar entradas en la tabla N:M `profesor_asignaturas`.

### 01-analisis y 02-diseño
- Crear los dos CUs nuevos en `RUP/01-analisis/casos-uso/` y `RUP/02-diseño/casos-uso/` con su README y diagrama.
- Comprobar si conviene modelar `responsable_id` en `Asignatura` (qué Secretaria la dio de alta) y en la fila de `profesor_asignaturas` (qué Secretaria asignó al profesor) para mantener coherencia con [[feedback_auditoria_coherente_por_entidad]].

### 03-desarrollo

**Backend — catálogo de asignaturas:**
- `routers/asignaturas.py`: añadir `POST`, `PATCH /{id}`, `DELETE /{id}` (la borradura puede ser lógica si conviene, decidir en diseño). El `GET` ya existe.
- `services/asignatura_service.py` nuevo: validar `codigo` único, validar `ects > 0`, validar `caracter ∈ {FB,OB,OP}` (revisar valores reales), comprobar antes de borrar que no haya `AsignaturaMatriculada` ni `SesionDeClase` ni `Profesor` que la referencien (o cascadear si así se decide en diseño).
- Schemas `CrearAsignaturaRequest`, `EditarAsignaturaRequest`.

**Backend — asignar profesor↔asignatura:**
- Endpoints `POST /usuarios/{profesor_id}/asignaturas-impartidas/{asignatura_id}` y `DELETE /usuarios/{profesor_id}/asignaturas-impartidas/{asignatura_id}`, protegidos por Secretaria.
- `services/usuario_service.py`: nuevos métodos `asignar_asignatura(profesor_id, asignatura_id)` y `desasignar_asignatura(...)`. Validar que el usuario sea Profesor (no Alumno/Director/etc.).

**Frontend:**
- Sección nueva "Asignaturas" en el nav de Secretaria (`Layout.tsx`).
- Pantallas: `AsignaturasPage` (listado + alta/edición/borrado), `AsignarAsignaturasProfesorPage` (selecciona profesor → ver y editar sus asignaturas impartidas como checkboxes).
- READMEs en `RUP/03-desarrollo/casos-uso/gestionarCatalogoAsignaturas/` y `asignarAsignaturasAProfesor/`.

**Pruebas manuales:** como Secretaria crear `IYA050`; asignársela a `profesor1`; loguearse como `profesor1` y comprobar que ya aparece en sus pestañas de `/alumnos` y como opción en `/sesiones-clase/nuevo`.

**Riesgo a vigilar.** El `seed.py` quedará como "datos iniciales de cortesía para demo"; cualquier asignatura que se borre desde la UI desaparece, y el seed solo la repondrá tras un re-arranque limpio (es idempotente y solo crea si no existe). Documentarlo en el README del backend.

---

## Lo que cambia en el denominador "26 CUs"

Si se ejecuta el plan completo: 26 → **29 CUs** (M4 + dos en M5). Actualizar el README principal y `CLAUDE.md` (sección "Medida de progreso") al terminar.
