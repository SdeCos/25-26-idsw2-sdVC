# CGU > importarListasAlumnos > Desarrollo

> | [🏠️](/README.md) | [Desarrollo](/RUP/03-desarrollo/README.md) | [Análisis](/RUP/01-analisis/casos-uso/importarListasAlumnos/README.md) | [Diseño](/RUP/02-diseño/casos-uso/importarListasAlumnos/README.md) | **Desarrollo** |
> |-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Construcción
- **Disciplina**: Desarrollo
- **Caso de uso**: `importarListasAlumnos()`
- **Actor**: Secretaria
- **Versión**: 1.0
- **Fecha**: 2026-06-01

## trazabilidad código ↔ diseño

| Participante del diseño | Implementación |
|---|---|
| ImportarListasAlumnosPage (`/alumnos/importar`) | [src/frontend/src/pages/ImportarListasAlumnosPage.tsx](/src/frontend/src/pages/ImportarListasAlumnosPage.tsx) |
| alumnosService.importar | [src/frontend/src/services/alumnosService.ts](/src/frontend/src/services/alumnosService.ts) |
| Gate `secretariaOnly` | [src/frontend/src/App.tsx](/src/frontend/src/App.tsx) |
| AlumnosRouter (`POST /alumnos/importar`) | [src/backend/app/routers/alumnos.py](/src/backend/app/routers/alumnos.py) |
| AlumnoService.importar | [src/backend/app/services/alumno_service.py](/src/backend/app/services/alumno_service.py) |
| ValidadorArchivoListasAlumnos | [src/backend/app/services/validador_archivo_listas_alumnos.py](/src/backend/app/services/validador_archivo_listas_alumnos.py) |
| UsuarioRepository.upsert_lote_alumnos | [src/backend/app/repositories/usuario_repository.py](/src/backend/app/repositories/usuario_repository.py) |
| Schema `InformeImportacionAlumnosOut` + `ErrorImportacionOut` | [src/backend/app/schemas/paginacion.py](/src/backend/app/schemas/paginacion.py) |

## verificación end-to-end

Validado vía `curl` contra `localhost:8000` con un CSV de 3 filas (2 válidas + 1 fila con campo `nombre` vacío):

| Escenario | Resultado |
|---|---|
| `POST /alumnos/importar` sin token | 401 |
| Mismo endpoint con token de Alumno | 403 |
| Mismo endpoint con token de Secretaria + CSV | 200 `{creados: 2, actualizados: 0, errores: [{archivo, fila: 4, mensaje: "campo 'nombre' obligatorio"}]}` |
| Re-importar el mismo CSV | 200 `{creados: 0, actualizados: 2, errores: [...]}` — upsert sin tocar password |

## decisiones materializadas

- **`UsuarioRepository.upsert_lote_alumnos`** dentro del repo existente (no se crea `AlumnoRepository` aparte porque la STI lo haría wrapper trivial). Update sin tocar `password_hash` si el alumno ya existe.
- **Validador con `CabeceraInvalida` como excepción** → 422 a nivel router; errores de fila → al informe (best-effort).
- **`hash_password` de `core/security`** se usa en `AlumnoService`, no en `UsuarioRepository`.

## referencias

- [Análisis](/RUP/01-analisis/casos-uso/importarListasAlumnos/README.md)
- [Diseño](/RUP/02-diseño/casos-uso/importarListasAlumnos/README.md)
- [conversation-log.md](/conversation-log.md)
