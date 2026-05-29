import React, { createContext, useContext, useState } from 'react';
import { authService } from '../services/authService';
import type { Usuario } from '../types/auth';

interface AuthContextValue {
  usuario: Usuario | null;
  isAuthenticated: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

const STORAGE_USER = 'usuario';
const STORAGE_TOKEN = 'access_token';

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [usuario, setUsuario] = useState<Usuario | null>(() => {
    const raw = localStorage.getItem(STORAGE_USER);
    return raw ? (JSON.parse(raw) as Usuario) : null;
  });

  const login = async (username: string, password: string) => {
    const response = await authService.login({ username, password });
    localStorage.setItem(STORAGE_TOKEN, response.access_token);
    localStorage.setItem(STORAGE_USER, JSON.stringify(response.usuario));
    setUsuario(response.usuario);
  };

  const logout = async () => {
    try {
      await authService.logout();
    } catch {
      // Si la red falla o el token está expirado, igualmente cerramos sesión en cliente.
    }
    localStorage.removeItem(STORAGE_TOKEN);
    localStorage.removeItem(STORAGE_USER);
    setUsuario(null);
  };

  return (
    <AuthContext.Provider
      value={{ usuario, isAuthenticated: usuario !== null, login, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextValue => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth debe usarse dentro de <AuthProvider>');
  return ctx;
};
