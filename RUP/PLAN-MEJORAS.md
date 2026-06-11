# Plan de mejoras post-base

Tras la primera ronda de pruebas manuales sobre el sistema base (26 CUs implementados), surgieron 5 huecos iniciales (1 bug, 2 mejoras de UX y 2 funcionalidades faltantes), más uno detectado mientras se ejecutaba el plan (cardinalidad de grupos por sesión). Este plan los aborda en orden de coste creciente.

**Principio de reparto que guía el plan:** la Secretaría es la operadora académica del sistema (alumnos, matrículas, asignaturas, planes); el Administrador es el operador del sistema (cuentas de personal: profesores, directores, secretarias, administradores). Esto justifica mover a Secretaria las altas que hoy hace el Administrador y darle también el catálogo de asignaturas.

## Resumen

| # | Item | Alcance RUP | Coste estimado | Estado |
|---|------|-------------|----------------|--------|
| M1 | Asistencias en la ficha del alumno | 03 (backend + pequeño frontend) | bajo | hecho (2026-06-10) |
| M2 | Filtro de asignatura en `/sesiones-clase` | 03 (solo frontend) | bajo | hecho (2026-06-10) |
| M3 | Grupo en sesión: desplegable derivado del historial | 03 (backend + frontend) | bajo | hecho (2026-06-10) |
| M6 | Sesiones con múltiples grupos (cardinalidad 1 → N) | 01 + 02 + 03 | medio | hecho (2026-06-10) |
| M7 | Restaurar `Grado` como entidad y scoping de Director/Secretaria por grado | 01 + 02 + 03 | alto | hecho (2026-06-10) |
| M4 | Alta individual de alumno por Secretaria; el Administrador deja de poder crear alumnos | 01 + 02 + 03 | medio | hecho (2026-06-11) |
| M5 | Catálogo de asignaturas + asignar profesor↔asignatura por Secretaria | 01 + 02 + 03 | alto | pendiente |

Orden recomendado: M1 → M2 → M3 → M6 → M7 → M4 → M5. Los tres primeros son arreglos contenidos que no tocan diseño; M6, M7, M4 y M5 atraviesan las tres disciplinas.

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

## M2 — Filtro de asignatura en el listado de sesiones  ·  **hecho (2026-06-10)**

**Síntoma.** El `<select>` de la cabecera de `/sesiones-clase` parecía un filtro pero solo alimentaba la exportación. Confuso.

**Decisión.** Mantener el selector de exportación (es necesario para `exportarHistorialAsistencias`) y **añadir un filtro distinto**, con opción "Todas" por defecto, que sí restrinja la tabla.

**Pasos.**
1. En `src/frontend/src/pages/SesionesClasePage.tsx`:
   - Añadir estado `asigFiltro: number | null` (null = todas).
   - Renderizar un segundo `<select>` con etiqueta "Filtrar por asignatura:", opción "Todas" + las del profesor.
   - Etiquetar explícitamente el `<select>` existente como "Asignatura a exportar:".
   - Derivar `sesionesFiltradas = asigFiltro ? sesiones.filter(s => s.asignatura.id === asigFiltro) : sesiones` y usarlo en el `<tbody>`.
2. Verificar visualmente que (a) "Todas" muestra todo, (b) seleccionar una asignatura reduce la tabla, (c) la exportación sigue funcionando independiente del filtro.

**Sin cambios en backend.** Sin tocar 01/02.

**Resumen de la ejecución.** Cambios en un único archivo:
- `src/frontend/src/pages/SesionesClasePage.tsx` — nuevo estado `asigFiltro`, `<select>` "Filtrar por asignatura:" sobre la tabla, etiqueta "Exportar:" delante del selector preexistente, `.filter()` aplicado al `.map()` del `<tbody>`.

---

## M3 — Grupo en sesión: desplegable derivado  ·  **hecho (2026-06-10)**

**Síntoma.** El campo "Grupo" al crear sesión era un `<input>` de texto libre. Fácil teclear inconsistencias (`3A` vs `3-A` vs `3 A`).

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

