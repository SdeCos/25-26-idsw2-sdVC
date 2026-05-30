# CGU > consultarUsuario > Desarrollo

> | [🏠️](/README.md) | [Desarrollo](/RUP/03-desarrollo/README.md) | [Análisis](/RUP/01-analisis/casos-uso/consultarUsuario/README.md) | [Diseño](/RUP/02-diseño/casos-uso/consultarUsuario/README.md) | **Desarrollo** |
> |-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Construcción
- **Disciplina**: Desarrollo
- **Caso de uso**: `consultarUsuario()`
- **Actor**: Administrador
- **Versión**: 1.0
- **Fecha**: 2026-05-30

## trazabilidad código ↔ diseño

| Participante del diseño | Implementación |
|---|---|
| ConsultarUsuarioPage (`/usuarios/{id}`) | [src/frontend/src/pages/ConsultarUsuarioPage.tsx](/src/frontend/src/pages/ConsultarUsuarioPage.tsx) |
| UsuariosPage (listado `:Usuarios Abierto`) | [src/frontend/src/pages/UsuariosPage.tsx](/src/frontend/src/pages/UsuariosPage.tsx) |
| usuariosService.obtener + listar | [src/frontend/src/services/usuariosService.ts](/src/frontend/src/services/usuariosService.ts) |
| UsuariosRouter (`GET /usuarios`, `GET /usuarios/{id}`) | [src/backend/app/routers/usuarios.py](/src/backend/app/routers/usuarios.py) |
| UsuarioRepository.obtener_todos + obtener_por_id | [src/backend/app/repositories/usuario_repository.py](/src/backend/app/repositories/usuario_repository.py) |
| Schema `UsuarioDetalleOut` | [src/backend/app/schemas/usuarios.py](/src/backend/app/schemas/usuarios.py) |

`UsuarioService` **no participa** en este CU — `Router → Repository` directo, como dictaba el diseño (lectura sin lógica de negocio).

## verificación end-to-end

Validado vía `curl` contra `localhost:8000`:

| Escenario | Resultado |
|---|---|
| `GET /usuarios` con token de admin | 200 + lista de 6 `UsuarioDetalleOut` (5 seed + 1 creado en prueba) |
| `GET /usuarios` con token de `alumno1` | 403 |
| `GET /usuarios/6` con token de admin | 200 + ficha completa |
| `GET /usuarios/9999` | 404 `Usuario no encontrado` |

Render condicional por subtipo en el cliente: por ahora `UsuarioDetalleOut` solo lleva campos comunes; el `tipo` se muestra como badge de color (alumno/profesor/director/secretaria/administrador) pero no hay campos específicos por subtipo todavía. Punto de extensión documentado para cuando el modelo del dominio incorpore `Profesor.departamento`, `Alumno.matricula`, etc.

## referencias

- [Análisis](/RUP/01-analisis/casos-uso/consultarUsuario/README.md)
- [Diseño](/RUP/02-diseño/casos-uso/consultarUsuario/README.md)
- [conversation-log.md](/conversation-log.md)
