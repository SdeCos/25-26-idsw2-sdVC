import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { alumnosService } from '../services/alumnosService';
import { useAuth } from '../context/AuthContext';
import type { AlumnoListaItem } from '../types/alumnos';
import type { PaginaOut } from '../types/paginacion';

export const AlumnosPage: React.FC = () => {
  const { usuario } = useAuth();
  const esSecretaria = usuario?.tipo === 'secretaria';
  const [pagina, setPagina] = useState<PaginaOut<AlumnoListaItem> | null>(null);
  const [page, setPage] = useState(1);
  const [size] = useState(25);
  const [q, setQ] = useState('');
  const [qSubmit, setQSubmit] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    alumnosService
      .listar({ page, size, q: qSubmit || undefined })
      .then(setPagina)
      .catch(() => setError('No se pudo cargar el listado de alumnos'))
      .finally(() => setLoading(false));
  }, [page, size, qSubmit]);

  const buscar = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(1);
    setQSubmit(q);
  };

  const totalPaginas = pagina ? Math.max(1, Math.ceil(pagina.total / pagina.size)) : 1;

  return (
    <div className="page">
      <header className="page-header">
        <h1>Alumnos</h1>
        {esSecretaria && (
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <Link to="/alumnos/nuevo">
              <button type="button">+ Nuevo alumno</button>
            </Link>
            <Link to="/alumnos/importar">
              <button type="button">Importar listas</button>
            </Link>
          </div>
        )}
      </header>

      <form
        onSubmit={buscar}
        style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem' }}
      >
        <input
          type="search"
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Buscar por username, nombre, apellidos, email…"
          style={{ flex: 1 }}
        />
        <button type="submit">Buscar</button>
        {qSubmit && (
          <button
            type="button"
            onClick={() => {
              setQ('');
              setQSubmit('');
              setPage(1);
            }}
          >
            Limpiar
          </button>
        )}
      </form>

      {loading && <p>Cargando…</p>}
      {error && <div className="error">{error}</div>}

      {!loading && !error && pagina && (
        <>
          <table className="data-table">
            <thead>
              <tr>
                <th>Username</th>
                <th>Nombre</th>
                <th>Apellidos</th>
                <th>Email</th>
                <th>Activo</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {pagina.items.map((a) => (
                <tr key={a.id}>
                  <td>{a.username}</td>
                  <td>{a.nombre}</td>
                  <td>{a.apellidos}</td>
                  <td>{a.email}</td>
                  <td>{a.activo ? 'Sí' : 'No'}</td>
                  <td>
                    <Link to={`/alumnos/${a.id}`}>Ver ficha</Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {pagina.items.length === 0 && (
            <p style={{ color: '#6e6e73', marginTop: '1rem' }}>
              {qSubmit
                ? `Sin resultados para "${qSubmit}".`
                : 'No hay alumnos registrados todavía.'}
            </p>
          )}

          <div style={{ marginTop: '1rem', display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
            <button
              type="button"
              disabled={page <= 1}
              onClick={() => setPage((p) => p - 1)}
            >
              ←
            </button>
            <span>
              Página {pagina.page} de {totalPaginas} · {pagina.total} alumnos
            </span>
            <button
              type="button"
              disabled={page >= totalPaginas}
              onClick={() => setPage((p) => p + 1)}
            >
              →
            </button>
          </div>
        </>
      )}
    </div>
  );
};
