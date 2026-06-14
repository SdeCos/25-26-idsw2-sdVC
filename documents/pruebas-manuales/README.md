# Pruebas manuales — Centro de Gestión Universitaria

Guion de verificación funcional end-to-end del sistema (30 CUs) antes de la entrega. Cada bloque corresponde a un actor/ramillete y se recorre en orden. Las casillas `[ ]` se marcan al pasar.

## Preparación

1. **Estado limpio (opcional, recomendado primera pasada).** Para empezar desde seed exacto:
   ```bash
   rm src/backend/cgu.db
   ```
   Si no se borra, el seed se aplica idempotente sobre el estado actual.
2. **Arrancar el sistema:**
   ```bash
   ./scripts/start.sh
   ```
   Backend en `http://localhost:8000`, frontend en `http://localhost:5173`. Ctrl+C detiene ambos.
3. Abrir el navegador en `http://localhost:5173`.

### Usuarios sembrados

| Username       | Contraseña      | Rol               | Grado     |
| -------------- | --------------- | ----------------- | --------- |
| `admin`        | `admin123`      | Administrador     | —         |
| `secretaria1`  | `secre123`      | SecretariaAcadémica | —       |
| `director1`    | `director123`   | DirectorDeGrado   | INF       |
| `director2`    | `director123`   | DirectorDeGrado   | ADE       |
| `profesor1`    | `profe123`      | Profesor          | —         |
| `alumno1`      | `alumno123`     | Alumno            | INF (matr.)|
| `alumno2`      | `alumno123`     | Alumno            | ADE (matr.)|

### CSVs de prueba

Disponibles en [`csvs/`](csvs/):
- `alumnos-validos.csv` — 3 filas correctas (importan 3 alumnos: `alumno3..alumno5`).
- `alumnos-con-errores.csv` — 6 filas: 2 válidas (`alumno6`, `alumno10`) + 4 con error (username vacío, password vacía, nombre vacío, email inválido).
- `matriculas-validas.csv` — 7 detalles para `alumno3..alumno5` (después de importarlos primero).
- `matriculas-con-errores.csv` — alumno desconocido, asignatura desconocida, n_matricula no entero, n_matricula < 1, y dos asignaturas con intersección de grados vacía en la misma matrícula (error de coherencia de grado post-M5).

---

## 0. Iniciar sesión / cerrar sesión (Usuario — 2 CUs)

- [x] **iniciarSesion()** — caso vacío: dejar usuario y contraseña en blanco → error visible "campos obligatorios".
- [x] **iniciarSesion()** — credenciales inválidas: usuario `admin`, contraseña `xxx` → error "Credenciales inválidas".
- [x] **iniciarSesion()** — credenciales válidas con `admin/admin123` → redirige al dashboard, badge con nombre y rol arriba a la derecha.
- [x] **cerrarSesion()** — clic en "Cerrar sesión" → vuelve a `/login`, intentar acceder a `/usuarios` redirige a login.

---

## 1. Administrador (3 CUs)

Login como `admin / admin123`.

- [x] **consultarUsuario()** — entra a `/usuarios`, ve listado paginado con todas las cuentas del seed.
- [x] **consultarUsuario()** — abre la ficha de `profesor1`; muestra tipo, email, fecha de creación.
- [x] **crearUsuario()** — `/usuarios/nuevo`:
  - Crea `profesor2` (tipo profesor, contraseña `profe123`, email `profesor2@cgu.es`).
  - Intenta seleccionar `tipo=alumno` en el `<select>` → **opción no aparece** (M4: el alta de alumnos pasó a Secretaria).
  - Crea `director3` (tipo director); el formulario exige `grado_id` y muestra los grados disponibles.
- [x] **editarUsuario()** — abre `profesor2`, cambia el email a `nuevo@cgu.es`, guarda; ve el cambio en la ficha.
- [x] **editarUsuario()** — desactiva `profesor2` (`activo=false`); intenta loguear con esas credenciales → falla.
- [x] **Negativo** — logueado como admin, intentar entrar a `/alumnos` → 403 o redirect (el Administrador no opera sobre Alumnos).
- [x] **Negativo (post-extensión 2026-06-14)** — como `admin`, intentar `GET /usuarios/<id_alumno>` (escribir la URL a mano con el id de un alumno) → **403 o redirect**. Lo mismo con `/usuarios/<id_alumno>/editar`. El admin no opera sobre alumnos ni en lectura ni en escritura.

---

## 2. Secretaria — Catálogos (2 CUs)

Login como `secretaria1 / secre123`.

### gestionarCatalogoGrados()

