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

export interface AlumnoEnAsignatura {
  id: number;
  username: string;
  nombre: string;
  apellidos: string;
  email: string;
  carnet: string;
  curso_academico: string;
  estado_matricula: string;
}

export interface AsistenciaEnFicha {
  id: number;
  sesion_clase_id: number;
  asignatura_codigo: string;
  fecha: string;
  estado: string;
}

export interface AlumnoDetalle {
  id: number;
  username: string;
  nombre: string;
  apellidos: string;
  email: string;
  activo: boolean;
  asignaturas_matriculadas: AsignaturaMatriculadaDelAlumno[];
  asistencias: AsistenciaEnFicha[];
}
