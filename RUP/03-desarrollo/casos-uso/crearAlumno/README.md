# CGU > crearAlumno > Desarrollo

> | [🏠️](/README.md) | [Desarrollo](/RUP/03-desarrollo/README.md) | [Análisis](/RUP/01-analisis/casos-uso/crearAlumno/README.md) | [Diseño](/RUP/02-diseño/casos-uso/crearAlumno/README.md) | **Desarrollo** |
> |-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Construcción
- **Disciplina**: Desarrollo
- **Caso de uso**: `crearAlumno()`
- **Actor**: Secretaria
- **Versión**: 1.0
- **Fecha**: 2026-06-11

## trazabilidad código ↔ diseño

| Participante del diseño | Implementación |
|---|---|
| CrearAlumnoPage (`/alumnos/nuevo`) | [src/frontend/src/pages/CrearAlumnoPage.tsx](/src/frontend/src/pages/CrearAlumnoPage.tsx) |
| alumnosService.crear | [src/frontend/src/services/alumnosService.ts](/src/frontend/src/services/alumnosService.ts) |
| Tipos DTO (`CrearAlumnoRequest`) | [src/frontend/src/types/alumnos.ts](/src/frontend/src/types/alumnos.ts) |
| Ruta gated `secretariaOnly` | [src/frontend/src/App.tsx](/src/frontend/src/App.tsx) |
| Botón "+ Nuevo alumno" visible solo a Secretaria | [src/frontend/src/pages/AlumnosPage.tsx](/src/frontend/src/pages/AlumnosPage.tsx) |
| Quitar `alumno` del select de `CrearUsuarioPage` | [src/frontend/src/pages/CrearUsuarioPage.tsx](/src/frontend/src/pages/CrearUsuarioPage.tsx) |
| AlumnosRouter (`POST /alumnos`) | [src/backend/app/routers/alumnos.py](/src/backend/app/routers/alumnos.py) |
| Schema `CrearAlumnoRequest` | [src/backend/app/schemas/alumnos.py](/src/backend/app/schemas/alumnos.py) |
| Rechazo 422 de `tipo=alumno` en `POST /usuarios` | [src/backend/app/routers/usuarios.py](/src/backend/app/routers/usuarios.py) |
| `UsuarioService.crear` reutilizado | [src/backend/app/services/usuario_service.py](/src/backend/app/services/usuario_service.py) (sin cambios) |
| `UsuarioRepository.crear` reutilizado | [src/backend/app/repositories/usuario_repository.py](/src/backend/app/repositories/usuario_repository.py) (sin cambios) |

## divergencias respecto al diseño

| Diseño | Implementación | Motivo |
|---|---|---|
| `DatosPersonalesAlumno` materializa los 4 campos personales del análisis (nombre, apellidos, email, teléfono) | El schema `CrearAlumnoRequest` lleva solo 3 (nombre, apellidos, email); no hay teléfono | El modelo `Usuario` actual no tiene columna `telefono`. Añadirla excede el alcance de este CU (cambio de esquema, migración, propagación a otras vistas). Si en el futuro se incorpora, basta con extender el schema. La firma del request sigue siendo más limpia que la "Long Parameter List" original (5 params vs 6). |

Todas las decisiones de fondo del diseño se conservan:
- **Canal HTTP separado**: `POST /alumnos` (Secretaria) y `POST /usuarios` (Administrador) son endpoints distintos. `POST /usuarios` rechaza explícitamente `tipo="alumno"` con 422.
- **`UsuarioService.crear` reutilizado** con `tipo="alumno"` fijado por el router. El polimorfismo de instanciación se mantiene single-source en `UsuarioRepository.crear`.
- **409 por `UNIQUE(username)`** con captura de `IntegrityError`, mismo patrón que `crearUsuario` / `gestionarCatalogoGrados`.
- **Doble defensa cliente+servidor**: la opción `alumno` se retira del `<select>` de tipo en `CrearUsuarioPage`; el backend rechaza por si acaso.

## verificación end-to-end

Validado vía `curl` contra `localhost:8000` con `secretaria1` (sin grado, departamento colectivo) y `admin`:

| Escenario | Resultado |
|---|---|
| `POST /alumnos` con token de `secretaria1` + datos válidos | 201 + `UsuarioDetalleOut` (`tipo: "alumno"`, `grado: null`) |
| `POST /alumnos` con `username` duplicado | 409 `El username ya está en uso` |
| `POST /alumnos` con token de `admin` | 403 `No autorizado para esta operación` |
| `POST /usuarios` con token de `admin` + `tipo="alumno"` | 422 `El alta de alumno corresponde a Secretaría (POST /alumnos).` |
| `POST /usuarios` con token de `admin` + `tipo="profesor"` | 201 (no regresión: el alta de personal sigue funcionando) |
| `GET /alumnos?q=alumno9` | el alumno recién creado aparece en el listado |

Validación a nivel navegador (login como Secretaria → `/alumnos` → botón "+ Nuevo alumno" → form → submit → redirect a `/alumnos`) pendiente de ejecución manual.

## referencias

- [Análisis](/RUP/01-analisis/casos-uso/crearAlumno/README.md)
- [Diseño](/RUP/02-diseño/casos-uso/crearAlumno/README.md)
- [Desarrollo `crearUsuario()`](/RUP/03-desarrollo/casos-uso/crearUsuario/README.md) — patrón espejado
- [conversation-log.md](/conversation-log.md)
