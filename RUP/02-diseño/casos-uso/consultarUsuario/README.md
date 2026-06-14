# CGU > consultarUsuario > Diseño

> | [🏠️](/README.md) | [Diseño](/RUP/02-diseño/README.md) | [Detalle](/modelosUML/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Administrador/consultarUsuario.puml) | [Análisis](/RUP/01-analisis/casos-uso/consultarUsuario/README.md) | **Diseño** | Desarrollo |
> |-|-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Caso de uso**: `consultarUsuario()`
- **Actor**: Administrador
- **Versión**: 1.0
- **Fecha**: 2026-05-30

## diagrama de secuencia

<div align=center>

|![Secuencia consultarUsuario()](/images/RUP/02-diseño/casos-uso/consultarUsuario/secuencia.svg)|
|-|
|**Disciplina**: Diseño RUP<br>**Enfoque**: Diagrama de secuencia con tecnología concreta|

</div>

[Código PlantUML](/modelosUML/RUP/02-diseño/casos-uso/consultarUsuario/secuencia.puml)

## participantes

| Participante | Rol |
|---|---|
| **ConsultarUsuarioPage** (React, ruta `/usuarios/{id}`) | Ficha read-only del usuario; render condicional por subtipo |
| **usuariosService** (axios) | Cliente HTTP, método `obtener(id)` |
| **UsuariosRouter** (FastAPI) | Endpoint `GET /usuarios/{id}` |
| **require_rol** (dependency) | Autoriza exigiendo `current_user.tipo == "administrador"` |
| **UsuarioRepository** (SQLAlchemy) | `obtener_por_id(id)` con resolución polimórfica del subtipo (ya existía desde iniciarSesion) |
| **SQLite** | Tabla `usuarios` (STI con discriminator `tipo`) |

## materialización del análisis

| Mensaje del análisis | Materialización en diseño |
|---|---|
| `:Usuarios Abierto → ConsultarUsuarioView : consultarUsuario(usuarioId)` | Navegación SPA a `/usuarios/{id}` desde `UsuariosPage` (no representada en la secuencia — UI fuera del scope del CU) |
| `ConsultarUsuarioView → UsuarioController : cargarUsuario(usuarioId)` | `usuariosService.obtener(id)` → `GET /usuarios/{id}` |
| `UsuarioController → UsuarioRepository : obtenerPorId(usuarioId)` | `UsuarioRepository.obtener_por_id(id)` (mismo método ya en uso desde iniciarSesion) |
| `<<include>> editarUsuario(usuarioId)` (opcional) | Botón "Editar" en la ficha → `navigate("/usuarios/{id}/editar")`. Transición de navegación, no incluida en la secuencia. |
| Subtipo invariante durante la lectura | `UsuarioOut` lleva el campo `tipo`; el frontend ramifica el render condicional sin un GET extra |

## decisiones de diseño

- **Sin `UsuarioService` intermedio en la lectura** — `Router → Repository` directo. El análisis tenía un `UsuarioController` orquestando, pero para una operación read-only sin reglas de negocio una capa Service sería un thin pass-through sin valor. Decisión inversa al `crearUsuario` (que sí necesita hash de contraseña).
- **404 honesto, sin filtros silenciosos** — el repositorio devuelve `None` si el id no existe; el router lo traduce a `HTTP 404`. El frontend renderiza un estado de error claro, no una ficha vacía. Coherente con el principio de no enmascarar errores.
- **Endpoint complementario `GET /usuarios` para el listado** — fuera de la secuencia (el CU del análisis es la ficha individual), pero necesario para que la `UsuariosPage` exista. Se implementa en el mismo router; `UsuarioRepository.obtener_todos() : list[Usuario]` es trivial. Sin paginación por ahora — el detallado no lo exige y los volúmenes esperados son bajos.
- **Render condicional por subtipo en cliente** — el `UsuarioOut` lleva `tipo`; el componente React decide qué campos extra mostrar (`Profesor.departamento`, `Alumno.matricula`, …) cuando esos campos existan en el modelo. Hoy el `UsuarioOut` solo tiene los campos comunes; el render condicional queda como punto de extensión documentado, no como código aún.
- **`require_rol(["administrador"])` reutilizado** — misma dependency que en `crearUsuario`. Patrón consolidado: la autorización vive como dependency a nivel de endpoint, no embebida en el código del handler.

## referencias

- [Análisis `consultarUsuario()`](/RUP/01-analisis/casos-uso/consultarUsuario/README.md)
- [Detallado `consultarUsuario()`](/modelosUML/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Administrador/consultarUsuario.puml)
- [Prototipo SALT `consultarUsuario1.png`](/images/RUP/00-requisitos/CasosDeUso/Prototipos/Administrador/consultarUsuario1.png)
- [Diseño `crearUsuario()`](/RUP/02-diseño/casos-uso/crearUsuario/README.md)
- [conversation-log.md](/conversation-log.md)
