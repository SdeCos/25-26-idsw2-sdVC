import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { usuariosService } from '../services/usuariosService';
import type { UsuarioDetalle } from '../types/usuarios';

export const UsuariosPage: React.FC = () => {
  const [usuarios, setUsuarios] = useState<UsuarioDetalle[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    usuariosService
      .listar()
      .then((data) => setUsuarios(data))
      .catch(() => setError('No se pudo cargar la lista de usuarios'))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="page">
      <header className="page-header">
        <h1>Usuarios</h1>
        <Link to="/usuarios/nuevo">
          <button type="button">+ Nuevo usuario</button>
        </Link>
      </header>

      {loading && <p>Cargando…</p>}
      {error && <div className="error">{error}</div>}

      {!loading && !error && (
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Tipo</th>
              <th>Usuario</th>
              <th>Nombre</th>
              <th>Email</th>
              <th>Activo</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {usuarios.map((u) => (
              <tr key={u.id}>
                <td>{u.id}</td>
                <td>
                  <span className={`tipo-badge tipo-${u.tipo}`}>{u.tipo}</span>
                </td>
                <td>{u.username}</td>
                <td>
                  {u.nombre} {u.apellidos}
                </td>
                <td>{u.email}</td>
                <td>{u.activo ? '✓' : '✗'}</td>
                <td>
                  <Link to={`/usuarios/${u.id}`}>Ver</Link>
                  {' · '}
                  <Link to={`/usuarios/${u.id}/editar`}>Editar</Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};
