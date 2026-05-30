import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { isAxiosError } from 'axios';
import { usuariosService } from '../services/usuariosService';
import type { CrearUsuarioRequest } from '../types/usuarios';
import type { TipoUsuario } from '../types/auth';

const TIPOS: TipoUsuario[] = [
  'alumno',
  'profesor',
  'director',
  'secretaria',
  'administrador',
];

export const CrearUsuarioPage: React.FC = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState<CrearUsuarioRequest>({
    tipo: 'alumno',
    username: '',
    password: '',
    nombre: '',
    apellidos: '',
    email: '',
  });
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const usuario = await usuariosService.crear(form);
      navigate(`/usuarios/${usuario.id}/editar`, { replace: true });
    } catch (err) {
      if (isAxiosError(err) && err.response?.status === 409) {
        setError('Ese username ya está en uso');
      } else if (isAxiosError(err) && err.response?.status === 422) {
        setError('Revisa los campos: faltan datos o el email no es válido');
      } else {
        setError('No se pudo crear el usuario');
      }
    } finally {
      setLoading(false);
    }
  };

  const upd =
    <K extends keyof CrearUsuarioRequest>(key: K) =>
    (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) =>
      setForm({ ...form, [key]: e.target.value });

  return (
    <div className="page">
      <header className="page-header">
        <h1>Nuevo usuario</h1>
        <Link to="/usuarios">← Volver al listado</Link>
      </header>

      <form onSubmit={handleSubmit} className="form-card">
        <div className="field">
          <label htmlFor="tipo">Tipo</label>
          <select id="tipo" value={form.tipo} onChange={upd('tipo')} required>
            {TIPOS.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
        </div>
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
