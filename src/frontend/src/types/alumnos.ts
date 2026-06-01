export interface AlumnoListaItem {
  id: number;
  username: string;
  nombre: string;
  apellidos: string;
  email: string;
  activo: boolean;
}

export interface AsignaturaMatriculadaDelAlumno {
  id: number;
  codigo: string;
  nombre: string;
  curso_academico: string;
  n_matricula: number;
}
