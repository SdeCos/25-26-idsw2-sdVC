#!/usr/bin/env bash
# Arranca backend (FastAPI/uvicorn) y frontend (Vite) del CGU.
# Uso: ./scripts/start.sh    (Ctrl+C para parar ambos)

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACK="$ROOT/src/backend"
FRONT="$ROOT/src/frontend"

cd "$BACK"

if [ ! -d ".venv" ]; then
  echo "==> Creando venv del backend"
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

if ! python -c "import fastapi" 2>/dev/null; then
  echo "==> Instalando dependencias del backend"
  pip install -e ".[dev]"
fi

if [ ! -f ".env" ]; then
  echo "==> Copiando .env.example a .env"
  cp .env.example .env
fi

echo "==> Sembrando usuarios (idempotente)"
python -m scripts.seed

echo "==> Arrancando backend en http://localhost:8000"
uvicorn app.main:app --reload --port 8000 &
BACK_PID=$!

cd "$FRONT"

if [ ! -d "node_modules" ]; then
  echo "==> Instalando dependencias del frontend"
  npm install
fi

echo "==> Arrancando frontend en http://localhost:5173"
npm run dev &
FRONT_PID=$!

cleanup() {
  echo ""
  echo "==> Parando procesos"
  kill "$BACK_PID" "$FRONT_PID" 2>/dev/null || true
  wait "$BACK_PID" "$FRONT_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

wait
