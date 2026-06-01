# Diseño

Disciplina RUP de diseño del Centro de Gestión Universitaria.

Para cada caso de uso analizado en [`RUP/01-analisis/`](/RUP/01-analisis/) se produce un **diagrama de secuencia** que lo realiza con tecnología concreta: componentes React, endpoints FastAPI, servicios, repositorios y BD.

## Cambio de notación respecto al análisis

| | Análisis | Diseño |
|---|---|---|
| Diagrama | Colaboración (enlaces conceptuales) | Secuencia (orden temporal + tecnología) |
| Clases | Estereotipos MVC abstractos | Componentes y módulos concretos |
| Mensajes | Intención de negocio | Llamadas a métodos / endpoints HTTP |

## Modo iterativo

Por indicación del profesor: **diseño + implementación por ramillete de actor**. Se diseñan los CUs de un actor, se implementan, y se pasa al siguiente. No se diseña todo por adelantado.

## Stack

| Capa | Tecnología |
|---|---|
| Backend | Python 3.11 + FastAPI + SQLAlchemy async |
| Persistencia | SQLite (`aiosqlite`), migrable a PostgreSQL sin cambio de código |
| Auth | JWT (`python-jose`) + bcrypt (`passlib`) |
| Frontend | React 18 + TypeScript + Vite + axios + Context API |
| Estructura | `src/backend/` (capas `routers → services → repositories → models`) y `src/frontend/` (capas `pages → services → context`) |

Stack alineado con la rama [`diseño-fastapi-react`](https://github.com/mmasias/pySigHor/tree/dise%C3%B1o-fastapi-react) de pySigHor.

## Casos de uso diseñados

Ver [índice](casos-uso/README.md) — 18/26.

## Referencias

- [Análisis](/RUP/01-analisis/)
- [pySigHor — diseño-fastapi-react](https://github.com/mmasias/pySigHor/tree/dise%C3%B1o-fastapi-react)
- [Temario IDSW2 — diseño OO](https://github.com/mmasias/25-26-IdSw2/tree/main/temario/03-dise%C3%B1oOO)