**Resumen de la ejecución.** Cambios en 4 archivos:
- `src/backend/app/repositories/sesion_clase_repository.py` — nuevo `grupos_distintos(profesor_id, asignatura_id)` con `SELECT DISTINCT s.grupo`.
- `src/backend/app/routers/sesiones_clase.py` — nuevo `GET /sesiones-clase/grupos?asignatura_id=N`, insertado antes de `GET /{sesion_id}` para que FastAPI no lo intente parsear como id.
- `src/frontend/src/services/sesionesClaseService.ts` — método `gruposUsados(asignaturaId)`.
- `src/frontend/src/pages/CrearSesionClasePage.tsx` — al cambiar de asignatura recarga los grupos; renderiza `<select>` con los previos + opción "+ Nuevo grupo…", o `<input>` directo si no hay previos; envoltorio `<div>` + `display:block` en el botón "← Volver al listado de grupos" para que no se cuele al lado del campo "Aula" (bug detectado en la primera prueba).

---

## M4 — Alta individual de alumno por Secretaria  ·  **hecho (2026-06-11)**

**Resumen de la ejecución.** Implementado completo en 01 + 02 + 03:
- 01-analisis y 02-diseño: nuevo CU `crearAlumno` (espejo de `crearUsuario` con actor Secretaria y `tipo` fijo). En el análisis se aplicó "Introduce Parameter Object" (Fowler) con `DatosPersonalesAlumno`, consumiendo parte de la deuda blanda que dejó `crearSesionClase` para refactorizar `crear*` con ≥4 parámetros. En el diseño se materializa como `CrearAlumnoRequest` (Pydantic).
- 03-desarrollo: nuevo `POST /alumnos` bajo `require_rol(["secretaria"])`, que reutiliza `UsuarioService.crear` con `tipo="alumno"` fijado por el router (polimorfismo single-source en `UsuarioRepository`). Doble defensa: `POST /usuarios` rechaza `tipo="alumno"` con 422 y `CrearUsuarioPage` retira la opción del `<select>`. Nueva página `CrearAlumnoPage` (`/alumnos/nuevo`, secretariaOnly) y botón "+ Nuevo alumno" en `/alumnos` visible solo para Secretaria.
- **Divergencia respecto al diseño:** sin campo `telefono` (no existe en el modelo `Usuario`; el alta queda con 5 campos en lugar de los 6 del diseño).
- Total CUs: 27 → 28.



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

## M6 — Sesiones con múltiples grupos (cardinalidad 1 → N)  ·  **hecho (2026-06-10)**

**Síntoma.** Validando M2 (filtro de listado) el usuario detectó que el modelo asume **un grupo por sesión** (`grupo: String(50)`). La realidad académica permite que una misma sesión sirva a varios grupos a la vez — caso canónico: Inglés con ADE + Ing. Informática + Ing. Org. Industrial en el mismo aula, mismo horario. La columna "Grupo" del listado mentía: solo podía mostrar una de varias etiquetas.

**Decisión de modelado.** `grupos: list[str]` como columna JSON en `sesiones_clase`. **No** se promueve a entidad `Grupo` con tabla N:M porque:
- Un grupo aquí no tiene identidad reusable: "3A en IYA040" ≠ "3A en IYA041", son cohortes contextuales.
- Un grupo no tiene atributos propios (tutor, capacidad, calendario) — sería tabla de `(id, nombre)` vacía de semántica.
- No hay CU de gestión de grupos; convertir a entidad arrastraría un CU nuevo (paralelo a M5) cuya justificación no existe.
- Si en el futuro Grupo gana atributos, migrar de JSON list a entidad con FK es directo (un `INSERT … SELECT DISTINCT` desde la columna JSON).

Coherente con la decisión original de 02-diseño de mantener `grupo` como string libre (YAGNI); solo se cambia la cardinalidad.

**Cambios en disciplinas RUP.**

### 01-analisis
- `casos-uso/crearSesionClase/README.md`: actualización de la introducción y de las definiciones canónicas de `SesionDeClase` y `DatosSesionClase` para reflejar `grupos: list[str]`. Se añadió una nota "Evolución post-base" remitiendo a este plan. Las menciones a "grupo" en la sección histórica "Long Parameter List" se preservan (es narrativa pedagógica sobre un problema distinto, no canónica).

### 02-diseño
- `casos-uso/crearSesionClase/README.md`: actualización de `participantes`, contrato HTTP del POST y la decisión "grupos/aula strings libres" para documentar por qué no entidad.
- `casos-uso/crearSesionClase/secuencia.puml`: parámetro renombrado; SVG regenerado con `plantuml -tsvg`.

