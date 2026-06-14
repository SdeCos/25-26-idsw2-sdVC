# CGU > registrarTomaAsistencia > Diseño

> | [🏠️](/README.md) | [Diseño](/RUP/02-diseño/README.md) | [Detalle](/modelosUML/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Profesor/registrarTomaAsistencia.puml) | [Análisis](/RUP/01-analisis/casos-uso/registrarTomaAsistencia/README.md) | **Diseño** | Desarrollo |
> |-|-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Caso de uso**: `registrarTomaAsistencia()`
- **Actor**: Profesor
- **Versión**: 1.0
- **Fecha**: 2026-06-02

## diagrama de secuencia

<div align=center>

|![Secuencia registrarTomaAsistencia()](/images/RUP/02-diseño/casos-uso/registrarTomaAsistencia/secuencia.svg)|
|-|
|**Disciplina**: Diseño RUP<br>**Enfoque**: Diagrama de secuencia con tecnología concreta|

</div>

[Código PlantUML](/modelosUML/RUP/02-diseño/casos-uso/registrarTomaAsistencia/secuencia.puml)

El diagrama muestra la persistencia de **una sola marca**. La carga inicial del listado de alumnos matriculados se hace al montar la página activa (`GET /sesiones-clase/{id}/asistencias` retorna las ya registradas + se cruza con `consultarListaAlumnos` para mostrar los no marcados). El upsert se repite por cada cambio de estado del Profesor — modelar el loop sería ruido visual.

## participantes

| Participante | Rol |
|---|---|
| **SesionClaseActivaPage** (React, `/sesiones-clase/{id}`) | Lista de alumnos matriculados en la asignatura + radio/dropdown por fila (Presente/Ausente/Tarde) + textarea opcional de justificación. Cada cambio dispara una llamada al backend (persistencia granular, sin "submit final") |
| **asistenciasService** (axios) | Método nuevo `marcar(sesionId, alumnoId, datos)` |
| **AsistenciasRouter** (FastAPI) | Endpoint nuevo `PUT /sesiones-clase/{id}/asistencias/{alumno_id}` + `GET /sesiones-clase/{id}/asistencias` (listado para la carga inicial) |
| **require_rol** (dependency) | Autoriza `"profesor"` |
| **AsistenciaService** | Valida propietario + estado + matrícula del alumno; orquesta el upsert |
| **AsistenciaRepository** | Método `upsert(sesion_clase_id, alumno_id, estado, justificacion)` con `INSERT ... ON CONFLICT DO UPDATE` |
| **SQLite** | Tabla nueva `asistencias` (ver "entidad nueva") |

## materialización del análisis

| Mensaje del análisis | Materialización en diseño |
|---|---|
| `:Sesion Asistencia Abierta → RegistrarTomaAsistenciaView : registrarTomaAsistencia(sesion)` | El "modo toma" es la pantalla `/sesiones-clase/{id}` con la lista de alumnos visible. No hay activación explícita — pasar lista es el flujo principal de la sesión activa |
| `cargarAlumnosDeSesion(sesionId) : List<Alumno>` | `GET /sesiones-clase/{id}/asistencias` retorna asistencias persistidas + se completa con `GET /alumnos?asignatura_id={sesion.asignatura_id}` para alumnos no marcados |
| `obtenerPorAsignatura(asignatura) : List<Alumno>` | Reutiliza el endpoint del bloque alumnos del Profesor — ya introducido en [consultarListaAlumnos](/RUP/02-diseño/casos-uso/consultarListaAlumnos/README.md) |
| `registrarAsistencia(sesionId, alumnoId, estado, justificacion)` (mensaje 4, **repetido por alumno**) | `PUT /sesiones-clase/{id}/asistencias/{alumno_id}` — un PUT por cambio del Profesor |
| `guardar(asistencia)` upsert idempotente | `INSERT ... ON CONFLICT (sesion_clase_id, alumno_id) DO UPDATE SET estado, justificacion, fecha_registro` en una sola sentencia |

## decisiones de diseño

