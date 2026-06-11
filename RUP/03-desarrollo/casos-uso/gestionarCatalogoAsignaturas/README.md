# CGU > gestionarCatalogoAsignaturas > Desarrollo

> | [🏠️](/README.md) | [Desarrollo](/RUP/03-desarrollo/README.md) | [Análisis](/RUP/01-analisis/casos-uso/gestionarCatalogoAsignaturas/README.md) | [Diseño](/RUP/02-diseño/casos-uso/gestionarCatalogoAsignaturas/README.md) | **Desarrollo** |
> |-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Construcción
- **Disciplina**: Desarrollo
- **Caso de uso**: `gestionarCatalogoAsignaturas()`
- **Actor**: Secretaria
- **Versión**: 1.0
- **Fecha**: 2026-06-11

## trazabilidad código ↔ diseño

| Participante del diseño | Implementación |
|---|---|
| AsignaturasPage (`/asignaturas`) | [src/frontend/src/pages/AsignaturasPage.tsx](/src/frontend/src/pages/AsignaturasPage.tsx) |
| asignaturasService (`listar`, `crear`, `actualizar`, `eliminar`) | [src/frontend/src/services/asignaturasService.ts](/src/frontend/src/services/asignaturasService.ts) |
| Tipos DTO (`Asignatura`, `CrearAsignaturaRequest`, `EditarAsignaturaRequest`) | [src/frontend/src/types/asignaturas.ts](/src/frontend/src/types/asignaturas.ts) |
| Ruta gated `secretariaOnly` + link "Asignaturas" en el nav | [src/frontend/src/App.tsx](/src/frontend/src/App.tsx), [src/frontend/src/components/Layout.tsx](/src/frontend/src/components/Layout.tsx) |
| AsignaturasRouter (`POST`, `GET /{id}`, `PATCH /{id}`, `DELETE /{id}`) | [src/backend/app/routers/asignaturas.py](/src/backend/app/routers/asignaturas.py) |
| AsignaturaService (pre-validación de `grado_id`, `referencias`, resolución de `responsable_id`) | [src/backend/app/services/asignatura_service.py](/src/backend/app/services/asignatura_service.py) |
| Excepciones `CodigoEnUso`, `AsignaturaNoEncontrada`, `GradoNoEncontrado`, `AsignaturaConReferencias` | [src/backend/app/services/asignatura_service.py](/src/backend/app/services/asignatura_service.py) |
| AsignaturaRepository (`crear`, `actualizar`, `eliminar`, `referencias`) | [src/backend/app/repositories/asignatura_repository.py](/src/backend/app/repositories/asignatura_repository.py) |
| Modelo `Asignatura.responsable_id` añadido + `grados: list[Grado]` vía N:M (cardinalidad 1 → N) | [src/backend/app/models/asignatura.py](/src/backend/app/models/asignatura.py) |
| Tabla N:M `asignatura_grados` | [src/backend/app/models/asignatura_grado.py](/src/backend/app/models/asignatura_grado.py) |
| Schemas `CrearAsignaturaRequest.grado_ids: list[int] (min_length=1)`, `EditarAsignaturaRequest.grado_ids` | [src/backend/app/schemas/asignaturas.py](/src/backend/app/schemas/asignaturas.py) |
| `PoliticaDirector` adaptada (`director.grado_id in {g.id for g in asignatura.grados}`) + `SolicitudDispensaRepository.obtener_por_grado` (JOIN por la N:M) | [src/backend/app/services/politica_acceso.py](/src/backend/app/services/politica_acceso.py), [src/backend/app/repositories/solicitud_dispensa_repository.py](/src/backend/app/repositories/solicitud_dispensa_repository.py) |
| Seed que atribuye las asignaturas iniciales a `secretaria1` | [src/backend/scripts/seed.py](/src/backend/scripts/seed.py) |

## divergencias respecto al diseño

| Diseño | Implementación | Motivo |
|---|---|---|
| `responsable_id` `NOT NULL` en el modelo | `Mapped[int \| None]` (nullable) | Las asignaturas pre-existentes del seed se asocian a `secretaria1` cuando esta ya está en BD, pero no podemos hacer `NOT NULL` sin migrar el seed antiguo. Nullable permite el backfill suave; en producción nueva todas las altas vía endpoint lo pueblan obligatoriamente desde `current_user.id`. |

