# CGU > consultarListaAlumnos (Secretaria) > Diseño

> | [🏠️](/README.md) | [Diseño](/RUP/02-diseño/README.md) | [Detalle](/modelosUML/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Secretaria/consultarListaAlumnos.puml) | [Análisis](/RUP/01-analisis/casos-uso/consultarListaAlumnosSecretaria/README.md) | **Diseño** | Desarrollo |
> |-|-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Caso de uso**: `consultarListaAlumnos()` (Secretaria)
- **Actor**: Secretaria
- **Versión**: 1.0
- **Fecha**: 2026-06-01

> **Nota — scoping por grado.** Una revisión posterior restauró la entidad `Grado` del SDR. `GET /alumnos` ahora filtra por `matricula.grado_id == current_user.grado_id` cuando el `current_user.tipo == "secretaria"`. La cascada del scoping aplica también a `GET /matriculas` y `GET /dispensas` con el mismo filtro. El `AlumnoRepository.buscar_alumnos(...)` añade el WHERE; `AlumnoService` lo orquesta inyectando el grado del usuario. Estructura de la secuencia inalterada. Detalle en [[gestionarCatalogoGrados]].

## diagrama de secuencia

<div align=center>

|![Secuencia consultarListaAlumnos() Secretaria](/images/RUP/02-diseño/casos-uso/consultarListaAlumnosSecretaria/secuencia.svg)|
|-|
|**Disciplina**: Diseño RUP<br>**Enfoque**: Diagrama de secuencia con tecnología concreta|

</div>

[Código PlantUML](/modelosUML/RUP/02-diseño/casos-uso/consultarListaAlumnosSecretaria/secuencia.puml)

## participantes

| Participante | Rol |
|---|---|
| **AlumnosPage** (React, ruta `/alumnos`) | Tabla con paginador inferior + búsqueda libre arriba; columnas username, nombre, apellidos, email, acciones |
| **alumnosService** (axios) | Método `listar({page, size, q?})` |
| **AlumnosRouter** (FastAPI) | Endpoint `GET /alumnos?page&size&q` |
| **require_rol** (dependency) | Autoriza exigiendo `tipo == "secretaria"` |
| **UsuarioRepository** (extendido) | Estrena `buscar_alumnos(page, size, q) → (List[Alumno], total)` — filtra por `tipo='alumno'` y opcionalmente por `LIKE %q%` sobre `username/nombre/apellidos/email` |
| **SQLite** | Tabla `usuarios` (STI) |

## materialización del análisis

| Mensaje del análisis | Materialización en diseño |
|---|---|
| `:Listas Abierto → ConsultarListaAlumnosSecretariaView : consultarListaAlumnos()` | Click "Alumnos" en el menú de la Secretaria → navegación SPA a `/alumnos` |
| `ConsultarListaAlumnosSecretariaView → AlumnoController : cargarTodos() : List<Alumno>` | `GET /alumnos?page=&size=&q=` |
| `AlumnoController → AlumnoRepository : obtenerTodos() : List<Alumno>` | `UsuarioRepository.buscar_alumnos(page, size, q)` — filtro `tipo='alumno'` + paginación |
| Sin verificación de propiedad (la Secretaria es operadora global) | Solo `require_rol("secretaria")`. No defense-in-depth en el repositorio — la STI ya garantiza que solo devuelve `Alumno`. |

## decisiones de diseño

- **Sin capa de Service** — patrón consolidado del proyecto: los `consultar` read-only van Router → Repository directos (`consultarUsuario`, `consultarSolicitudDispensa`). Service solo donde hay reglas de negocio.
- **Paginación server-side desde el día 1**. El prototipo del SDR menciona "1-14 de 332 elementos, 24 páginas" — un listado realista de facultad supera los pocos cientos, devolverlo entero por defecto es despilfarro. Parámetros estándar `?page=1&size=25`; el Repository hace `LIMIT/OFFSET` y devuelve `(rows, total)` para que el paginador del frontend pinte "página X de Y".
- **Búsqueda libre `?q=`** sobre `username/nombre/apellidos/email` con `LIKE %q%` case-insensitive. El prototipo muestra un campo "Filtrar alumnos"; lo materializamos como búsqueda libre (no filtros multicolumna) por simplicidad. Filtros por grado/curso son deuda — emergerán cuando `Matricula` esté implementada (filtros por matriculación). Hoy `Alumno` no tiene esos campos en el modelo.
- **`UsuarioRepository.buscar_alumnos` en lugar de `obtener_todos`** — el método de la Secretaria es semánticamente distinto del genérico del Admin (`obtener_todos` retorna todos los `Usuario`s sin filtro), así que vive como método propio. Reutiliza la misma sesión SQLAlchemy.
- **Sin `obtener_todos_alumnos` por separado** — el método `buscar_alumnos` cubre el caso "listar todo" cuando `q=None` (no añade la cláusula `LIKE`). Una sola firma para los dos modos.
- **Sin defensa en profundidad en el Controller/Service**: la autorización vive en `require_rol` del router. Coherente con la decisión equivalente en `crearSolicitudDispensa` (Director). Si alguna vez se introduce un endpoint nuevo que reutilice `buscar_alumnos`, la autorización deberá redefinirse a ese nivel.
- **Schema de paginación reutilizable** `PaginaOut[T]` Pydantic genérica: `{items: List[T], total: int, page: int, size: int}`. Primer endpoint que pagina; se moverá a `app/schemas/paginacion.py` para reutilización futura (lista de matrículas, dispensas con filtros, etc.).

## schema de salida

`PaginaAlumnosOut` = `PaginaOut[AlumnoListaItemOut]` con:

```
AlumnoListaItemOut {
  id: int,
  username: str,
  nombre: str,
  apellidos: str,
  email: str,
  activo: bool,
}
```

Versión reducida de `UsuarioDetalleOut` (sin `tipo` ni metadatos que no se ven en la tabla — coherencia con el prototipo que solo muestra 5 columnas).

## referencias

- [Análisis `consultarListaAlumnos()` (Secretaria)](/RUP/01-analisis/casos-uso/consultarListaAlumnosSecretaria/README.md)
- [Análisis `consultarListaAlumnos()` (Profesor) — política contraria con filtro](/RUP/01-analisis/casos-uso/consultarListaAlumnos/README.md)
- [Diseño `consultarUsuario()` — patrón de consulta read-only](/RUP/02-diseño/casos-uso/consultarUsuario/README.md)
- [Detallado `consultarListaAlumnos.puml` (Secretaria)](/modelosUML/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Secretaria/consultarListaAlumnos.puml)
- [conversation-log.md](/conversation-log.md)
