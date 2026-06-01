# CGU > exportarDispensas > Desarrollo

> | [🏠️](/README.md) | [Desarrollo](/RUP/03-desarrollo/README.md) | [Análisis](/RUP/01-analisis/casos-uso/exportarDispensas/README.md) | [Diseño](/RUP/02-diseño/casos-uso/exportarDispensas/README.md) | **Desarrollo** |
> |-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Construcción
- **Disciplina**: Desarrollo
- **Caso de uso**: `exportarDispensas()`
- **Actor**: Secretaria
- **Versión**: 1.0
- **Fecha**: 2026-06-01

## trazabilidad código ↔ diseño

| Participante del diseño | Implementación |
|---|---|
| DispensasPage botón "Exportar CSV" (sólo Secretaria) | [src/frontend/src/pages/DispensasPage.tsx](/src/frontend/src/pages/DispensasPage.tsx) |
| dispensasService.exportar (Blob + download) | [src/frontend/src/services/dispensasService.ts](/src/frontend/src/services/dispensasService.ts) |
| DispensasRouter (`GET /dispensas/exportar` con `require_rol(["secretaria"])`) | [src/backend/app/routers/dispensas.py](/src/backend/app/routers/dispensas.py) |
| SolicitudDispensaRepository.obtener_por_filtros | [src/backend/app/repositories/solicitud_dispensa_repository.py](/src/backend/app/repositories/solicitud_dispensa_repository.py) |
| GeneradorArchivoDispensas (tercer servicio del proyecto) | [src/backend/app/services/generador_archivo_dispensas.py](/src/backend/app/services/generador_archivo_dispensas.py) |

## verificación end-to-end

| Escenario | Resultado |
|---|---|
| `GET /dispensas/exportar` con Secretaria | 200 + `Content-Disposition: attachment; filename="dispensas-YYYY-MM-DD.csv"` + UTF-8 BOM + 13 columnas |
| Mismo endpoint con Director | 403 |
| Mismo endpoint con Alumno | 403 |
| Filtros `?estado=aprobada` | 200 con solo dispensas APROBADAS |

## decisiones materializadas

- **`GET /dispensas/exportar` dedicado**, no `?formato=csv` sobre el listado.
- **`GeneradorArchivoDispensas.generar_csv(lista) → bytes`** con `csv.writer` stdlib y BOM `utf-8-sig` para Excel.
- **Frontend usa `responseType: 'blob'`** + `URL.createObjectURL` + `<a download>` para disparar la descarga sin recargar la SPA.
- **Filtros opcionales** `estado, alumno_id, desde, hasta` como query params.

## referencias

- [Análisis](/RUP/01-analisis/casos-uso/exportarDispensas/README.md)
- [Diseño](/RUP/02-diseño/casos-uso/exportarDispensas/README.md)
- [conversation-log.md](/conversation-log.md)
