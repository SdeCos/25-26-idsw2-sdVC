# Desarrollo

Disciplina RUP de desarrollo del Centro de Gestión Universitaria.

Para cada caso de uso diseñado en [`RUP/02-diseño/`](/RUP/02-diseño/) se produce su implementación bajo [`/src`](/src/) y un README en `casos-uso/<cuName>/` con la trazabilidad código ↔ diseño.

## Estructura del código

- [`/src/backend/`](/src/backend/) — FastAPI + SQLAlchemy + SQLite + JWT/bcrypt. Capas `routers → services → repositories → models`. Arranque: `uvicorn app.main:app --reload --port 8000`.
- [`/src/frontend/`](/src/frontend/) — React 18 + TypeScript + Vite + axios + Context. Arranque: `npm run dev` (sirve en `:5173`, proxy `/api` → `:8000`).

## Modo iterativo

Cada ramillete diseña e implementa antes de pasar al siguiente actor — no se desarrolla todo de golpe.

## Casos de uso implementados

Ver [índice](casos-uso/README.md) — 18/26.

## Referencias

- [Diseño](/RUP/02-diseño/)
- [Análisis](/RUP/01-analisis/)
