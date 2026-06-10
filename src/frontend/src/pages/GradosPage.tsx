import React, { useEffect, useState } from 'react';
import { isAxiosError } from 'axios';
import { gradosService } from '../services/gradosService';
import type { Grado } from '../types/grados';

type Modo =
  | { tipo: 'lista' }
  | { tipo: 'alta' }
  | { tipo: 'edicion'; grado: Grado };

const FORM_VACIO = { codigo: '', nombre: '', facultad: '' };

export const GradosPage: React.FC = () => {
  const [grados, setGrados] = useState<Grado[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [modo, setModo] = useState<Modo>({ tipo: 'lista' });
  const [form, setForm] = useState(FORM_VACIO);
  const [guardando, setGuardando] = useState(false);

  const cargar = () => {
    setLoading(true);
    gradosService
      .listar()
      .then(setGrados)
      .catch(() => setError('No se pudo cargar el catálogo'))
      .finally(() => setLoading(false));
  };

  useEffect(cargar, []);

  const abrirAlta = () => {
    setForm(FORM_VACIO);
    setError(null);
    setModo({ tipo: 'alta' });
  };

  const abrirEdicion = (g: Grado) => {
    setForm({ codigo: g.codigo, nombre: g.nombre, facultad: g.facultad });
    setError(null);
    setModo({ tipo: 'edicion', grado: g });
  };

  const cancelar = () => {
    setForm(FORM_VACIO);
    setError(null);
    setModo({ tipo: 'lista' });
  };

  const submit = async (ev: React.FormEvent) => {
    ev.preventDefault();
    setError(null);
    setGuardando(true);
    try {
      if (modo.tipo === 'alta') {
        await gradosService.crear(form);
      } else if (modo.tipo === 'edicion') {
        await gradosService.actualizar(modo.grado.id, {
          nombre: form.nombre,
          facultad: form.facultad,
        });
      }
      setModo({ tipo: 'lista' });
      cargar();
    } catch (err) {
      const msg =
        isAxiosError(err) && err.response?.data?.detail
          ? String(err.response.data.detail)
          : 'No se pudo guardar';
      setError(msg);
    } finally {
      setGuardando(false);
    }
  };

  const eliminar = async (g: Grado) => {
    if (!window.confirm(`¿Eliminar grado ${g.codigo} (${g.nombre})?`)) return;
    setError(null);
    try {
      await gradosService.eliminar(g.id);
      cargar();
    } catch (err) {
      const msg =
        isAxiosError(err) && err.response?.data?.detail
          ? String(err.response.data.detail)
          : 'No se pudo eliminar';
      setError(msg);
    }
  };

  return (
    <div className="page">
      <header className="page-header">
        <h1>Grados</h1>
        {modo.tipo === 'lista' && (
          <button type="button" onClick={abrirAlta}>
            + Nuevo grado
          </button>
        )}
      </header>

      {error && <div className="error">{error}</div>}

      {(modo.tipo === 'alta' || modo.tipo === 'edicion') && (
        <form
          onSubmit={submit}
          className="form-card"
          style={{ marginBottom: '1.5rem' }}
        >
          <h2 style={{ fontSize: '1.125rem', marginBottom: '1rem' }}>
            {modo.tipo === 'alta' ? 'Nuevo grado' : `Editando ${modo.grado.codigo}`}
          </h2>

          <label>
            Código
            <input
              type="text"
              value={form.codigo}
              onChange={(e) => setForm({ ...form, codigo: e.target.value })}
              disabled={modo.tipo === 'edicion'}
              required
            />
          </label>

          <label>
            Nombre
            <input
              type="text"
              value={form.nombre}
              onChange={(e) => setForm({ ...form, nombre: e.target.value })}
              required
            />
          </label>

          <label>
            Facultad
            <input
              type="text"
              value={form.facultad}
              onChange={(e) => setForm({ ...form, facultad: e.target.value })}
              required
            />
          </label>

          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <button type="submit" disabled={guardando}>
              {guardando ? 'Guardando…' : 'Guardar'}
            </button>
            <button type="button" onClick={cancelar}>
              Cancelar
            </button>
          </div>
        </form>
      )}

      {loading && <p>Cargando…</p>}

      {!loading && (
        <table className="data-table">
          <thead>
            <tr>
              <th>Código</th>
              <th>Nombre</th>
              <th>Facultad</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {grados.map((g) => (
              <tr key={g.id}>
                <td>{g.codigo}</td>
                <td>{g.nombre}</td>
                <td>{g.facultad}</td>
                <td>
                  <button
                    type="button"
                    onClick={() => abrirEdicion(g)}
                    style={{
                      background: 'none',
                      border: 'none',
                      color: '#0066cc',
                      cursor: 'pointer',
                      padding: 0,
                    }}
                  >
                    Editar
                  </button>
                  {' · '}
                  <button
                    type="button"
                    onClick={() => eliminar(g)}
                    style={{
                      background: 'none',
                      border: 'none',
                      color: '#c00',
                      cursor: 'pointer',
                      padding: 0,
                    }}
                  >
                    Eliminar
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};