### 03-desarrollo
- Backend (7 archivos):
  - `models/sesion_clase.py` — `grupo: String(50)` → `grupos: Mapped[list[str]] = mapped_column(JSON, default=list)`.
  - `schemas/sesiones_clase.py` — `grupos: list[str]` en `SesionDeClaseOut` y `CrearSesionClaseRequest`; docstring de `EditarSesionClaseRequest` actualizado (grupos sigue siendo no editable post-creación).
  - `services/sesion_clase_service.py` — nuevo `_normalizar_grupos` que recorta, descarta vacíos, deduplica y exige al menos 1.
  - `repositories/sesion_clase_repository.py` — `crear()` usa `datos.grupos`; `grupos_distintos()` aplana las listas JSON en Python (pequeña escala, evita acoplamiento a `JSON_EACH` de SQLite).
  - `services/generador_archivo_asistencias.py` — columna CSV `grupo` → `grupos`, valor `", ".join(s.grupos)`.
  - `services/asistencia_service.py::serializar_sesion_para_csv` — misma transformación.
  - `scripts/seed.py` — `grupo="3A"` → `grupos=["3A"]`.
- Frontend (4 archivos):
  - `types/sesiones_clase.ts` — `grupo: string` → `grupos: string[]` en `SesionDeClase` y `CrearSesionClaseRequest`.
  - `pages/SesionesClasePage.tsx` — columna "Grupo" → "Grupos"; render con `grupos.join(', ')`.
  - `pages/SesionClaseActivaPage.tsx` — mismo render.
  - `pages/CrearSesionClasePage.tsx` — reescritura del bloque de selección: chips removibles con × para los grupos añadidos, `<input list="grupos-previos">` con `<datalist>` autocompletando los grupos previos no seleccionados, botón "Añadir" (también Enter). El botón problemático "← Volver al listado de grupos" desaparece — ya no aplica con chips.
- BD: borrar `cgu.db` y re-ejecutar `seed.py` (mismo flujo que M1; la columna JSON es un cambio destructivo en SQLite y `Base.metadata.create_all` no migra esquemas).

**Verificación.**
- `curl` confirma: listado devuelve `grupos: ["3A"]` (array); `POST` con `grupos: []` → 422 "indica al menos un grupo"; `POST` con `grupos: ["ADE","INF"]` → 201.
- UI: chips, autocomplete contra previos, validación cliente y servidor.

---

## M7 — Restaurar `Grado` como entidad y scoping de Director/Secretaria  ·  **hecho (2026-06-10)**

**Resumen de la ejecución.** Implementado completo en 01 + 02 + 03:
- 01-analisis y 02-diseño: nuevo CU `gestionarCatalogoGrados` (CRUD por Secretaria) + 4 notas de evolución en `consultarSolicitudesDispensas`, `editarSolicitudDispensaDirector`, `consultarListaAlumnosSecretaria` y `crearSesionClase`.
- 03-desarrollo: entidad `Grado` con `codigo` único; FKs en `Asignatura.grado_id` (sustituye `plan_estudios`/`facultad`), `Matricula.grado_id` y `Usuario.grado_id`; políticas con scoping; router `/grados` bajo Secretaria; frontend `GradosPage` + selectores condicionales en alta/edición de usuarios.
- **Corrección lingüística del SDR durante implementación:** la relación `Grado --> SecretariaAcademica : Gestionado por` se lee como "gestionado por (el departamento de) Secretaría Académica", no por una cuenta concreta. Por tanto el scoping por grado se aplica **solo al Director** (relación 1:1 con identidad); la Secretaría queda como departamento colectivo sin scoping. El seed final tiene `secretaria1` sin grado vinculada a las matrículas de ambos grados.
- Total CUs: 26 → 27.



**Síntoma.** En la realidad académica cada Grado tiene su propio Director (el de ADE no resuelve dispensas de Informática) y su propia Secretaria (idem). En el sistema actual `DirectorDeGrado` y `SecretariaAcademica` son globales: cualquiera ve y resuelve cualquier cosa. `services/politica_acceso.py:130` materializa la pifia: `PoliticaDirector.puede_ver` devuelve literalmente `True` siempre.

**Causa raíz.** El **SDR sí modeló `Grado` como entidad de dominio** (`RUP/00-requisitos/ModeloDelDominio/DiagramasDeClase/ModeloCompleto.puml`):

