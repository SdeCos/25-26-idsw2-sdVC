import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { isAxiosError } from 'axios';
import { dispensasService } from '../services/dispensasService';
import { alumnosService } from '../services/alumnosService';
import type { AsignaturaMatriculadaDelAlumno } from '../types/alumnos';
import { useAuth } from '../context/AuthContext';

export const CrearSolicitudPage: React.FC = () => {
  const navigate = useNavigate();
  const { usuario } = useAuth();
  const [asignaturas, setAsignaturas] = useState<
    AsignaturaMatriculadaDelAlumno[]
  >([]);
  const [asignaturaMatriculadaId, setAsignaturaMatriculadaId] = useState<number | ''>('');
  const [motivo, setMotivo] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!usuario) return;
    alumnosService
      .asignaturasMatriculadas(usuario.id)
      .then((lista) => {
        setAsignaturas(lista);
        if (lista.length > 0) setAsignaturaMatriculadaId(lista[0].id);
      })
      .catch(() => setError('No se pudieron cargar tus asignaturas matriculadas'));
  }, [usuario]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!asignaturaMatriculadaId) {
      setError('Selecciona una asignatura');
      return;
    }
    setError(null);
    setLoading(true);
    try {
      const creada = await dispensasService.crear({
        asignatura_matriculada_id: Number(asignaturaMatriculadaId),
        motivo,
      });
      navigate(`/dispensas/${creada.id}`, { replace: true });
    } catch (err) {
      const detail =
        isAxiosError(err) && err.response?.data
          ? (err.response.data as { detail?: string }).detail
          : null;
      setError(detail || 'No se pudo crear la solicitud');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <header className="page-header">
        <h1>Nueva solicitud de dispensa</h1>
        <Link to="/dispensas">← Volver al listado</Link>
      </header>

      {asignaturas.length === 0 && !error && (
        <p style={{ color: '#6e6e73' }}>Cargando asignaturas matriculadas…</p>
      )}

      {asignaturas.length > 0 && (
        <form onSubmit={handleSubmit} className="form-card">
          <div className="field">
            <label htmlFor="am">Asignatura matriculada</label>
            <select
              id="am"
              value={asignaturaMatriculadaId}
              onChange={(e) => setAsignaturaMatriculadaId(Number(e.target.value))}
              required
            >
              {asignaturas.map((am) => (
                <option key={am.id} value={am.id}>
                  {am.codigo} · {am.nombre} ({am.curso_academico}, {am.n_matricula}ª)
                </option>
              ))}
            </select>
          </div>
          <div className="field">
            <label htmlFor="motivo">Motivo</label>
            <textarea
              id="motivo"
              value={motivo}
              onChange={(e) => setMotivo(e.target.value)}
              required
              rows={4}
              placeholder="Explica brevemente la razón de la solicitud…"
            />
          </div>
          <button type="submit" disabled={loading}>
            {loading ? 'Creando…' : 'Crear solicitud'}
          </button>
          {error && <div className="error">{error}</div>}
        </form>
      )}
    </div>
  );
};
