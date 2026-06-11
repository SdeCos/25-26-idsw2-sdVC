import api from './api';
import type {
  AlumnoDetalle,
  AlumnoEnAsignatura,
  AlumnoListaItem,
  AsignaturaMatriculadaDelAlumno,
  CrearAlumnoRequest,
} from '../types/alumnos';
import type { InformeImportacionAlumnos } from '../types/paginacion';
import type { PaginaOut } from '../types/paginacion';
import type { UsuarioDetalle } from '../types/usuarios';

export const alumnosService = {
  /** Listado de Secretaria (paginado + búsqueda libre). */
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

  /** Listado del Profesor (filtrado por asignatura impartida). */
  async listarPorAsignatura(
    asignaturaId: number,
    page = 1,
    size = 50
  ): Promise<PaginaOut<AlumnoEnAsignatura>> {
    const { data } = await api.get<PaginaOut<AlumnoEnAsignatura>>('/alumnos', {
      params: { asignatura_id: asignaturaId, page, size },
    });
    return data;
  },

  async crear(datos: CrearAlumnoRequest): Promise<UsuarioDetalle> {
    const { data } = await api.post<UsuarioDetalle>('/alumnos', datos);
    return data;
  },

  async obtener(id: number): Promise<AlumnoDetalle> {
    const { data } = await api.get<AlumnoDetalle>(`/alumnos/${id}`);
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
