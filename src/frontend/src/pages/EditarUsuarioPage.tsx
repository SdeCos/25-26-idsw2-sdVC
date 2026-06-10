import React, { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { isAxiosError } from 'axios';
import { usuariosService } from '../services/usuariosService';
import { gradosService } from '../services/gradosService';
import type { EditarUsuarioRequest, UsuarioDetalle } from '../types/usuarios';
import type { Grado } from '../types/grados';

// Solo Director es individual y se scopea por grado. Secretaría es colectivo.
const ROLES_CON_GRADO = new Set(['director']);

interface FormState {
  username: string;
  password: string;
  nombre: string;
  apellidos: string;
  email: string;
  activo: boolean;
  grado_id: number | null;
}

const desdeUsuario = (u: UsuarioDetalle): FormState => ({
  username: u.username,
  password: '',
  nombre: u.nombre,
  apellidos: u.apellidos,
  email: u.email,
  activo: u.activo,
  grado_id: u.grado?.id ?? null,
});

export const EditarUsuarioPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [original, setOriginal] = useState<UsuarioDetalle | null>(null);
  const [form, setForm] = useState<FormState | null>(null);
  const [grados, setGrados] = useState<Grado[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (!id) return;
    usuariosService
      .obtener(Number(id))
      .then((u) => {
        setOriginal(u);
        setForm(desdeUsuario(u));
      })
      .catch((err) => {
        if (isAxiosError(err) && err.response?.status === 404) {
          setError('Usuario no encontrado');
        } else {
          setError('No se pudo cargar el usuario');
        }
      });
    gradosService
      .listar()
      .then(setGrados)
      .catch(() => {
        /* Si Admin no tiene acceso a /grados, lo dejamos sin cargar. */
      });
  }, [id]);

  const diff = (): EditarUsuarioRequest => {
    if (!original || !form) return {};
    const cambios: EditarUsuarioRequest = {};
    if (form.username !== original.username) cambios.username = form.username;
    if (form.password) cambios.password = form.password;
    if (form.nombre !== original.nombre) cambios.nombre = form.nombre;
    if (form.apellidos !== original.apellidos) cambios.apellidos = form.apellidos;
    if (form.email !== original.email) cambios.email = form.email;
    if (form.activo !== original.activo) cambios.activo = form.activo;
    if (ROLES_CON_GRADO.has(original.tipo)) {
      const originalGradoId = original.grado?.id ?? null;
      if (form.grado_id !== originalGradoId) cambios.grado_id = form.grado_id;
    }
    return cambios;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!original) return;
    const cambios = diff();
    if (Object.keys(cambios).length === 0) {
      navigate(`/usuarios/${original.id}`);
      return;
    }
    setSaving(true);
    setError(null);
    try {
      await usuariosService.actualizar(original.id, cambios);
      navigate(`/usuarios/${original.id}`);
    } catch (err) {
      if (isAxiosError(err) && err.response?.status === 409) {
        setError('Ese username ya está en uso');
      } else if (isAxiosError(err) && err.response?.status === 422) {
        setError('Revisa los campos: alguno no es válido');
      } else {
        setError('No se pudo guardar el usuario');
      }
    } finally {
      setSaving(false);
    }
  };

  if (error && !form) {
    return (
      <div className="page">
        <div className="error">{error}</div>
        <Link to="/usuarios">← Volver al listado</Link>
      </div>
    );
  }
  if (!form || !original) return <div className="page"><p>Cargando…</p></div>;

  return (
    <div className="page">
      <header className="page-header">
        <h1>Editar usuario #{original.id}</h1>
        <div>
          <Link to={`/usuarios/${original.id}`}>← Cancelar</Link>
        </div>
      </header>

      <form onSubmit={handleSubmit} className="form-card">
        <div className="field">
          <label>Tipo</label>
          <input value={original.tipo} disabled />
          <small style={{ color: '#6e6e73' }}>
            El tipo se fija en el alta y no se puede modificar.
          </small>
        </div>
        {ROLES_CON_GRADO.has(original.tipo) && (
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
          <input
            id="username"
            value={form.username}
            onChange={(e) => setForm({ ...form, username: e.target.value })}
            required
          />
        </div>
        <div className="field">
          <label htmlFor="password">Nueva contraseña (opcional)</label>
          <input
            id="password"
            type="password"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            minLength={6}
            placeholder="Dejar en blanco para no cambiar"
          />
        </div>
        <div className="field">
          <label htmlFor="nombre">Nombre</label>
          <input
            id="nombre"
            value={form.nombre}
            onChange={(e) => setForm({ ...form, nombre: e.target.value })}
            required
          />
        </div>
        <div className="field">
          <label htmlFor="apellidos">Apellidos</label>
          <input
            id="apellidos"
            value={form.apellidos}
            onChange={(e) => setForm({ ...form, apellidos: e.target.value })}
            required
          />
        </div>
        <div className="field">
          <label htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            required
          />
        </div>
        <div className="field">
          <label>
            <input
              type="checkbox"
              checked={form.activo}
              onChange={(e) => setForm({ ...form, activo: e.target.checked })}
            />
            {' '}Activo
          </label>
        </div>
        <button type="submit" disabled={saving}>
          {saving ? 'Guardando…' : 'Guardar cambios'}
        </button>
        {error && <div className="error">{error}</div>}
      </form>
    </div>
  );
};
