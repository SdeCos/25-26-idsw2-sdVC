# Desarrollo — Casos de uso

Implementación de cada caso de uso bajo [`/src`](/src/), con un README de trazabilidad código ↔ diseño.

## Estado

| Caso de uso | Actor | Desarrollo |
|---|---|---|
| [iniciarSesion()](iniciarSesion/README.md) | Usuario | ✅ |
| [cerrarSesion()](cerrarSesion/README.md) | Usuario | ✅ |
| [crearUsuario()](crearUsuario/README.md) | Administrador | ✅ |
| [consultarUsuario()](consultarUsuario/README.md) | Administrador | ✅ |
| [editarUsuario()](editarUsuario/README.md) | Administrador | ✅ |
| consultarListaAlumnos() | Profesor | ⏳ |
| consultarDetalleAlumno() | Profesor | ⏳ |
| crearSesionClase() | Profesor | ⏳ |
| editarSesionClase() | Profesor | ⏳ |
| registrarTomaAsistencia() | Profesor | ⏳ |
| cerrarSesionClase() | Profesor | ⏳ |
| exportarHistorialAsistencias() | Profesor | ⏳ |
| consultarSolicitudDispensa() (Profesor) | Profesor | ⏳ |
| [crearSolicitudDispensa() (Alumno)](crearSolicitudDispensa/README.md) | Alumno | ✅ |
| [editarSolicitudDispensa() (Alumno)](editarSolicitudDispensa/README.md) | Alumno | ✅ |
| [consultarSolicitudDispensa() (Alumno)](consultarSolicitudDispensa/README.md) | Alumno | ✅ |
| [consultarSolicitudesDispensas()](consultarSolicitudesDispensas/README.md) | DirectorDeGrado | ✅ |
| [editarSolicitudDispensa() (Director)](editarSolicitudDispensaDirector/README.md) | DirectorDeGrado | ✅ |
| consultarListaAlumnos() (Secretaria) | Secretaria | ⏳ |
| consultarDetalleMatricula() | Secretaria | ⏳ |
| importarListasAlumnos() | Secretaria | ⏳ |
| importarMatriculas() | Secretaria | ⏳ |
| crearSolicitudDispensa() (Secretaria) | Secretaria | ⏳ |
| editarSolicitudDispensa() (Secretaria) | Secretaria | ⏳ |
| consultarSolicitudDispensa() (Secretaria) | Secretaria | ⏳ |
| exportarDispensas() | Secretaria | ⏳ |

**Progreso:** 10/26