- [x] Listado en `/grados` muestra `INF` y `ADE` del seed.
- [x] Crear grado `MED` (Medicina, Facultad de Ciencias de la Salud).
- [x] Editar `MED`: cambiar facultad → se refleja.
- [x] Intentar borrar `INF` → **error** "tiene asignaturas/usuarios asociados".
- [x] Borrar `MED` (sin nada asociado) → desaparece del listado.

### gestionarCatalogoAsignaturas()

- [x] Listado en `/asignaturas` muestra las 8 del seed (cada una con su badge de grado(s); `IDIO1` con dos: INF+ADE).
- [x] Crear `IYA050` ("Patrones avanzados", 6 ECTS, OB, curso 4, grado INF) → aparece en el listado.
- [x] Crear `IDIO2` con grados `INF + ADE` simultáneos (multi-grado) → aparece con ambos badges.
- [x] Editar `IYA050`: cambiar nombre → se refleja.
- [x] Crear con código duplicado (`IYA040`) → error "código ya existe".
- [x] Intentar borrar `IYA040` (la imparte profesor1) → error "tiene profesores impartiéndola / matrículas / sesiones".
- [x] Borrar `IYA050` (no referenciado) → desaparece.

---

## 3. Secretaria — Personal docente (1 CU)

### asignarAsignaturasAProfesor()

- [x] En `/profesores`, abrir `profesor1` → checkboxes con todas las asignaturas; ya marcadas `IYA038`, `IYA040`, `IYA041` (del seed).
- [x] Marcar `IDIO1` → cambio optimista; recargar la página confirma el alta.
- [x] Desmarcar `IDIO1` → desaparece de impartidas.
- [x] Repetir con `profesor2` (creado en bloque 1): asignar `IYA010`.
- [x] Acción idempotente: marcar dos veces seguidas la misma asignatura no rompe nada.

---

## 4. Secretaria — Alumnos (4 CUs)

### crearAlumno()

- [x] `/alumnos/nuevo`: crear `alumno_test` (password `test123`, email `test@cgu.es`).
- [x] Aparece en el listado de `/alumnos`.
- [x] Como `admin`, comprobar que **no aparece** en su CRUD de usuarios (los alumnos no están en `/usuarios` del admin).

### importarListasAlumnos()

- [x] En `/alumnos`, clic en "Importar listas".
- [x] Subir `csvs/alumnos-validos.csv` → informe: "3 creados, 0 actualizados, 0 errores". `alumno3..alumno5` aparecen en el listado.
- [x] Subir `csvs/alumnos-validos.csv` **de nuevo** → "0 creados, 3 actualizados" (upsert; los emails se reescriben con los mismos valores).
- [x] Subir `csvs/alumnos-con-errores.csv` → informe: **"2 creados (alumno6, alumno10), 4 errores"**. Errores reportados:
  - Fila 3: campo `username` obligatorio.
  - Fila 4: campo `password` obligatorio.
  - Fila 5: campo `nombre` obligatorio.
  - Fila 6: email inválido `'no-es-un-email'`.

### consultarListaAlumnos() (Secretaria)

- [x] `/alumnos` muestra todos los alumnos (seed + importados). No hay filtro por grado para Secretaria (departamento colectivo).
- [x] Buscador por nombre/apellidos funciona.
- [x] Paginación funciona si hay más de 1 página.

### consultarDetalleAlumno()

- [x] Abrir ficha de `alumno1` → muestra datos personales + matrícula `2025/2026 (INF)` con 4 asignaturas + 1 asistencia demo en `IYA040` (sesión cerrada del seed).
- [x] Abrir `alumno3` recién importado → datos personales sin matrícula todavía.

### editarUsuario() — actor extendido (Secretaria sobre alumno)

> Mismo CU que en Bloque 1; aquí se prueba con el rol Secretaria sobre target `tipo=alumno`. Cambio detectado y aplicado durante esta ronda de pruebas — ver entrada del 2026-06-14 en `conversation-log.md`. El catálogo se queda en 30 CUs (no se añade `editarAlumno` espejo porque `Alumno` es `Usuario` por STI y la operación es idéntica).

- [x] En la ficha del alumno aparece un botón **Editar** arriba a la derecha. Logueado como Profesor en la misma ruta `/alumnos/:id`, el botón **no aparece**.
- [x] Clic en Editar → carga el formulario con los datos pre-rellenos. El campo `Tipo` está deshabilitado (invariante: no se edita).
- [x] Cambiar el email de `alumno1` a `alumno1-edit@cgu.es` y guardar → vuelve a la ficha del alumno (`/alumnos/:id`, **no** a `/usuarios/:id` que es admin-only) con el cambio reflejado.
- [x] Editar de nuevo, cambiar el email de vuelta a `maria@cgu.es` (dejar el dato seed limpio).
- [x] Desde el form, clic en "← Cancelar" → vuelve a la ficha sin guardar.
- [x] **Negativo** — como `secretaria1`, intentar `GET /usuarios/<id_profesor1>` por URL → **403**. La Secretaria solo accede a targets `tipo=alumno`.

