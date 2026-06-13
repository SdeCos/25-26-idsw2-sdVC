import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { isAxiosError } from 'axios';
import { alumnosService } from '../services/alumnosService';
import { gradosService } from '../services/gradosService';
import type { CrearAlumnoRequest } from '../types/alumnos';
import type { Grado } from '../types/grados';

export const CrearAlumnoPage: React.FC = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState<CrearAlumnoRequest>({
    username: '',
    password: '',
    nombre: '',
    apellidos: '',
    email: '',
    grado_id: null,
  });
  const [grados, setGrados] = useState<Grado[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    gradosService
      .listar()
      .then(setGrados)
      .catch(() => {
        /* sin grados disponibles → el selector queda vacío y el alta se hace
           sin matrícula; flujo soportado por backend. */
      });
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await alumnosService.crear(form);
      navigate('/alumnos', { replace: true });
    } catch (err) {
      if (isAxiosError(err) && err.response?.status === 409) {
        setError('Ese username ya está en uso');
      } else if (isAxiosError(err) && err.response?.status === 422) {
        const detail = err.response?.data?.detail;
        if (Array.isArray(detail) && detail[0]?.msg) {
          setError(String(detail[0].msg));
        } else if (typeof detail === 'string') {
          setError(detail);
        } else {
          setError('Revisa los campos: faltan datos o el email no es válido');
        }
      } else {
        setError('No se pudo crear el alumno');
      }
    } finally {
      setLoading(false);
    }
  };

  const upd =
    <K extends keyof CrearAlumnoRequest>(key: K) =>
    (e: React.ChangeEvent<HTMLInputElement>) => {
      setForm({ ...form, [key]: e.target.value });
    };

  return (
    <div className="page">
      <header className="page-header">
        <h1>Nuevo alumno</h1>
        <Link to="/alumnos">← Volver al listado</Link>
      </header>

      <form onSubmit={handleSubmit} className="form-card">
        <div className="field">
          <label htmlFor="username">Username</label>
          <input
            id="username"
            value={form.username}
            onChange={upd('username')}
            required
            autoFocus
          />
        </div>
        <div className="field">
          <label htmlFor="password">Contraseña</label>
          <input
            id="password"
            type="password"
            value={form.password}
            onChange={upd('password')}
            required
            minLength={6}
          />
        </div>
        <div className="field">
          <label htmlFor="nombre">Nombre</label>
          <input id="nombre" value={form.nombre} onChange={upd('nombre')} required />
        </div>
        <div className="field">
          <label htmlFor="apellidos">Apellidos</label>
          <input
            id="apellidos"
            value={form.apellidos}
            onChange={upd('apellidos')}
            required
          />
        </div>
        <div className="field">
          <label htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            value={form.email}
            onChange={upd('email')}
            required
          />
        </div>
        <div className="field">
          <label htmlFor="grado_id">Grado (opcional)</label>
          <select
            id="grado_id"
            value={form.grado_id ?? ''}
            onChange={(e) =>
              setForm({
                ...form,
                grado_id: e.target.value ? Number(e.target.value) : null,
              })
            }
          >
            <option value="">— sin matrícula —</option>
            {grados.map((g) => (
              <option key={g.id} value={g.id}>
                {g.codigo} · {g.nombre}
              </option>
            ))}
          </select>
          <small style={{ color: '#6e6e73' }}>
            Si lo eliges, se crea una matrícula vacía 2025/2026 para ese grado.
          </small>
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Creando…' : 'Crear alumno'}
        </button>
        {error && <div className="error">{error}</div>}
      </form>
    </div>
  );
};
