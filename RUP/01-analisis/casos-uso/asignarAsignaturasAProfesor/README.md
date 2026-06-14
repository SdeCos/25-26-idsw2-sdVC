# CGU > asignarAsignaturasAProfesor > Análisis

> | [🏠️](/README.md) | [Análisis](/RUP/01-analisis/README.md) | Detalle | **Análisis** | Diseño | Desarrollo |
> |-|-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Construction
- **Disciplina**: Análisis
- **Caso de uso**: `asignarAsignaturasAProfesor()`
- **Actor**: Secretaria
- **Versión**: 1.0
- **Fecha**: 2026-06-11

## propósito

Análisis del caso de uso `asignarAsignaturasAProfesor()` mediante diagrama de colaboración MVC. La Secretaria gestiona qué asignaturas imparte cada profesor: para un profesor dado ve todas las asignaturas del catálogo, marca/desmarca cuáles imparte, y cada cambio se persiste en la relación N:M `profesor_asignaturas`.

Hoy la relación solo existe vía `seed.py` — no es editable en runtime. Este CU la lleva a estar gestionable.

Complementa a [[gestionarCatalogoAsignaturas]] (que opera sobre la entidad `Asignatura`), pero opera sobre una abstracción distinta: la **relación** entre `Profesor` y `Asignatura`, no sobre ninguna de las dos por separado.

## diagrama de colaboración

<div align=center>

|![Análisis asignarAsignaturasAProfesor()](/images/RUP/01-analisis/casos-uso/asignarAsignaturasAProfesor/colaboracion.svg)|
|-|
|**Disciplina**: Análisis RUP<br>**Enfoque**: Diagramas de colaboración MVC|

</div>


[Código PlantUML](/modelosUML/RUP/01-analisis/casos-uso/asignarAsignaturasAProfesor/colaboracion.puml)
## clases de análisis identificadas

### clases model (naranja #F2AC4E)

| Clase | Responsabilidad | Trazabilidad |
|-|-|-|
| **AsignaturaImpartida** | **Relación N:M reificada**: fila de `profesor_asignaturas` con `(profesor_id, asignatura_id, responsable_id)`. La elevamos a entidad de análisis por dos razones: (a) tiene atributos propios (`responsable_id`, auditoría), no es un simple par opaco; (b) la operación CRUD del CU es sobre la relación, no sobre `Profesor` ni `Asignatura` por separado | **Nueva**. El SDR no la modela explícitamente (la N:M aparece como flecha `Asignatura ↔ Profesor : Imparte`); este CU le da nombre para poder hablar de su ciclo de vida |
| **AsignaturaRepository** | Aporta el catálogo completo de asignaturas para pintar los checkboxes | Reutilizado de [[gestionarCatalogoAsignaturas]] |
| **UsuarioRepository** | Persiste las filas de `AsignaturaImpartida` (alta/baja) y lee las impartidas por un profesor | Reutilizado; estrena `crearImparte`, `eliminarImparte` y reutiliza el `obtenerImpartidas` ya existente para lectura |

`Profesor` y `Asignatura` aparecen implícitamente como referencias en `AsignaturaImpartida` — no se dibujan como cajas separadas para no inflar el diagrama; sus ciclos de vida los gestionan otros CUs ([[crearUsuario]] / [[gestionarCatalogoAsignaturas]]).

### clases view (azul #629EF9)

| Clase | Responsabilidad | Derivación |
|-|-|-|
| **AsignarAsignaturasProfesorView** | Pantalla con selector de profesor + lista de todas las asignaturas como checkboxes. Cada toggle dispara un `asignar`/`desasignar` inmediato (sin "guardar" final). Mensaje de feedback inline tras cada operación | Sin prototipo SALT; deriva del patrón "ficha de profesor" + sub-sección de asignaciones |

### clases controller (verde #b5bd68)

| Clase | Responsabilidad | Casos de uso |
|-|-|-|
| **UsuarioController** | Orquesta las operaciones sobre la relación porque conceptualmente operan sobre **un Profesor** (subtipo de `Usuario`): qué imparte, asignar, desasignar | Compartido con [[crearUsuario]], [[consultarUsuario]], [[editarUsuario]] — patrón "Controller por entidad" sobre `Usuario`. La extensión natural cuando la entidad gana relaciones gestionables |
| **AsignaturaController** | Aporta el listado del catálogo a la vista | Reutilizado de [[gestionarCatalogoAsignaturas]] |

