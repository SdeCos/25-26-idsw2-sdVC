# CGU > exportarHistorialAsistencias > Desarrollo

> | [🏠️](/README.md) | [Desarrollo](/RUP/03-desarrollo/README.md) | [Análisis](/RUP/01-analisis/casos-uso/exportarHistorialAsistencias/README.md) | [Diseño](/RUP/02-diseño/casos-uso/exportarHistorialAsistencias/README.md) | **Desarrollo** |
> |-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Construcción
- **Disciplina**: Desarrollo
- **Caso de uso**: `exportarHistorialAsistencias()`
- **Actor**: Profesor
- **Versión**: 1.0
- **Fecha**: 2026-06-02

## trazabilidad código ↔ diseño

| Participante del diseño | Implementación |
|---|---|
| Selector de asignatura + botón "Exportar historial CSV" en `SesionesClasePage` | [src/frontend/src/pages/SesionesClasePage.tsx](/src/frontend/src/pages/SesionesClasePage.tsx) |
| asistenciasService.exportar (`responseType: 'blob'`) | [src/frontend/src/services/asistenciasService.ts](/src/frontend/src/services/asistenciasService.ts) |
| AsistenciasRouter (`GET /asistencias/exportar`) | [src/backend/app/routers/asistencias.py](/src/backend/app/routers/asistencias.py) |
| Defensa "Profesor competente" en el router | mismo archivo |
| AsistenciaRepository.obtener_por_rango (join con `sesiones_clase`) | [src/backend/app/repositories/asistencia_repository.py](/src/backend/app/repositories/asistencia_repository.py) |
| GeneradorArchivoAsistencias (CSV con BOM utf-8-sig) | [src/backend/app/services/generador_archivo_asistencias.py](/src/backend/app/services/generador_archivo_asistencias.py) |

## divergencia documentada respecto al diseño

| Diseño | Implementación | Motivo |
|---|---|---|
| Modal con campos `desde`/`hasta`/`formato` | Selector inline en `SesionesClasePage` (sin modal, sin rango) | Simplificación UX: el caso típico es "exporta todo el historial de la asignatura". Si emerge la necesidad de rango, se añade modal con `desde`/`hasta` sin tocar el endpoint (los query params ya están). |

## verificación end-to-end

| Escenario | Resultado |
|---|---|
| `GET /asistencias/exportar?asignatura_id=2` Profesor competente | 200 + CSV con cabecera + filas |
| Mismo endpoint con asignatura NO impartida | 403 |
| CSV abierto en Excel (BOM utf-8-sig) | tildes correctas (María, López) |

## decisiones materializadas

- **Formato CSV único** en v1.0 (XLSX/PDF como deuda blanda).
- **`GeneradorArchivoAsistencias` paralelo a `GeneradorArchivoDispensas`** — segundo servicio del proyecto.
- **Sin abstracción `Generador<T>`** — los dos servicios comparten forma pero no contrato intercambiable; agruparlos por ABC sería sintaxis sin polimorfismo real.
- **Filtros como query params simples** — `desde`/`hasta` opcionales. Si emerge un tercer endpoint con filtros similares, se refactoriza a Parameter Object.

## referencias

- [Análisis](/RUP/01-analisis/casos-uso/exportarHistorialAsistencias/README.md)
- [Diseño](/RUP/02-diseño/casos-uso/exportarHistorialAsistencias/README.md)
- [conversation-log.md](/conversation-log.md)