```
class Grado
Matricula --> Grado : Pertenece a
Asignatura --> Grado : Pertenece a
Grado --> DirectorDeGrado : Dirigido por
Grado --> SecretariaAcademica : Gestionado por
DirectorDeGrado -u-|> Profesor : Es un
```

Durante análisis/diseño la entidad se aplanó: `Asignatura.plan_estudios` y `Asignatura.facultad` son strings libres, `Matricula` no tiene grado, y Director/Secretaria son globales. La decisión local en `crearSesionClase` README ("plan_estudios como string libre, YAGNI") arrastró sin querer la pérdida del scoping. **A diferencia de M5 (alta de catálogo de asignaturas, fuera del SDR), M7 es restaurar algo que el SDR pidió y se perdió.**

**Decisión.** Implementarlo tal cual el SDR. Particularidades verificadas en el código actual antes de planificar:
- `DirectorDeGrado(Profesor)` **ya hereda de Profesor** en `models/usuario.py:57` — la STI anidada del SDR ya está implementada. No hay coste ahí.
- Cada `Asignatura` pertenece a **un único** `Grado` (simplificación del SDR aceptada — universidades reales pueden compartir asignaturas entre grados con códigos distintos, pero no es nuestro alcance).

**Cambios en disciplinas RUP.**

### 01-analisis
- Restaurar `Grado` como entidad en cualquier CU que lo mencione (sobre todo los del bloque Dispensa: `consultarSolicitudesDispensas`, `consultarSolicitudDispensa`, `editarSolicitudDispensaDirector`, y los del bloque Matrícula: `importarMatriculas`, `consultarDetalleMatricula`).
- Documentar la corrección en el README de `crearSesionClase` (donde se tomó la decisión original de "string libre") explicando por qué se reabre.
- **Nuevo CU `gestionarCatalogoGrados`** (Secretaria), paralelo al `gestionarCatalogoAsignaturas` de M5. Sin él los grados solo entran por seed, y un sistema con scoping por grado necesita poder dar de alta nuevos grados en runtime. Se ejecuta natural junto a M5.

### 02-diseño
- Nueva entidad `Grado` con `id, codigo, nombre, facultad`. La `facultad` migra desde `Asignatura.facultad` hacia `Grado.facultad` (un grado pertenece a una facultad; reducir duplicación).
- Cambios en `Asignatura`: quitar `plan_estudios` y `facultad`, añadir `grado_id` FK.
- Cambios en `Matricula`: añadir `grado_id` FK (cierra la "decisión derivada en API" que hoy infiere facultad/plan_estudios desde las asignaturas matriculadas).
- Cambios en `DirectorDeGrado` y `SecretariaAcademica`: añadir `grado_id` FK.
- `PoliticaDirector.puede_ver` y `obtener_listado`: filtrar dispensas donde `dispensa.asignatura_matriculada.asignatura.grado_id == director.grado_id`.
- `PoliticaSecretaria`: cascada completa — filtra por grado en dispensas, alumnos y matrículas. Coherente con el SDR (`Matricula → Grado : Pertenece a`, `Grado → SecretariaAcademica : Gestionado por`). Sin la cascada, `secretaria1` seguiría viendo alumnos y matrículas de otros grados, lo que contradice el modelo.
- Migración limpia de `Asignatura.facultad` a `Grado.facultad` (un solo lugar). El CSV de import de asignaturas, cuando entre, no requerirá `facultad` — se infiere del grado.
- Documentar en `crearSesionClase` README que la decisión "string libre" queda revertida.

### 03-desarrollo

**Backend (modelos):**
- `models/grado.py` nuevo: `Grado(Base)` con id, codigo (unique), nombre, facultad.
- `models/asignatura.py`: quitar `plan_estudios` y `facultad`, añadir `grado_id: Mapped[int] = mapped_column(ForeignKey("grados.id"))` + relación `grado: Mapped[Grado]`.
- `models/matricula.py`: añadir `grado_id` FK + relación.
- `models/usuario.py`: añadir `grado_id` a `DirectorDeGrado` y `SecretariaAcademica`. Como es STI, las columnas viven en `usuarios` y son NULL para los otros subtipos. Alternativa: usar `polymorphic_load="inline"` y `concrete=False` para mantener limpio.

