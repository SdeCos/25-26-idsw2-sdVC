import api from './api';

export interface FiltrosHistorial {
  asignatura_id: number;
  desde?: string; // YYYY-MM-DD
  hasta?: string;
}

export const asistenciasService = {
  async exportar(filtros: FiltrosHistorial): Promise<Blob> {
    const { data } = await api.get('/asistencias/exportar', {
      params: filtros,
      responseType: 'blob',
    });
    return data as Blob;
  },
};
