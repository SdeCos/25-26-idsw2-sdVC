# CGU > gestionarCatalogoGrados > Desarrollo

> | [🏠️](/README.md) | [Desarrollo](/RUP/03-desarrollo/README.md) | [Análisis](/RUP/01-analisis/casos-uso/gestionarCatalogoGrados/README.md) | [Diseño](/RUP/02-diseño/casos-uso/gestionarCatalogoGrados/README.md) | **Desarrollo** |
> |-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Construcción
- **Disciplina**: Desarrollo
- **Caso de uso**: `gestionarCatalogoGrados()`
- **Actor**: Secretaria
- **Versión**: 1.0
- **Fecha**: 2026-06-10

## trazabilidad código ↔ diseño

| Participante del diseño | Implementación |
|---|---|
| GradosPage (`/grados`) | [src/frontend/src/pages/GradosPage.tsx](/src/frontend/src/pages/GradosPage.tsx) |
| gradosService (`listar`, `crear`, `actualizar`, `eliminar`) | [src/frontend/src/services/gradosService.ts](/src/frontend/src/services/gradosService.ts) |
| Tipos DTO (`Grado`, `CrearGradoRequest`, `EditarGradoRequest`) | [src/frontend/src/types/grados.ts](/src/frontend/src/types/grados.ts) |
| Ruta gated `secretariaOnly` | [src/frontend/src/App.tsx](/src/frontend/src/App.tsx) |
| Enlace "Grados" en el nav de Secretaria | [src/frontend/src/components/Layout.tsx](/src/frontend/src/components/Layout.tsx) |
| GradosRouter (CRUD bajo `/grados`) | [src/backend/app/routers/grados.py](/src/backend/app/routers/grados.py) |
| require_rol (dependency) | [src/backend/app/dependencies.py](/src/backend/app/dependencies.py) (reutilizado) |
| GradoService (CRUD + `referencias` antes de borrar) | [src/backend/app/services/grado_service.py](/src/backend/app/services/grado_service.py) |
| Excepciones `CodigoEnUso`, `GradoNoEncontrado`, `GradoConReferencias` | [src/backend/app/services/grado_service.py](/src/backend/app/services/grado_service.py) |
| GradoRepository (I/O sobre tabla `grados`) | [src/backend/app/repositories/grado_repository.py](/src/backend/app/repositories/grado_repository.py) |
| Modelo `Grado` (id, codigo único, nombre, facultad) | [src/backend/app/models/grado.py](/src/backend/app/models/grado.py) |
| Schemas `GradoOut`, `CrearGradoRequest`, `EditarGradoRequest` | [src/backend/app/schemas/grados.py](/src/backend/app/schemas/grados.py) |
| FKs `Asignatura.grado_id`, `Matricula.grado_id`, `Usuario.grado_id` (Director) | [src/backend/app/models/asignatura.py](/src/backend/app/models/asignatura.py), [matricula.py](/src/backend/app/models/matricula.py), [usuario.py](/src/backend/app/models/usuario.py) |
| Seed con dos grados (INF, ADE) | [src/backend/scripts/seed.py](/src/backend/scripts/seed.py) |

## divergencias respecto al diseño

| Diseño | Implementación | Motivo |
|---|---|---|
| `PoliticaSecretaria` aplica cascada de scoping por grado (dispensas, alumnos, matrículas) | Solo `PoliticaDirector` está scopeada; `PoliticaSecretaria` queda global (Secretaría sin grado) | Revisión lingüística del SDR durante implementación: `Grado --> SecretariaAcademica : Gestionado por` se lee como "gestionado por (el departamento de) Secretaría Académica", no por una secretaria nombrada. Coherente con `Dispensa --> SecretariaAcademica : Gestionada por`. El Director sí mantiene el scoping (relación 1:1 con identidad). Schema `CrearUsuarioRequest` materializa la asimetría: `_ROLES_CON_GRADO = {"director"}`. |

El resto de decisiones del diseño se preserva: catálogo global (sin scoping en el propio `/grados`), validación de unicidad sin pre-check (`UNIQUE(codigo)` + `IntegrityError` → 409), validación de referencias en service antes del `DELETE`, `codigo` no editable post-creación, único `GradosPage` con sub-vistas inline.

## verificación end-to-end

Validado vía `curl` contra `localhost:8000`:

| Escenario | Resultado |
|---|---|
| `GET /grados` como Secretaria | 200 + `[GradoOut]` con INF y ADE del seed |
| `POST /grados {codigo:"INF"}` (duplicado) | 409 "Código de grado en uso" |
| `POST /grados {codigo:"MED", nombre:"Medicina", facultad:"…"}` | 201 + `GradoOut` |
| `DELETE /grados/{id}` con referencias | 409 con detalle `["asignaturas","matriculas","usuarios"]` |
| `POST /usuarios {tipo:"director"}` sin `grado_id` | 422 (validador `_grado_id_obligatorio_para_director`) |
| `director1` (INF) ve solo sus 3 dispensas; `director2` (ADE) ve 1 | filtrado por grado funciona |
| `secretaria1` (sin grado) ve todos los alumnos, matrículas y dispensas | departamento colectivo, sin scoping |

Validación a nivel navegador realizada en su día (alta/edición/borrado de grado, mensajes 409 inline, selector de grado en `CrearUsuarioPage`/`EditarUsuarioPage` solo visible cuando `tipo === 'director'`).

## referencias

- [Análisis](/RUP/01-analisis/casos-uso/gestionarCatalogoGrados/README.md)
- [Diseño](/RUP/02-diseño/casos-uso/gestionarCatalogoGrados/README.md)
- [Modelo del dominio (SDR)](/modelosUML/RUP/00-requisitos/ModeloDelDominio/DiagramasDeClase/ModeloCompleto.puml)
- [Desarrollo `crearUsuario()`](/RUP/03-desarrollo/casos-uso/crearUsuario/README.md) — precedente del patrón router/service/repository con `UNIQUE` + 409
- [conversation-log.md](/conversation-log.md)