**Backend (schemas):**
- `schemas/grados.py` nuevo: `GradoOut`, `CrearGradoRequest`, `EditarGradoRequest`.
- `schemas/asignaturas.py`: `AsignaturaOut.grado: GradoOut` en lugar de `plan_estudios` + `facultad`.
- `schemas/usuarios.py`:
  - `CrearUsuarioRequest`: añadir `grado_id: int | None`. Validador: obligatorio si `tipo in {"director","secretaria"}`.
  - `EditarUsuarioRequest`: añadir `grado_id` opcional.
  - `UsuarioDetalleOut`: añadir `grado: GradoOut | None`.
- `schemas/matriculas.py`: añadir `grado` a los `Out`.

**Backend (servicios y políticas):**
- `services/politica_acceso.py`:
  - `PoliticaDirector.puede_ver(solicitud, usuario)` → `solicitud.asignatura_matriculada.asignatura.grado_id == usuario.grado_id`.
  - `PoliticaDirector.obtener_listado(...)` → filtra por grado en lugar de devolver todas.
  - `PoliticaSecretaria` análogo en dispensas, alumnos y matrículas (cascada completa).
- `services/alumno_service.listar_*`: filtro por grado de la Secretaria. El Profesor sigue sin grado (puede impartir en varios).
- `services/matricula_service.listar`: filtro por grado de la Secretaria.
- Imports masivos (`importarListasAlumnos`, `importarMatriculas`): los alumnos/matrículas importados se asignan al grado de la Secretaria que importa.

**Backend (seed):**
- Crear **al menos 2 `Grado`**: "INF" (Ingeniería Informática, Escuela Politécnica Superior) y "ADE" (Administración y Dirección de Empresas, Facultad de Económicas). Dos grados son necesarios para que las pruebas manuales del scoping puedan ver el efecto real (un solo grado oculta el filtrado).
- `director1`, `secretaria1` y `alumno1` quedan en INF. Sembrar adicionalmente `director2`, `secretaria2` y `alumno2` en ADE para que las pruebas crucen.
- Las asignaturas seed (`IYA*`) van todas a INF. Añadir 1–2 asignaturas seed de ADE para que `alumno2` tenga matrícula no vacía.
- Matrículas: una para `alumno1` en INF (ya existe), otra para `alumno2` en ADE.

**Frontend:**
- `types/grados.ts` nuevo.
- `services/gradosService.ts` nuevo: `listar()` para los selectores; `crear()`, `actualizar()`, `borrar()` para el CU `gestionarCatalogoGrados`.
- `pages/CrearUsuarioPage.tsx`: cuando `tipo` es director o secretaria, mostrar `<select>` de grados (poblado con `gradosService.listar()`).
- `pages/EditarUsuarioPage.tsx`: idem para edición.
- `pages/ConsultarUsuarioPage.tsx`: mostrar el grado del Director/Secretaria.
- Listados que muestran `plan_estudios` o `facultad` de asignatura: cambiar a `grado.nombre` / `grado.facultad`. Buscar referencias antes (probablemente `ConsultarDetalleMatriculaPage`, `MatriculasPage`).
- Nueva pantalla `GradosPage` (CRUD por Secretaria) para el CU `gestionarCatalogoGrados`. Acceso desde el nav de Secretaria.

**BD:** borrar `cgu.db` y re-ejecutar `seed.py`. La migración no es declarativa (cambios de schema en SQLite).

**Pruebas manuales clave:**
- Loguearse como `director1` (INF) y `director2` (ADE) y verificar que cada uno ve solo las dispensas de su grado.
- Como `secretaria1` (INF), las dispensas, alumnos y matrículas que ve son solo de INF; misma comprobación cruzada con `secretaria2` (ADE).
- Como `profesor1` (sin grado): sigue viendo solo dispensas de sus asignaturas (PoliticaProfesor existente). No se rompe.
- `crearUsuario` rechaza alta de Director/Secretaria sin `grado_id` (422).
- `gestionarCatalogoGrados`: la Secretaria puede crear un tercer grado y darle de alta personal y asignaturas.

---

## Lo que cambia en el denominador "26 CUs"

Si se ejecuta el plan completo: 26 → **30 CUs**.
- M4 añade 1 (`crearAlumno`).
- M5 añade 2 (`gestionarCatalogoAsignaturas`, `asignarAsignaturasAProfesor`).
- M7 añade 1 (`gestionarCatalogoGrados`).
- M6 no añade — refina la cardinalidad de un CU existente (`crearSesionClase`).

Actualizar el README principal y `CLAUDE.md` (sección "Medida de progreso") al terminar.
