import api from './api';
import type {
  CrearSolicitudRequest,
  EditarSolicitudRequest,
  SolicitudDispensa,
} from '../types/dispensas';

export const dispensasService = {
  async listar(): Promise<SolicitudDispensa[]> {
    const { data } = await api.get<SolicitudDispensa[]>('/dispensas');
    return data;
  },

  async obtener(id: number): Promise<SolicitudDispensa> {
    const { data } = await api.get<SolicitudDispensa>(`/dispensas/${id}`);
    return data;
  },

  async crear(body: CrearSolicitudRequest): Promise<SolicitudDispensa> {
    const { data } = await api.post<SolicitudDispensa>('/dispensas', body);
    return data;
  },

  async actualizar(
    id: number,
    body: EditarSolicitudRequest
  ): Promise<SolicitudDispensa> {
    const { data } = await api.patch<SolicitudDispensa>(`/dispensas/${id}`, body);
    return data;
  },
};
