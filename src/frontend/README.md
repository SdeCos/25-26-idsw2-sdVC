# Frontend — CGU

SPA en React + TypeScript + Vite. Consume la API del backend en `/api/*` vía proxy de Vite.

## Arranque

```bash
cd src/frontend
npm install
npm run dev    # http://localhost:5173
```

El backend debe estar corriendo en `localhost:8000` (`uvicorn app.main:app --reload --port 8000`).

## Estructura

```
src/
├── pages/        # LoginPage, DashboardPage
├── components/   # Layout (con logout), RequireAuth
├── context/      # AuthContext (token + usuario en localStorage)
├── services/     # api (axios), authService
└── types/        # TypeScript DTOs (Usuario, TokenResponse, …)
```

Flujo: `LoginPage → useAuth().login() → authService → /api/auth/login → backend`. El token se guarda en `localStorage` y se inyecta automáticamente por interceptor en todas las peticiones siguientes. Errores 401 (excepto los del propio `/auth/login`) limpian el token y redirigen a `/login`.