---

## 5. Secretaria — Matrículas (2 CUs)

### importarMatriculas()

- [x] En `/matriculas`, clic en "Importar matrículas".
- [x] Subir `csvs/matriculas-validas.csv` → informe: "**3 matrículas creadas, 7 detalles creados, 0 errores**" (1 matrícula por alumno).
- [x] Reimportar el mismo CSV → "0 matrículas, 0 detalles, **7 errores** 'asignatura ya matriculada en este curso'".
- [x] Subir `csvs/matriculas-con-errores.csv` → errores esperados (un por fila, salvo agrupación final):
  - Fila 3: alumno desconocido `'fantasma99'`.
  - Fila 4: asignatura desconocida `'XXX999'`.
  - Fila 5: n_matricula debe ser entero.
  - Fila 6: n_matricula >= 1.
  - Lote: matrícula con asignaturas de grados **incompatibles** (`alumno10`, INF+ADE — intersección vacía).
  - **1 matrícula + 1 detalle creados** (la fila válida de `alumno6` con `IYA040`).

### consultarDetalleMatricula()

- [x] En `/matriculas`, abrir la matrícula de `alumno3` → ve grado (INF, derivado de las asignaturas), curso, las 2 asignaturas matriculadas con n_matricula.
- [x] Abrir la matrícula multi-grado intentada (`alumno10`): debería existir solo la del primer commit de `alumno6` o nada para `alumno10` (porque fue rechazada por grado mixto).

---

## 6. Secretaria — Dispensas (4 CUs)

Login sigue como `secretaria1`.

- [x] **consultarSolicitudDispensa() (Secretaria)** — `/dispensas` muestra **todas** las dispensas (seed: 4 — 3 INF de `alumno1`, 1 ADE de `alumno2`). Sin scoping por grado (decisión M7: Secretaría es departamento colectivo).
- [x] **crearSolicitudDispensa() (Secretaria)** — crea una dispensa para `alumno3` en `IDIO1` con motivo "Convalidación parcial"; aparece en estado PENDIENTE.
- [x] **editarSolicitudDispensa() (Secretaria)** — edita el motivo de la recién creada; persiste el cambio.
- [x] **exportarDispensas()** — botón "Exportar a CSV" descarga `dispensas.csv`. Comprobar que tiene todas las columnas (alumno, asignatura, estado, fechas, responsable, observaciones).
- [x] **Negativo** — intentar editar una dispensa APROBADA (la 3ª del seed) → la UI deshabilita la edición o el backend devuelve 409.

---

## 7. Profesor (8 CUs)

Login como `profesor1 / profe123`.

### consultarListaAlumnos() (Profesor)

- [x] `/alumnos` muestra **una pestaña por asignatura impartida** (`IYA038`, `IYA040`, `IYA041`).
- [x] Cada pestaña muestra solo alumnos matriculados en esa asignatura.
- [x] Sin acceso global a la lista de alumnos (no aparece "Todos").

### consultarDetalleAlumno() (Profesor competente)

- [x] Abrir `alumno1` (matriculado en `IYA040` que imparte profesor1) → muestra la ficha incluyendo las asistencias.
- [x] Manualmente navegar a `alumno2` (matriculado solo en ADE, que profesor1 no imparte) → **403 "Profesor no competente"**.

### crearSesionClase()

- [x] `/sesiones-clase/nuevo`: seleccionar asignatura `IYA040`, grupos `["3A"]` (sale como autocompletado del histórico), aula `Aula 201`, fecha hoy, hora 12:00–13:30, tema "Test".
- [x] Crear con `grupos=[]` → error "indica al menos un grupo".
- [x] Probar M6 (multi-grupo): añadir `"4A"` + `"3B"` como chips → se persisten ambos.
- [x] Probar M3 (grupos previos): al crear otra sesión, el desplegable ya sugiere `3A`, `4A`, `3B`.

### editarSesionClase()

- [x] Sobre una sesión **ABIERTA**, cambiar el tema → guarda.
- [x] Sobre una sesión **CERRADA**, intentar editar → UI deshabilitada o backend 409.

### registrarTomaAsistencia()

