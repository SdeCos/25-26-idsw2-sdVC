# Diseño — Casos de uso

Diagramas de secuencia por caso de uso. Cada CU lleva los participantes concretos (componente React, endpoint FastAPI, servicio, repositorio, BD) y las decisiones de diseño que materializan el análisis.

## Estado

| Caso de uso | Actor | Diseño |
|---|---|---|
| [iniciarSesion()](iniciarSesion/README.md) | Usuario | ✅ |
| [cerrarSesion()](cerrarSesion/README.md) | Usuario | ✅ |
| crearUsuario() | Administrador | ⏳ |
| consultarUsuario() | Administrador | ⏳ |
| editarUsuario() | Administrador | ⏳ |
| consultarListaAlumnos() | Profesor | ⏳ |
| consultarDetalleAlumno() | Profesor | ⏳ |
| crearSesionClase() | Profesor | ⏳ |
| editarSesionClase() | Profesor | ⏳ |
| registrarTomaAsistencia() | Profesor | ⏳ |
| cerrarSesionClase() | Profesor | ⏳ |
| exportarHistorialAsistencias() | Profesor | ⏳ |
| consultarSolicitudDispensa() (Profesor) | Profesor | ⏳ |
| crearSolicitudDispensa() (Alumno) | Alumno | ⏳ |
| editarSolicitudDispensa() (Alumno) | Alumno | ⏳ |
| consultarSolicitudDispensa() (Alumno) | Alumno | ⏳ |
| consultarSolicitudesDispensas() | DirectorDeGrado | ⏳ |
| editarSolicitudDispensa() (Director) | DirectorDeGrado | ⏳ |
| consultarListaAlumnos() (Secretaria) | Secretaria | ⏳ |
| consultarDetalleMatricula() | Secretaria | ⏳ |
| importarListasAlumnos() | Secretaria | ⏳ |
| importarMatriculas() | Secretaria | ⏳ |
| crearSolicitudDispensa() (Secretaria) | Secretaria | ⏳ |
| editarSolicitudDispensa() (Secretaria) | Secretaria | ⏳ |
| consultarSolicitudDispensa() (Secretaria) | Secretaria | ⏳ |
| exportarDispensas() | Secretaria | ⏳ |

**Progreso:** 2/26