El resto del diseño se conserva tal cual:
- **Cardinalidad N:M `Asignatura ↔ Grado`** materializada como tabla `asignatura_grados`. Schema `CrearAsignaturaRequest.grado_ids: list[int]` con `Field(min_length=1)`. `AsignaturaOut.grados: list[GradoOut]`.
- **Pre-validación iterando `grado_ids` en service** (`AsignaturaService._resolver_grados` deduplica y consulta `grado_repo.obtener_por_id` por cada id) → 422 al primer id inválido con `"El grado N no existe"`. `codigo` sí confía en `UNIQUE` → 409.
- **PATCH reemplaza el conjunto entero** via `asignatura.grados = nuevos`; SQLAlchemy resuelve el diff en `asignatura_grados`.
- **Pydantic** rechaza `caracter` no en `{FB,OB,OP}`, `ects <= 0` y `grado_ids` vacío con 422 sin entrar en service.
- **`codigo` y `responsable_id` no editables** vía `extra="ignore"` en `EditarAsignaturaRequest`.
- **`require_rol(["secretaria"])` solo en POST/PATCH/DELETE**; GET sigue abierto a cualquier autenticado.
- **`AsignaturasPage` con checkboxes** para `grado_ids` (no `<select multiple>` nativo). El listado renderiza `grados.map(g => g.codigo).join(', ')`.
- **`PoliticaDirector` scopa por intersección de grados**: si el grado del Director está en la lista `asignatura.grados`, ve la dispensa. Resultado canónico: "Inglés" multi-grado (INF + ADE) → ambos directores ven sus respectivas dispensas.

## verificación end-to-end

Validado vía `curl` contra `localhost:8000` con `secretaria1` (`secre123`), `admin` (`admin123`) y `profesor1` (`profe123`):

| Escenario | Resultado |
|---|---|
| `GET /asignaturas` como `profesor1` (lectura abierta) | 200 + lista del seed (8 asignaturas: 5 INF, 2 ADE, 1 multi-grado IDIO1 INF+ADE) |
| `POST /asignaturas` como `secretaria1` con `grado_ids=[INF, ADE]` | 201 + `AsignaturaOut` con `grados: [INF, ADE]` |
| `POST /asignaturas` con `codigo=IYA038` (duplicado) | 409 `Código de asignatura en uso: IYA038` |
| `POST /asignaturas` con `grado_ids=[INF, 99999]` | 422 `El grado 99999 no existe` (pre-validación iterativa en service) |
| `POST /asignaturas` con `grado_ids=[]` | 422 Pydantic `List should have at least 1 item` |
| `POST /asignaturas` con `ects=0` | 422 Pydantic `Input should be greater than 0` |
| `POST /asignaturas` con `caracter='XX'` | 422 Pydantic `Input should be 'FB', 'OB' or 'OP'` |
| `POST /asignaturas` como `profesor1` | 403 `No autorizado para esta operación` |
| `PATCH /asignaturas/{MULTI1}` con `grado_ids=[INF]` (reemplaza el conjunto) | 200 + `grados: [INF]` |
| `DELETE /asignaturas/{IYA038}` (referenciada por profesor1) | 409 `tiene referencias en ['profesores_que_imparten']` |
| `DELETE /asignaturas/{MULTI1}` (sin referencias) | 204 |
| **Multi-grado en PoliticaDirector**: `director1` (INF) y `director2` (ADE) tras hacer IYA040 multi-grado INF+ADE | `director2` empieza a ver IYA040 además de sus ADE habituales (scoping cruza correctamente por la N:M) |

Validación visual a nivel navegador pendiente de ejecución manual (UI análoga a `GradosPage`).

## referencias

- [Análisis](/RUP/01-analisis/casos-uso/gestionarCatalogoAsignaturas/README.md)
- [Diseño](/RUP/02-diseño/casos-uso/gestionarCatalogoAsignaturas/README.md)
- [Desarrollo `gestionarCatalogoGrados()`](/RUP/03-desarrollo/casos-uso/gestionarCatalogoGrados/README.md) — patrón espejado
- [conversation-log.md](/conversation-log.md)
