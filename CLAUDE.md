# CLAUDE.md

## Contexto del proyecto

Este repositorio es la fase de construcción del **Centro de Gestión Universitaria (CGU)**, originado en la disciplina de requisitado de IDSW1. Los artefactos del requisitado (modelo del dominio, casos de uso, diagrama de contexto, detalle y prototipos) están en `../25-26-IDSW1-SDR/documents/`.

La descripción del sistema está fijada en [`QUE_HACE.md`](QUE_HACE.md) y no se modifica.

## Idioma

Todo en español: documentación, commits y comentarios de código.

## Protocolo de sesión

### Inicio

Leer `conversation-log.md` para retomar el contexto exacto del punto donde se dejó.

### Cierre

Cuando el usuario diga "fin de sesión" o similar, añadir una nueva entrada al `conversation-log.md` con el formato definido abajo.

## Formato del conversation-log ```

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