- **`Asistencia` debuta como entidad de dominio** — cierre de la deuda urgente del análisis. Tabla `asistencias` con columnas:
  - `id` PK
  - `sesion_clase_id` FK → `sesiones_clase.id`
  - `alumno_id` FK → `usuarios.id` (Alumno)
  - `estado` enum `EstadoAsistencia = {PRESENTE, AUSENTE, JUSTIFICADO}` (ver "evolución post-base 2026-06-14" al final)
  - `justificacion` string nullable
  - `fecha_registro` datetime (cuándo se marcó, ≠ fecha de la sesión)
  - **UNIQUE `(sesion_clase_id, alumno_id)`** — una marca por alumno y sesión, base del upsert idempotente del análisis
- **Endpoint `PUT /sesiones-clase/{id}/asistencias/{alumno_id}` (granular, idempotente)** — semántica HTTP correcta para upsert con identidad conocida (sesión + alumno = clave compuesta). El análisis adoptó granular sobre batch; el diseño lo respeta. Razones:
  - **Concurrencia trivial**: marcar dos veces seguidas al mismo alumno con estados distintos converge al último valor enviado (no race condition).
  - **UX honesta**: el prototipo no muestra botón "Guardar" final — cada interacción persiste.
  - **Sin endpoint batch** por ahora. Si la UX evoluciona a "marcar todos como Presente y luego corregir excepciones" (común), se añade `PUT /sesiones-clase/{id}/asistencias` con body batch. YAGNI.
- **Sub-recurso `/sesiones-clase/{id}/asistencias`** (no `/asistencias` plano) — refleja la jerarquía conceptual: la asistencia **pertenece a** una sesión de clase. Coherente con cómo `asignaturas_matriculadas` cuelga de `matriculas`. URL semántica honesta.
- **Verificación "Profesor competente" + propietario en el Service** — tres validaciones encadenadas:
  1. `sesion.profesor_id == current_user.id` (propietario, 403 `AsistenciaNoEditable`)
  2. `sesion.estado == ABIERTA` (no se marca asistencia en sesión cerrada, 422)
  3. `alumno_id` está matriculado en `sesion.asignatura_id` vía `AsignaturaMatriculada` (422, evita marcar a alumnos no matriculados)
  
  Tres validaciones honestas, errores distintos según causa.
- **Interacción `Asistencia` ↔ `SolicitudDispensa`: opción A del análisis** (independencia) — las dos entidades coexisten; la **vista** del listado las combina mostrando una columna "Dispensa" derivada cruzando `SolicitudDispensa.APROBADA` con `(alumno_id, asignatura_matriculada.asignatura_id)`. Razones:
  - No acopla las entidades a nivel persistencia (cambios en una no requieren cambios en otra).
  - La opción B (pre-marca automática) abriría la pregunta "¿se sobrescribe si el Profesor marca distinto?" sin respuesta clara del negocio.
  - La opción C (excluir del listado) ocultaría información útil al Profesor (los dispensados también deben pasar lista, solo que con marca prevista).
  
  La columna combinada vive en el frontend; el backend retorna `Asistencia` y `SolicitudDispensa` por separado en la carga inicial.
- **`enum EstadoAsistencia`** con 3 valores fijos (`PRESENTE`, `AUSENTE`, `JUSTIFICADO`). Ver "evolución post-base 2026-06-14" al final: el enum original era `{PRESENTE, AUSENTE, TARDE}` con la idea de que la justificación era un campo aparte; la evolución reemplaza `TARDE` por `JUSTIFICADO` con semántica explícita de "ausencia documentada que cuenta como presente para el umbral del 70%".
- **Sin auditoría adicional** (deuda del análisis: ¿quién marcó? ¿cuándo?) — el `fecha_registro` ya responde "cuándo". El "quién" es trivialmente `sesion.profesor_id` (gracias a la verificación de propietario). Sin columna `registrado_por_id` separada. YAGNI hasta que aparezca un caso (p.ej. Secretaria marca asistencia en nombre del Profesor).
- **Sin política de cierre temporal** (deuda del análisis) — la regla "no se marca tras cerrar" se materializa con la validación de estado. La pregunta "¿modificar dentro de ventana post-cierre?" queda fuera de scope (no hay reapertura).
- **Concurrencia** (deuda del análisis: dos pestañas del mismo Profesor) — el upsert por (sesion, alumno) es naturalmente idempotente. Último-en-escribir-gana, sin race condition destructiva.