### colaboraciones (verde claro #CDEBA5)

| Colaboración | Propósito | Invocación |
|-|-|-|
| **:Asignaciones Abierto** | Estado de origen — la Secretaria entra al apartado "Asignaciones de profesores" desde el menú y selecciona el profesor objetivo | Punto de entrada del caso de uso |

## mensajes de colaboración

### flujo principal

| # | Origen | Destino | Mensaje | Intención |
|-|-|-|-|-|
| 1 | **:Asignaciones Abierto** | **AsignarAsignaturasProfesorView** | `asignarAsignaturasAProfesor()` | Abrir la pantalla con un profesor seleccionado |
| 2 | **AsignarAsignaturasProfesorView** | **AsignaturaController** | `listar() : list<Asignatura>` | Cargar el catálogo completo para pintar los checkboxes |
| 3 | **AsignarAsignaturasProfesorView** | **UsuarioController** | `obtenerImpartidas(profesorId) : list<Asignatura>` | Cargar qué asignaturas ya imparte el profesor (checkboxes marcados) |
| 4 | **AsignarAsignaturasProfesorView** | **UsuarioController** | `asignar(profesorId, asignaturaId) : AsignaturaImpartida` | Toggle de un checkbox sin marcar → crear fila en la N:M |
| 5 | **AsignarAsignaturasProfesorView** | **UsuarioController** | `desasignar(profesorId, asignaturaId)` | Toggle de un checkbox marcado → eliminar fila de la N:M |
| 6 | **UsuarioController** | **UsuarioRepository** | `obtenerImpartidas / crearImparte / eliminarImparte (con validación)` | Persistencia. El Controller valida que el `usuarioId` corresponde a un Profesor antes de delegar |

### flujos alternativos

- **El usuario no es Profesor**: el Controller rechaza `asignar` y `desasignar` si el `usuarioId` corresponde a otro subtipo (alumno, director, secretaria, administrador). Defensa contra invocación cruzada.
- **Asignación duplicada**: si la fila `(profesor_id, asignatura_id)` ya existe, el Controller no la duplica (la operación es idempotente).
- **Asignatura inexistente**: si `asignaturaId` no existe, el Controller aborta con error.
- **Cerrar sin acción**: ningún toggle → no se llama a `asignar`/`desasignar`. Sin clase adicional.

## enlaces de dependencia

- **AsignarAsignaturasProfesorView** conoce a **AsignaturaController** (catálogo) y a **UsuarioController** (estado e mutación de la relación)
- **AsignaturaController** conoce a **AsignaturaRepository**
- **UsuarioController** conoce a **UsuarioRepository**
- **UsuarioRepository** conoce a **AsignaturaImpartida** (gestión de las filas de la N:M)
- **UsuarioController** conoce a **Sesion** (auditoría `responsable`; no dibujada — patrón "auto-poblado por Controller", igual que [[gestionarCatalogoAsignaturas]] y los imports masivos)

## decisiones de análisis

### la relación como entidad de análisis (`AsignaturaImpartida`)

Una relación N:M sin atributos extra suele dejarse como "flecha" entre dos entidades. Aquí la elevamos a clase de análisis porque le añadimos `responsable_id` y, conceptualmente, la operación del CU no es "editar un Profesor" ni "editar una Asignatura" — es **crear/eliminar la fila de relación**. Darle nombre permite hablar de su ciclo de vida y aterriza con naturalidad el método `crearImparte` en el repository.

Es el mismo movimiento que `Matricula` hace con la relación `Alumno ↔ Asignatura`: al ganar atributos (responsable, curso académico) deja de ser flecha y se vuelve entidad. La diferencia es que `Matricula` tiene mucho más estado; `AsignaturaImpartida` es ligera.

### CU separado de `gestionarCatalogoAsignaturas`

Discutido en el análisis del CU hermano: la operación no muta la entidad `Asignatura`, vive en una abstracción distinta (la relación), y el punto de entrada en la UI es el profesor, no el catálogo. Separarlos evita que `gestionarCatalogoAsignaturas` tenga que conocer a `Profesor` (y viceversa).

### UsuarioController como controller principal

