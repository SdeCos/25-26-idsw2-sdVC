import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { usuario, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login', { replace: true });
  };

  return (
    <>
      <header className="layout-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
          <Link to="/dashboard" style={{ textDecoration: 'none', color: 'inherit' }}>
            <strong>CGU</strong>
          </Link>
          {usuario?.tipo === 'administrador' && (
            <Link to="/usuarios" style={{ color: '#0071e3', textDecoration: 'none' }}>
              Usuarios
            </Link>
          )}
          {usuario?.tipo === 'director' && (
            <Link to="/dispensas" style={{ color: '#0071e3', textDecoration: 'none' }}>
              Dispensas
            </Link>
          )}
          {usuario?.tipo === 'alumno' && (
            <Link to="/dispensas" style={{ color: '#0071e3', textDecoration: 'none' }}>
              Mis dispensas
            </Link>
          )}
        </div>
        <div>
          <span style={{ marginRight: '1rem', color: '#6e6e73' }}>
            {usuario?.nombre} {usuario?.apellidos} · {usuario?.tipo}
          </span>
          <button onClick={handleLogout}>Cerrar sesión</button>
        </div>
      </header>
      <main className="layout-main">{children}</main>
    </>
  );
};