## entidades nuevas introducidas en este CU

| Entidad | Capa | Notas |
|---|---|---|
| `Asistencia` | modelo SQLAlchemy `app/models/asistencia.py` | Tabla `asistencias` con UNIQUE compuesto |
| `EstadoAsistencia` | enum en el modelo | `PRESENTE`, `AUSENTE`, `JUSTIFICADO` |
| `AsistenciaIn`/`AsistenciaOut` | schema Pydantic `app/schemas/asistencias.py` | `AsistenciaIn` = `{estado, justificacion?}` (la sesión y el alumno van en path) |
| `AsistenciaService` | `app/services/asistencia_service.py` | `marcar`, `listar_por_sesion`. Excepciones `AsistenciaNoEditable`, `AlumnoNoMatriculado` |
| `AsistenciaRepository` | `app/repositories/asistencia_repository.py` | `upsert`, `listar_por_sesion`, `obtener_por_rango` (para el export) |

## sin Strategy `PoliticaAcceso` aquí

Aunque hay tres roles que podrían tocar `Asistencia` (Profesor marca, Alumno consulta, Secretaria potencial reporte), **solo el Profesor escribe**. El listado de asistencias de un alumno desde su propia ficha (futura extensión de `consultarDetalleAlumno`) tendría política de propiedad propia. Sin abstracción prematura — la Strategy se introduce cuando hay dos roles operando con políticas opuestas sobre la misma operación (lección consolidada del ramillete Alumno).

## evolución post-base — TARDE → JUSTIFICADO (2026-06-14)

Detectado durante las pruebas manuales pre-entrega: el enum `EstadoAsistencia` traía `{PRESENTE, AUSENTE, TARDE}`, pero `TARDE` ocupaba una zona ambigua — no contaba como `PRESENTE` para el % del 70% (la cuenta era `estado == PRESENTE`), y tampoco era una ausencia formal. Nadie lo usaba con sentido pedagógico claro.

**Cambio.** Reemplazado `TARDE` por `JUSTIFICADO`:
- **PRESENTE**: vino a clase.
- **JUSTIFICADO**: ausencia documentada (médica, viaje universitario, etc.). **Cuenta como `PRESENTE`** para el cálculo del porcentaje de asistencia — práctica académica estándar.
- **AUSENTE**: no vino, sin justificar.

`asistencia_repository.obtener_estadisticas_por_alumno` cambia su condición de conteo a `estado IN (PRESENTE, JUSTIFICADO)`. El comentario que ya decía "presente, ausente, justificado" pasa de aspiracional a literal.

**Decisión original revisada.** El diseño base separaba `estado` del campo `justificacion` ortogonalmente, con la idea de que `estado=AUSENTE + justificacion="..."` cubría el caso. La evolución reconoce que esto exigía al Profesor recordar la disciplina + escribir texto, sin afectar el % visible. `JUSTIFICADO` como estado **automatiza la consecuencia** (cuenta como presente) y deja `justificacion` como campo opcional de contexto, no como discriminador semántico.

**Migración aplicada.** `UPDATE asistencias SET estado='justificado' WHERE estado='tarde'` sobre la BD existente. Pendiente: en próximas iteraciones, evaluar si conviene exigir `justificacion` no-nula cuando `estado=JUSTIFICADO` (auditoría).

## referencias

- [Análisis `registrarTomaAsistencia()`](/RUP/01-analisis/casos-uso/registrarTomaAsistencia/README.md)
- [Diseño `crearSesionClase()` — entidad padre `SesionDeClase`](/RUP/02-diseño/casos-uso/crearSesionClase/README.md)
- [Diseño `consultarListaAlumnos()` (Profesor) — reutiliza `buscar_por_asignatura`](/RUP/02-diseño/casos-uso/consultarListaAlumnos/README.md)
- [Diseño `consultarDetalleAlumno()` (Profesor) — donde el campo `asistencias` se llenará](/RUP/02-diseño/casos-uso/consultarDetalleAlumno/README.md)
- [conversation-log.md](/conversation-log.md)
