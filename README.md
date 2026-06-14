# Centro de Gestión Universitaria

> [Centro de Gestión Universitaria](https://github.com/enmabry/25-26-IdSw1-SdR), es un sistema que permite registrar asistencias, tramitar dispensas y gestionar matriculaciones de alumnos en una universidad.

## Origen

El sistema surge del proyecto de requisitado desarrollado en [IDSW1](https://github.com/enmabry/25-26-IdSw1-SdR), donde se modelaron el dominio, los actores, los casos de uso y los prototipos del sistema.

## Estado

| Artefacto                         | Estado     |
| --------------------------------- | ---------- |
| [Requisitado](RUP/00-requisitos/) | ✅ Migrado |
| [Análisis](RUP/01-analisis/)      | ✅ 30/30   |
| [Diseño](RUP/02-diseño/)          | ✅ 30/30   |
| [Desarrollo](RUP/03-desarrollo/)  | ✅ 30/30   |

## Estructura del repositorio

```
25-26-idsw2-sdVC/
├── RUP/                      # Documentación por disciplina (READMEs y trazabilidad)
│   ├── 00-requisitos/        # Artefactos del requisitado (IDSW1-SDR)
│   ├── 01-analisis/          # Diagramas de colaboración por caso de uso
│   ├── 02-diseño/            # Diagramas de secuencia por caso de uso
│   └── 03-desarrollo/        # Trazabilidad código ↔ diseño por caso de uso
├── modelosUML/RUP/...        # Fuentes .puml — espeja la jerarquía de RUP/
├── images/RUP/...            # SVGs y PNGs — espeja la jerarquía de RUP/
├── src/
│   ├── backend/              # FastAPI + SQLAlchemy + SQLite
│   └── frontend/             # React + TypeScript + Vite
├── documents/                # Documentación adicional
├── QUE_HACE.md               # Descripción del sistema (no se modifica)
├── conversation-log.md       # Registro de conversaciones con la IA
└── README.md                 # Este archivo
```

## Proceso

| #   | Artefacto                                    | Descripción                                                         |
| --- | -------------------------------------------- | ------------------------------------------------------------------- |
| 0   | [`QUE_HACE.md`](QUE_HACE.md)                 | En el primer commit. No se modifica.                                |
| 1   | `README.md`                                  | Este archivo, reescrito con la presentación del sistema construido. |
| 2   | Código fuente                                | `/src`, o `/backend` y `/frontend` según el stack.                  |
| 3   | Diagramas UML                                | Fuentes `.puml` en `/modelosUML`. SVGs en `/images`.                |
| 4   | Imágenes                                     | En `/images`, referenciadas desde el README.                        |
| 5   | Documentación adicional                      | En `/documents`.                                                    |
| 6   | [`conversation-log.md`](conversation-log.md) | Registro completo, honesto y cronológico.                           |
