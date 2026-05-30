import type { TipoUsuario } from './auth';

export interface UsuarioDetalle {
  id: number;
  tipo: TipoUsuario;
  username: string;
  nombre: string;
  apellidos: string;
  email: string;
  activo: boolean;
}

export interface CrearUsuarioRequest {
  tipo: TipoUsuario;
  username: string;
  password: string;
  nombre: string;
  apellidos: string;
  email: string;
}

export interface EditarUsuarioRequest {
  username?: string;
  password?: string;
  nombre?: string;
  apellidos?: string;
  email?: string;
  activo?: boolean;
}
