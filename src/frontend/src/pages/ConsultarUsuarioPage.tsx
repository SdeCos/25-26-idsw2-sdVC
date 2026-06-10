import React, { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { isAxiosError } from 'axios';
import { usuariosService } from '../services/usuariosService';
import type { UsuarioDetalle } from '../types/usuarios';

export const ConsultarUsuarioPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [usuario, setUsuario] = useState<UsuarioDetalle | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    usuariosService
      .obtener(Number(id))
      .then((data) => setUsuario(data))
      .catch((err) => {
        if (isAxiosError(err) && err.response?.status === 404) {
          setError('Usuario no encontrado');
        } else {
          setError('No se pudo cargar el usuario');
        }
      })
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="page"><p>Cargando…</p></div>;
  if (error)
    return (
      <div className="page">
        <div className="error">{error}</div>
        <Link to="/usuarios">← Volver al listado</Link>
      </div>
    );
  if (!usuario) return null;

  return (
    <div className="page">
      <header className="page-header">
        <h1>
          {usuario.nombre} {usuario.apellidos}
        </h1>
        <div>
          <Link to="/usuarios">← Listado</Link>
          {' · '}
          <Link to={`/usuarios/${usuario.id}/editar`}>
            <button type="button">Editar</button>
          </Link>
        </div>
      </header>

      <dl className="ficha">
        <dt>ID</dt>
        <dd>{usuario.id}</dd>
        <dt>Tipo</dt>
        <dd>
          <span className={`tipo-badge tipo-${usuario.tipo}`}>{usuario.tipo}</span>
        </dd>
        <dt>Username</dt>
        <dd>{usuario.username}</dd>
        <dt>Email</dt>
        <dd>{usuario.email}</dd>
        <dt>Activo</dt>
        <dd>{usuario.activo ? 'Sí' : 'No'}</dd>
        {usuario.grado && (
          <>
            <dt>Grado</dt>
            <dd>
              {usuario.grado.codigo} · {usuario.grado.nombre} — {usuario.grado.facultad}
            </dd>
          </>
        )}
      </dl>
    </div>
  );
};
