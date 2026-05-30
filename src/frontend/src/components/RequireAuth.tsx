import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import type { TipoUsuario } from '../types/auth';

interface Props {
  children: React.ReactNode;
  roles?: TipoUsuario[];
}

export const RequireAuth: React.FC<Props> = ({ children, roles }) => {
  const { isAuthenticated, usuario } = useAuth();
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  if (roles && usuario && !roles.includes(usuario.tipo)) {
    return <Navigate to="/dashboard" replace />;
  }
  return <>{children}</>;
};
