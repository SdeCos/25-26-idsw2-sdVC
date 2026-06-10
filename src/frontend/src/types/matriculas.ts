import type { Grado } from './grados';

export interface AlumnoMin {
  id: number;
  username: string;
  nombre: string;
  apellidos: string;
  email: string;
}

export interface ResponsableMin {
  id: number;
  nombre: string;
  apellidos: string;
}

export interface AsignaturaCatalogoEmbed {
  id: number;
  codigo: string;
  nombre: string;
  ects: number;
  caracter: 'OB' | 'OP' | 'FB';
  curso_plan: number;
}

export interface AsignaturaMatriculadaDetalle {
  id: number;
  n_matricula: number;
  asignatura: AsignaturaCatalogoEmbed;
}

export interface MatriculaDetalle {
  id: number;
  alumno: AlumnoMin;
  curso_academico: string;
  fecha_importacion: string;
  responsable: ResponsableMin;
  grado: Grado;
  asignaturas_matriculadas: AsignaturaMatriculadaDetalle[];
}

export interface MatriculaListaItem {
  id: number;
  alumno: AlumnoMin;
  curso_academico: string;
  grado: Grado;
  fecha_importacion: string;
  num_asignaturas: number;
}
