import React from 'react';
import { useNavigate } from 'react-router-dom';
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
        <strong>CGU</strong>
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
