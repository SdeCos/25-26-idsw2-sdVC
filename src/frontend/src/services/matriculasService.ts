import api from './api';
import type {
  MatriculaDetalle,
  MatriculaListaItem,
} from '../types/matriculas';
import type { InformeImportacionMatriculas } from '../types/paginacion';

export const matriculasService = {
  async listar(): Promise<MatriculaListaItem[]> {
    const { data } = await api.get<MatriculaListaItem[]>('/matriculas');
    return data;
  },

  async obtener(id: number): Promise<MatriculaDetalle> {
    const { data } = await api.get<MatriculaDetalle>(`/matriculas/${id}`);
    return data;
  },

  async importar(archivos: File[]): Promise<InformeImportacionMatriculas> {
    const form = new FormData();
    for (const f of archivos) form.append('archivos', f);
    const { data } = await api.post<InformeImportacionMatriculas>(
      '/matriculas/importar',
      form,
      { headers: { 'Content-Type': 'multipart/form-data' } }
    );
    return data;
  },
};
