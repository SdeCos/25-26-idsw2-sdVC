import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const linkStyle = { color: '#0071e3', textDecoration: 'none' };

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
            <Link to="/usuarios" style={linkStyle}>
              Usuarios
            </Link>
          )}
          {usuario?.tipo === 'director' && (
            <Link to="/dispensas" style={linkStyle}>
              Dispensas
            </Link>
          )}
          {usuario?.tipo === 'alumno' && (
            <Link to="/dispensas" style={linkStyle}>
              Mis dispensas
            </Link>
          )}
          {usuario?.tipo === 'profesor' && (
            <>
              <Link to="/sesiones-clase" style={linkStyle}>
                Sesiones
              </Link>
              <Link to="/alumnos" style={linkStyle}>
                Alumnos
              </Link>
              <Link to="/dispensas" style={linkStyle}>
                Dispensas
              </Link>
            </>
          )}
          {usuario?.tipo === 'secretaria' && (
            <>
              <Link to="/alumnos" style={linkStyle}>
                Alumnos
              </Link>
              <Link to="/matriculas" style={linkStyle}>
                Matrículas
              </Link>
              <Link to="/grados" style={linkStyle}>
                Grados
              </Link>
              <Link to="/asignaturas" style={linkStyle}>
                Asignaturas
              </Link>
              <Link to="/asignaciones" style={linkStyle}>
                Asignaciones
              </Link>
              <Link to="/dispensas" style={linkStyle}>
                Dispensas
              </Link>
            </>
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
