export interface Grado {
  id: number;
  codigo: string;
  nombre: string;
  facultad: string;
}

export interface CrearGradoRequest {
  codigo: string;
  nombre: string;
  facultad: string;
}

export interface EditarGradoRequest {
  nombre?: string;
  facultad?: string;
}
