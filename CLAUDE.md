# CLAUDE.md

## Contexto del proyecto

Este repositorio es la fase de construcción del **Centro de Gestión Universitaria (CGU)**, originado en la disciplina de requisitado de IDSW1. Los artefactos del requisitado (modelo del dominio, casos de uso, diagrama de contexto, detalle y prototipos) están copiados en [`RUP/00-requisitos/`](RUP/00-requisitos/) — espejo de `../25-26-IDSW1-SDR/documents/` (fuente original en main).

La descripción del sistema está fijada en [`QUE_HACE.md`](QUE_HACE.md) y no se modifica.

## Estructura RUP

Por indicación del profesor (siguiendo la convención de SigHor), cada disciplina RUP vive en su propia carpeta autocontenida bajo `RUP/`:

- `RUP/00-requisitos/` — copia espejo del SDR
- `RUP/01-analisis/` — análisis por caso de uso (pendiente)
- `RUP/02-diseño/` — diseño técnico (pendiente)
- `RUP/03-desarrollo/` — seguimiento del desarrollo (pendiente)

El código va en `/src`. Las carpetas root `/modelosUML`, `/images`, `/documents` son scaffolding inicial **pendiente de decidir** (eliminar o repurposar para artefactos globales).

## Medida de progreso

El denominador para las fracciones del README es **24 CUs** — los casos de uso con detalle migrados del SDR, distribuidos en 5 roles: Administrador (3), Profesor (8), Alumno (3), DirectorDeGrado (2), Secretaria (8).

## Idioma

Todo en español: documentación, commits y comentarios de código.

## Protocolo de sesión

### Inicio

Leer `conversation-log.md` para retomar el contexto exacto del punto donde se dejó.

Antes de la primera entrada de la sesión, añadir al log una cabecera de día con el formato `### Sesión YYYY-MM-DD` (una sola vez por sesión, no antes de cada entrada). Si la última cabecera del archivo ya corresponde al día actual, no duplicarla.

### Durante la sesión

Tras cada intercambio relevante (cambio en código/docs, decisión de diseño o estructura, corrección de rumbo, validación de hipótesis), añadir su entrada al `conversation-log.md` con el formato definido abajo. No se espera al cierre.

## Formato del conversation-log

`HH:MM` y `YYYY-MM-DD` son plantillas: sustituirlos por la hora y fecha reales del sistema en el momento de escribir la entrada (consultar `date` si no se conoce). Nunca dejar `HH:MM` literal.

```

## [HH:MM] Título breve de lo que se pidió

**Prompt:** lo que se le dijo al AI (textual o resumido fielmente)

**Resultado:** lo que produjo

**Decisión:** qué se aceptó, qué se rechazó, qué se modificó, y por qué

```

Solo intercambios relevantes. El log no se reescribe: se escribe mientras ocurre, o al cerrar sesión como máximo.

## Artefactos

| # | Artefacto | Nota |
|---|-----------|------|
| 0 | `QUE_HACE.md` | Fijado en el primer commit. No se modifica. |
| 1 | `README.md` | Se reescribe con la presentación del sistema construido. |
| 2 | Código fuente | `/src`, o `/backend` y `/frontend` según el stack. |
| 3 | Diagramas UML | Fuentes `.puml` en `/modelosUML`. SVGs en `/images`. |
| 4 | Imágenes | En `/images`, referenciadas desde el README. |
| 5 | Documentación adicional | En `/documents`. |
| 6 | `conversation-log.md` | Completo, honesto, cronológico. |

## Qué se evalúa

- Sistema funcional que hace lo que dice `QUE_HACE.md`.
- Proceso de creación visible en los commits.
- `conversation-log.md` completo, honesto y cronológico.
- Análisis del resultado frente a los contenidos de IDSW2.
```
