import api from './api';
import type {
  AlumnoListaItem,
  AsignaturaMatriculadaDelAlumno,
} from '../types/alumnos';
import type { InformeImportacionAlumnos } from '../types/paginacion';
import type { PaginaOut } from '../types/paginacion';

export const alumnosService = {
  async listar(params: {
    page?: number;
    size?: number;
    q?: string;
  }): Promise<PaginaOut<AlumnoListaItem>> {
    const { data } = await api.get<PaginaOut<AlumnoListaItem>>('/alumnos', {
      params,
    });
    return data;
  },

  async importar(archivos: File[]): Promise<InformeImportacionAlumnos> {
    const form = new FormData();
    for (const f of archivos) form.append('archivos', f);
    const { data } = await api.post<InformeImportacionAlumnos>(
      '/alumnos/importar',
      form,
      { headers: { 'Content-Type': 'multipart/form-data' } }
    );
    return data;
  },

  async asignaturasMatriculadas(
    alumnoId: number
  ): Promise<AsignaturaMatriculadaDelAlumno[]> {
    const { data } = await api.get<AsignaturaMatriculadaDelAlumno[]>(
      `/alumnos/${alumnoId}/asignaturas-matriculadas`
    );
    return data;
  },
};
