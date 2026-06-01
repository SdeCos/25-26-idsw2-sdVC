import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { isAxiosError } from 'axios';
import { alumnosService } from '../services/alumnosService';
import type { InformeImportacionAlumnos } from '../types/paginacion';

export const ImportarListasAlumnosPage: React.FC = () => {
  const [archivos, setArchivos] = useState<File[]>([]);
  const [informe, setInforme] = useState<InformeImportacionAlumnos | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);

  const handleFiles = (e: React.ChangeEvent<HTMLInputElement>) => {
    setArchivos(Array.from(e.target.files || []));
  };

  const importar = async (e: React.FormEvent) => {
    e.preventDefault();
    if (archivos.length === 0) return;
    setEnviando(true);
    setError(null);
    setInforme(null);
    try {
      const res = await alumnosService.importar(archivos);
      setInforme(res);
    } catch (err) {
      const detail =
        isAxiosError(err) && err.response?.data
          ? (err.response.data as { detail?: string }).detail
          : null;
      setError(detail || 'No se pudo importar el archivo');
    } finally {
      setEnviando(false);
    }
  };

  return (
    <div className="page">
      <header className="page-header">
        <h1>Importar listas de alumnos</h1>
        <Link to="/alumnos">← Volver al listado</Link>
      </header>

      <form onSubmit={importar} className="form-card">
        <div className="field">
          <label htmlFor="archivos">Archivos CSV</label>
          <input
            id="archivos"
            type="file"
            multiple
            accept=".csv"
            onChange={handleFiles}
          />
          {archivos.length > 0 && (
            <ul style={{ marginTop: '0.5rem', color: '#6e6e73', fontSize: '0.875rem' }}>
              {archivos.map((f) => (
                <li key={f.name}>{f.name} ({Math.round(f.size / 1024)} KB)</li>
              ))}
            </ul>
          )}
        </div>
        <button type="submit" disabled={enviando || archivos.length === 0}>
          {enviando ? 'Importando…' : 'Importar'}
        </button>
        <p style={{ color: '#6e6e73', fontSize: '0.875rem', marginTop: '0.5rem' }}>
          Cabecera CSV requerida:{' '}
          <code>username,password,nombre,apellidos,email,telefono?</code>
        </p>
        {error && <div className="error" style={{ marginTop: '1rem' }}>{error}</div>}
      </form>

      {informe && (
        <div className="form-card" style={{ marginTop: '1rem' }}>
          <h2>Informe de importación</h2>
          <p>
            <strong>{informe.creados}</strong> creados ·{' '}
            <strong>{informe.actualizados}</strong> actualizados ·{' '}
            <strong>{informe.errores.length}</strong> errores
          </p>
          {informe.errores.length > 0 && (
            <table className="data-table">
              <thead>
                <tr>
                  <th>Archivo</th>
                  <th>Fila</th>
                  <th>Mensaje</th>
                </tr>
              </thead>
              <tbody>
                {informe.errores.map((e, i) => (
                  <tr key={i}>
                    <td>{e.archivo}</td>
                    <td>{e.fila}</td>
                    <td>{e.mensaje}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  );
};
