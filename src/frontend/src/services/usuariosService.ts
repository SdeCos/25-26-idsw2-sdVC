import api from './api';
import type {
  CrearUsuarioRequest,
  EditarUsuarioRequest,
  UsuarioDetalle,
} from '../types/usuarios';

export const usuariosService = {
  async listar(): Promise<UsuarioDetalle[]> {
    const { data } = await api.get<UsuarioDetalle[]>('/usuarios');
    return data;
  },

  async obtener(id: number): Promise<UsuarioDetalle> {
    const { data } = await api.get<UsuarioDetalle>(`/usuarios/${id}`);
    return data;
  },

  async crear(body: CrearUsuarioRequest): Promise<UsuarioDetalle> {
    const { data } = await api.post<UsuarioDetalle>('/usuarios', body);
    return data;
  },

  async actualizar(id: number, body: EditarUsuarioRequest): Promise<UsuarioDetalle> {
    const { data } = await api.patch<UsuarioDetalle>(`/usuarios/${id}`, body);
    return data;
  },
};