La operación es semánticamente sobre **el Profesor**: "qué imparte X", "X pasa a impartir Y", "X deja de impartir Z". El sujeto gramatical es el profesor; la asignatura es el objeto. Por tanto el Controller natural es `UsuarioController` (el de la entidad-sujeto). `AsignaturaController` queda solo para aportar el catálogo de lectura — no muta nada.

Esta asimetría tiene precedente en el sistema: el Profesor es quien consulta sus alumnos por asignatura ([[consultarListaAlumnos]]) y quien crea sesiones de clase para sus asignaturas ([[crearSesionClase]]) — la asignatura es siempre objeto, no sujeto, de las operaciones del Profesor. Aquí la Secretaria sustituye al Profesor como actor que opera, pero la asimetría sujeto/objeto se preserva.

### toggle inmediato sin "guardar" final

Cada click en un checkbox dispara su mensaje (4 o 5). Sin botón "Guardar cambios" al final, sin estado intermedio "marcado pero no persistido". Razones:

- Cada toggle es atómico (una fila N:M, no transaccional con otras).
- Reduce la latencia mental: la Secretaria ve el efecto inmediato.
- Evita el problema "cierro la pestaña con cambios sin guardar".

Coste: si la red falla a mitad de un toggle, el checkbox visual debe revertirse. Decisión de UX para 02-diseño, no de análisis.

### auditoría con `responsable_id` en cada fila de la N:M

Cada `AsignaturaImpartida` lleva `responsable_id` apuntando a la Secretaria que hizo la asignación. Coherente con [[gestionarCatalogoAsignaturas]] e [[importarMatriculas]]. El `responsable_id` lo resuelve el Controller desde `Sesion.usuario` — auto-poblado, no entra como parámetro de la vista. En la desasignación no se conserva auditoría (la fila se elimina); si en el futuro se quisiera auditoría de baja, habría que mover a borrado lógico con `desasignadoPor` — registrado como deuda blanda, no se aplica ahora.

## trazabilidad con artefactos previos

### con el modelo del dominio

- **Relación `Asignatura ↔ Profesor : Imparte`** del SDR → la entidad `AsignaturaImpartida` con `responsable_id` la materializa para que sea gestionable en runtime.

### sin trazabilidad con detallados ni prototipos

- CU sin detallado ni prototipo en el SDR. Especificación canónica: este README.

## conexión con disciplinas rup

### desde requisitos

- **Modelo del dominio**: relación N:M `Imparte` — promovida a entidad gestionable.

### hacia diseño

- Tabla `profesor_asignaturas` SQL con PK compuesta `(profesor_id, asignatura_id)` y columna `responsable_id` FK.
- Endpoints REST sugeridos: `POST /usuarios/{profesor_id}/asignaturas-impartidas/{asignatura_id}` y `DELETE /usuarios/{profesor_id}/asignaturas-impartidas/{asignatura_id}`, protegidos por Secretaria. El path REST refleja que la operación es sobre la relación de un profesor concreto.
- Idempotencia del alta: `POST` repetido debe devolver 200 (o 201 la primera vez) sin duplicar. Decisión de diseño: capturar `IntegrityError` por PK compuesta y devolver 200.
- Validar en service que el `usuarioId` corresponde a tipo Profesor antes de delegar (defensa contra invocación cruzada).
- En frontend, dos llamadas de carga (catálogo + impartidas) pueden hacerse en paralelo. Posible composición a un único `GET /usuarios/{profesor_id}/asignaciones-vista` si la simplificación del cliente compensa el endpoint compuesto — alternativa a evaluar en diseño.

**Código fuente:** [colaboracion.puml](/modelosUML/RUP/01-analisis/casos-uso/asignarAsignaturasAProfesor/colaboracion.puml)

## referencias

- [Modelo del dominio (SDR)](/modelosUML/RUP/00-requisitos/ModeloDelDominio/DiagramasDeClase/ModeloCompleto.puml)
- [Análisis `gestionarCatalogoAsignaturas()`](/RUP/01-analisis/casos-uso/gestionarCatalogoAsignaturas/README.md) — CU complementario sobre la entidad
- [Análisis `crearUsuario()`](/RUP/01-analisis/casos-uso/crearUsuario/README.md) — `UsuarioController` reutilizado
- [Análisis `consultarListaAlumnos()`](/RUP/01-analisis/casos-uso/consultarListaAlumnos/README.md) — precedente de la asimetría Profesor-sujeto / Asignatura-objeto
- [conversation-log.md](/conversation-log.md)
