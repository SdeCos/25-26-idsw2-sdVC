export type TipoUsuario =
  | 'alumno'
  | 'profesor'
  | 'director'
  | 'secretaria'
  | 'administrador';

export interface Usuario {
  id: number;
  username: string;
  nombre: string;
  apellidos: string;
  email: string;
  tipo: TipoUsuario;
}

export interface TokenResponse {
  access_token: string;
  token_type: 'bearer';
  expira_en: string;
  usuario: Usuario;
}

export interface LoginRequest {
  username: string;
  password: string;
}