- [x] Abrir la sesión ABIERTA del seed (`IYA040` de hoy) → lista de alumnos matriculados.
- [x] Marcar `alumno1` como PRESENTE, otro como AUSENTE, otro como JUSTIFICADO; guardar.
- [x] Recargar → los estados persisten.
- [x] Re-marcar `alumno1` como AUSENTE → sobrescribe (no duplica filas).

### cerrarSesionClase()

- [x] Clic en "Cerrar sesión" sobre la sesión activa → estado pasa a CERRADA.
- [x] La asistencia queda visible pero no editable.
- [x] Intentar cerrar de nuevo → error.

### exportarHistorialAsistencias()

- [x] En `/sesiones-clase`, seleccionar asignatura `IYA040` en el selector "Exportar:" y clic en exportar → descarga CSV con cabecera `sesion_id,fecha,grupos,aula,tema,alumno_id,alumno_nombre,estado`.
- [x] Probar M2 (filtro independiente): seleccionar `IYA041` en el filtro "Filtrar por asignatura" → tabla se reduce; comprobar que la exportación sigue usando el selector de exportar (independiente del filtro).

### consultarSolicitudDispensa() (Profesor)

- [x] `/dispensas` (vista Profesor) → solo las dispensas de asignaturas que imparte profesor1 (`IYA040`, `IYA041`) — 2 del seed.
- [x] La dispensa de `alumno1` en `IYA010` (asignatura no impartida por profesor1) **no aparece**.

---

## 8. Alumno (3 CUs)

Login como `alumno1 / alumno123`.

### consultarSolicitudDispensa() (Alumno)

- [x] `/dispensas` muestra solo sus 3 dispensas (las del seed).

### crearSolicitudDispensa() (Alumno)

- [x] Crear una dispensa nueva sobre `IYA020` (su única asignatura sin dispensa) con motivo "Test alumno".
- [x] El `<select>` de asignaturas **solo muestra las matriculadas** del alumno; no muestra ADE101 ni ADE202 (de alumno2).
- [x] Intenta crear otra sobre `IYA020` → error "ya existe solicitud para esta asignatura matriculada".

### editarSolicitudDispensa() (Alumno)

- [x] Editar la solicitud PENDIENTE recién creada → cambio persiste.
- [x] Intentar editar la dispensa APROBADA (`IYA010` del seed) → UI deshabilitada o 409.
- [x] Loguear como `alumno2` e intentar acceder por URL a una dispensa de `alumno1` → 403.

---

## 9. DirectorDeGrado (2 CUs)

Login como `director1 / director123` (INF).

### consultarSolicitudesDispensas()

- [x] `/dispensas` muestra **solo dispensas de INF**: las 3 de `alumno1` + posibles nuevas creadas en pruebas anteriores. **No aparece** la de `alumno2` (ADE).

### editarSolicitudDispensaDirector()

- [x] Editar la dispensa PENDIENTE de `alumno1`/`IYA040` → cambiar estado a APROBADA + añadir observaciones; guardar.
- [x] El `responsable_id` queda registrado como `director1`.
- [x] Sobre la dispensa APROBADA (la del seed con `IYA010`), editar de nuevo → permitido (no hay restricción de cierre para Director).

### Scoping cruzado

- [x] Cerrar sesión, loguear como `director2 / director123` (ADE).
- [x] `/dispensas` muestra **solo la dispensa de `alumno2`/`ADE101`** del seed.
- [x] La aprobación de director1 sobre INF **no es visible** para director2.

---

## 10. Cierre

- [x] Cerrar sesión final.
- [x] Detener `start.sh` con Ctrl+C → ambos procesos paran sin errores en el shell.
- [x] Re-lanzar `./scripts/start.sh` → seed re-aplicado idempotente, sin errores (bug `.unique()` zanjado el 2026-06-14).

---

## Resumen

Cobertura por rol al completar el guion:

| Rol               | CUs | Cubierto |
| ----------------- | :-: | :------: |
| Usuario           | 2   | 0,10     |
| Administrador     | 3   | 1        |
| Secretaria        | 12  | 2,3,4,5,6|
| Profesor          | 8   | 7        |
| Alumno            | 3   | 8        |
| DirectorDeGrado   | 2   | 9        |
| **Total**         | **30** | **0–10** |

Los CUs de "evolución post-base" (mejoras M1–M7 del [`PLAN-MEJORAS.md`](/RUP/PLAN-MEJORAS.md)) están repartidos en los bloques: M1 en 4 (consultarDetalleAlumno), M2/M3/M6 en 7 (sesiones), M4 en 4 (crearAlumno), M5 en 2/3 (catálogo asignaturas + asignar profesor), M7 en 2 + 9 (gestionarCatalogoGrados + scoping Director).
