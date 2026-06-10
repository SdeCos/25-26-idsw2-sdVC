import type { TipoUsuario } from './auth';
import type { Grado } from './grados';

export interface UsuarioDetalle {
  id: number;
  tipo: TipoUsuario;
  username: string;
  nombre: string;
  apellidos: string;
  email: string;
  activo: boolean;
  grado: Grado | null;
}

export interface CrearUsuarioRequest {
  tipo: TipoUsuario;
  username: string;
  password: string;
  nombre: string;
  apellidos: string;
  email: string;
  grado_id?: number | null;
}

export interface EditarUsuarioRequest {
  username?: string;
  password?: string;
  nombre?: string;
  apellidos?: string;
  email?: string;
  activo?: boolean;
  grado_id?: number | null;
}
