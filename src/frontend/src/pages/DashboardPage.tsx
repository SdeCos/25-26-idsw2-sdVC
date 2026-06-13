import React from 'react';
import { useAuth } from '../context/AuthContext';

export const DashboardPage: React.FC = () => {
  const { usuario } = useAuth();
  return (
    <div>
      <h1>Hola, {usuario?.nombre}</h1>
      <p style={{ marginTop: '1rem', color: '#6e6e73' }}>
        Has iniciado sesión como <strong>{usuario?.tipo}</strong>.
      </p>
    </div>
  );
};
