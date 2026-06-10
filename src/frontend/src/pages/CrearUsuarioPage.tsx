import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { isAxiosError } from 'axios';
import { usuariosService } from '../services/usuariosService';
import { gradosService } from '../services/gradosService';
import type { CrearUsuarioRequest } from '../types/usuarios';
import type { TipoUsuario } from '../types/auth';
import type { Grado } from '../types/grados';

const TIPOS: TipoUsuario[] = [
  'alumno',
  'profesor',
  'director',
  'secretaria',
  'administrador',
];

// Solo Director es individual y se scopea por grado. Secretaría es un
// departamento colectivo (sin grado en la cuenta).
const ROLES_CON_GRADO: TipoUsuario[] = ['director'];

export const CrearUsuarioPage: React.FC = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState<CrearUsuarioRequest>({
    tipo: 'alumno',
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
        /* Si no es Secretaria, /grados devuelve 403. No bloquea el alta de
           tipos que no requieren grado. */
      });
  }, []);

  const necesitaGrado = ROLES_CON_GRADO.includes(form.tipo);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const payload: CrearUsuarioRequest = {
        ...form,
        grado_id: necesitaGrado ? form.grado_id : null,
      };
      const usuario = await usuariosService.crear(payload);
      navigate(`/usuarios/${usuario.id}/editar`, { replace: true });
    } catch (err) {
      if (isAxiosError(err) && err.response?.status === 409) {
        setError('Ese username ya está en uso');
      } else if (isAxiosError(err) && err.response?.status === 422) {
        const detail = err.response?.data?.detail;
        if (Array.isArray(detail) && detail[0]?.msg) {
          setError(String(detail[0].msg));
        } else {
          setError('Revisa los campos: faltan datos o el email no es válido');
        }
      } else {
        setError('No se pudo crear el usuario');
      }
    } finally {
      setLoading(false);
    }
  };

  const upd =
    <K extends keyof CrearUsuarioRequest>(key: K) =>
    (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
      const v = e.target.value;
      setForm({ ...form, [key]: v });
    };

  return (
    <div className="page">
      <header className="page-header">
        <h1>Nuevo usuario</h1>
        <Link to="/usuarios">← Volver al listado</Link>
      </header>

      <form onSubmit={handleSubmit} className="form-card">
        <div className="field">
          <label htmlFor="tipo">Tipo</label>
          <select
            id="tipo"
            value={form.tipo}
            onChange={(e) =>
              setForm({
                ...form,
                tipo: e.target.value as TipoUsuario,
                grado_id: null,
              })
            }
            required
          >
            {TIPOS.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
        </div>
        {necesitaGrado && (
          <div className="field">
            <label htmlFor="grado_id">Grado</label>
            <select
              id="grado_id"
              value={form.grado_id ?? ''}
              onChange={(e) =>
                setForm({
                  ...form,
                  grado_id: e.target.value ? Number(e.target.value) : null,
                })
              }
              required
            >
              <option value="" disabled>
                — selecciona —
              </option>
              {grados.map((g) => (
                <option key={g.id} value={g.id}>
                  {g.codigo} · {g.nombre}
                </option>
              ))}
            </select>
          </div>
        )}
        <div className="field">
          <label htmlFor="username">Username</label>
          <input id="username" value={form.username} onChange={upd('username')} required autoFocus />
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
          <input id="apellidos" value={form.apellidos} onChange={upd('apellidos')} required />
        </div>
        <div className="field">
          <label htmlFor="email">Email</label>
          <input id="email" type="email" value={form.email} onChange={upd('email')} required />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Creando…' : 'Crear y continuar a edición'}
        </button>
        {error && <div className="error">{error}</div>}
      </form>
    </div>
  );
};
