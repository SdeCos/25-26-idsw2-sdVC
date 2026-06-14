# CGU > gestionarCatalogoGrados > Diseño

> | [🏠️](/README.md) | [Diseño](/RUP/02-diseño/README.md) | Detalle | [Análisis](/RUP/01-analisis/casos-uso/gestionarCatalogoGrados/README.md) | **Diseño** | Desarrollo |
> |-|-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Construction
- **Disciplina**: Diseño
- **Caso de uso**: `gestionarCatalogoGrados()`
- **Actor**: Secretaria
- **Versión**: 1.0
- **Fecha**: 2026-06-10

## diagrama de secuencia

<div align=center>

|![Secuencia gestionarCatalogoGrados()](/images/RUP/02-diseño/casos-uso/gestionarCatalogoGrados/secuencia.svg)|
|-|
|**Disciplina**: Diseño RUP<br>**Enfoque**: Diagrama de secuencia con tecnología concreta — flujo de alta (operación más representativa del CU)|

</div>

[Código PlantUML](/modelosUML/RUP/02-diseño/casos-uso/gestionarCatalogoGrados/secuencia.puml)

## participantes

| Participante | Rol |
|---|---|
| **GradosPage** (React, ruta `/grados`) | Pantalla única: tabla del catálogo + sub-vistas para alta, edición y detalle. Modal o panel lateral; cierre vuelve al listado. |
| **gradosService** (axios) | Cliente HTTP para `/grados` (`listar`, `crear`, `actualizar`, `eliminar`) |
| **GradosRouter** (FastAPI) | Endpoints REST sobre `/grados` |
| **require_rol** (dependency) | Autoriza con `current_user.tipo == "secretaria"` |
| **GradoService** | Reglas de negocio: dedupe trivial en alta, `tieneReferencias` antes de eliminar |
| **GradoRepository** (SQLAlchemy) | I/O sobre tabla `grados` |
| **SQLite** | Tabla `grados` con `UNIQUE(codigo)` |

## materialización del análisis

El CU del análisis tiene cuatro operaciones (listar, crear, actualizar, eliminar). El diagrama muestra **alta** por ser la más representativa (única con validación de unicidad y posible 409). Las otras tres se materializan análogas, sobre los mismos participantes:

| Operación del análisis | Endpoint | Comentarios |
|-|-|-|
| `GradosView → GradoController : listar() : list<Grado>` | `GET /grados` → 200 + `list[GradoOut]` | Sin paginación (cardinalidad esperada baja, decenas como mucho). |
| `GradosView → GradoController : crear(codigo, nombre, facultad) : Grado` | `POST /grados` → 201 + `GradoOut` (o 409 si `codigo` en uso) | Diagrama de arriba. |
| `GradosView → GradoController : actualizar(id, cambios) : Grado` | `PATCH /grados/{id}` → 200 + `GradoOut` (o 404) | Solo `nombre` y `facultad` editables. `codigo` rechazado por `extra="ignore"` en el schema. |
| `GradosView → GradoController : eliminar(id)` | `DELETE /grados/{id}` → 204 (o 409 si tiene referencias, 404 si no existe) | Validación en service antes del DELETE; el cuerpo del 409 indica qué tipo de referencia bloquea (matrículas / asignaturas / directores / secretarias). |
| Choice point "código en uso" al alta | `IntegrityError` capturado en service → `CodigoEnUso` → 409 | Mismo patrón que `crearUsuario` con `username` — la BD es la autoridad. |
| Choice point "borrado con referencias" | `GradoService.eliminar` consulta `tieneReferencias` y aborta con `GradoConReferencias` → 409 | A diferencia del alta (delegamos al `UNIQUE` de BD), la validación de referencias no es directamente expresable como constraint que la BD reporte de forma útil; se hace explícita en service. |

## decisiones de diseño

- **CU agregado en un único endpoint base `/grados`** — el análisis modela el CU como una unidad (operación administrativa de catálogo). El diseño lo respeta: cuatro verbos HTTP sobre el mismo recurso. Pattern REST estándar. No se separan en routers distintos como ocurre con `usuarios` (un único `UsuariosRouter` también cubre POST/PATCH/GET/DELETE).
- **`GradoService` aunque la lógica sea fina** — coherencia con el split del bloque Usuario (`UsuariosRouter → UsuarioService → UsuarioRepository`). El service hoy hace poco (delega a repo), pero cuando se añada `eliminar` con `tieneReferencias` o reglas adicionales (p.ej. no permitir cambiar `codigo`), tener el sitio ya armado evita refactorizar el router. Mismo precedente que `AsistenciaService` cuando solo orquestaba un upsert.
- **Validación de unicidad sin pre-check** — el `UNIQUE(codigo)` de la BD ya es autoridad. Una sola llamada `POST` con captura de `IntegrityError` → 409, mismo patrón que `crearUsuario` con `username`. Sin endpoint `check-codigo` separado.
- **Validación de referencias en service, no en BD** — las FKs de `matriculas`, `asignaturas`, `usuarios` (Director/Secretaria) hacia `grados` se configuran como `RESTRICT` (no `CASCADE`). El service comprueba primero con `tieneReferencias(grado_id)` y devuelve un 409 con detalle del tipo de referencia. Capturar el `IntegrityError` del FK funcionaría, pero el mensaje sería opaco — la validación explícita en service permite el detalle.
- **`codigo` no editable post-creación** — análogo a `username` en usuarios. El `EditarGradoRequest` solo declara `nombre` y `facultad`; un `codigo` enviado se descarta por `extra="ignore"`.
- **`require_rol(["secretaria"])` sin scoping** — caso especial: el catálogo es global, cualquier Secretaria puede mantenerlo. Decisión documentada en el análisis y justificada por el bootstrap problem (sin esta excepción, una Secretaria nueva no podría dar de alta su propio grado). El `require_rol` no necesita variante "any-grado" — basta con el rol.
- **`GradosPage` única con sub-vistas en lugar de `/grados/nuevo`, `/grados/{id}`, `/grados/{id}/editar`** — el catálogo es plano y operativamente menor. Múltiples rutas serían sobrediseño; un único `GradosPage` con modal/panel para alta/edición es coherente con cómo se trata el CRUD plano en frontends ligeros. Contrasta con `usuarios`, donde las sub-rutas se justifican por la edición compleja (multitud de campos por subtipo) — aquí solo hay tres campos.

## referencias

- [Análisis `gestionarCatalogoGrados()`](/RUP/01-analisis/casos-uso/gestionarCatalogoGrados/README.md)
- [Diseño `crearUsuario()`](/RUP/02-diseño/casos-uso/crearUsuario/README.md) — patrón de validación de unicidad
- [Modelo del dominio (SDR)](/modelosUML/RUP/00-requisitos/ModeloDelDominio/DiagramasDeClase/ModeloCompleto.puml)
- [conversation-log.md](/conversation-log.md)
