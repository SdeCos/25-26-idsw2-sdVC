import React from 'react';
import { Navigate, Route, Routes } from 'react-router-dom';
import { LoginPage } from './pages/LoginPage';
import { DashboardPage } from './pages/DashboardPage';
import { UsuariosPage } from './pages/UsuariosPage';
import { CrearUsuarioPage } from './pages/CrearUsuarioPage';
import { ConsultarUsuarioPage } from './pages/ConsultarUsuarioPage';
import { EditarUsuarioPage } from './pages/EditarUsuarioPage';
import { DispensasPage } from './pages/DispensasPage';
import { ConsultarDispensaPage } from './pages/ConsultarDispensaPage';
import { EmitirVeredictoPage } from './pages/EmitirVeredictoPage';
import { CrearSolicitudPage } from './pages/CrearSolicitudPage';
import { EditarSolicitudPage } from './pages/EditarSolicitudPage';
import { AlumnosPage } from './pages/AlumnosPage';
import { CrearAlumnoPage } from './pages/CrearAlumnoPage';
import { ImportarListasAlumnosPage } from './pages/ImportarListasAlumnosPage';
import { MatriculasPage } from './pages/MatriculasPage';
import { ImportarMatriculasPage } from './pages/ImportarMatriculasPage';
import { ConsultarDetalleMatriculaPage } from './pages/ConsultarDetalleMatriculaPage';
import { CrearSolicitudDispensaSecretariaPage } from './pages/CrearSolicitudDispensaSecretariaPage';
import { SesionesClasePage } from './pages/SesionesClasePage';
import { CrearSesionClasePage } from './pages/CrearSesionClasePage';
import { SesionClaseActivaPage } from './pages/SesionClaseActivaPage';
import { ListaAlumnosPage } from './pages/ListaAlumnosPage';
import { DetalleAlumnoPage } from './pages/DetalleAlumnoPage';
import { GradosPage } from './pages/GradosPage';
import { AsignaturasPage } from './pages/AsignaturasPage';
import { AsignarAsignaturasProfesorPage } from './pages/AsignarAsignaturasProfesorPage';
import { Layout } from './components/Layout';
import { RequireAuth } from './components/RequireAuth';
import { useAuth } from './context/AuthContext';
import type { TipoUsuario } from './types/auth';

const gate = (roles: TipoUsuario[], page: React.ReactNode) => (
  <RequireAuth roles={roles}>
    <Layout>{page}</Layout>
  </RequireAuth>
);

const adminOnly = (page: React.ReactNode) => gate(['administrador'], page);
const directorOnly = (page: React.ReactNode) => gate(['director'], page);
const secretariaOnly = (page: React.ReactNode) => gate(['secretaria'], page);
const profesorOnly = (page: React.ReactNode) => gate(['profesor'], page);
const alumnoOSecretaria = (page: React.ReactNode) =>
  gate(['alumno', 'secretaria'], page);
const profesorOSecretaria = (page: React.ReactNode) =>
  gate(['profesor', 'secretaria'], page);
const lectura = (page: React.ReactNode) =>
  gate(['alumno', 'director', 'secretaria', 'profesor'], page);

export const App: React.FC = () => (
  <Routes>
    <Route path="/login" element={<LoginPage />} />
    <Route
      path="/dashboard"
      element={
        <RequireAuth>
          <Layout>
            <DashboardPage />
          </Layout>
        </RequireAuth>
      }
    />
    {/* Administrador */}
    <Route path="/usuarios" element={adminOnly(<UsuariosPage />)} />
    <Route path="/usuarios/nuevo" element={adminOnly(<CrearUsuarioPage />)} />
    <Route path="/usuarios/:id" element={adminOnly(<ConsultarUsuarioPage />)} />
    <Route path="/usuarios/:id/editar" element={adminOnly(<EditarUsuarioPage />)} />

    {/* Alumnos — Secretaria (listado paginado) y Profesor (por asignatura) */}
    <Route path="/alumnos" element={profesorOSecretariaOAlumnosPage()} />
    <Route path="/alumnos/nuevo" element={secretariaOnly(<CrearAlumnoPage />)} />
    <Route path="/alumnos/importar" element={secretariaOnly(<ImportarListasAlumnosPage />)} />
    <Route path="/alumnos/:id" element={profesorOSecretaria(<DetalleAlumnoPage />)} />

    {/* Grados — Secretaria (catálogo global) */}
    <Route path="/grados" element={secretariaOnly(<GradosPage />)} />

    {/* Asignaturas y asignaciones — Secretaria */}
    <Route path="/asignaturas" element={secretariaOnly(<AsignaturasPage />)} />
    <Route
      path="/asignaciones"
      element={secretariaOnly(<AsignarAsignaturasProfesorPage />)}
    />

    {/* Matrículas — Secretaria */}
    <Route path="/matriculas" element={secretariaOnly(<MatriculasPage />)} />
    <Route path="/matriculas/importar" element={secretariaOnly(<ImportarMatriculasPage />)} />
    <Route path="/matriculas/:id" element={secretariaOnly(<ConsultarDetalleMatriculaPage />)} />

    {/* Profesor — Sesiones de clase */}
    <Route path="/sesiones-clase" element={profesorOnly(<SesionesClasePage />)} />
    <Route path="/sesiones-clase/nuevo" element={profesorOnly(<CrearSesionClasePage />)} />
    <Route path="/sesiones-clase/:id" element={profesorOnly(<SesionClaseActivaPage />)} />

    {/* Dispensas — abiertas a los cuatro roles */}
    <Route path="/dispensas" element={lectura(<DispensasPage />)} />
    <Route path="/dispensas/nuevo" element={gate(['alumno'], <CrearSolicitudPage />)} />
    <Route
      path="/dispensas/nuevo-en-nombre-de"
      element={secretariaOnly(<CrearSolicitudDispensaSecretariaPage />)}
    />
    <Route path="/dispensas/:id" element={lectura(<ConsultarDispensaPage />)} />
    <Route
      path="/dispensas/:id/editar"
      element={alumnoOSecretaria(<EditarSolicitudPage />)}
    />
    <Route path="/dispensas/:id/veredicto" element={directorOnly(<EmitirVeredictoPage />)} />

    <Route path="*" element={<Navigate to="/dashboard" replace />} />
  </Routes>
);

// Bifurcación en /alumnos: la Secretaria ve `AlumnosPage` (búsqueda libre);
// el Profesor ve `ListaAlumnosPage` (con pestañas por asignatura).
function profesorOSecretariaOAlumnosPage(): React.ReactNode {
  return (
    <RequireAuth roles={['profesor', 'secretaria']}>
      <Layout>
        <BifurcacionAlumnos />
      </Layout>
    </RequireAuth>
  );
}

const BifurcacionAlumnos: React.FC = () => {
  const { usuario } = useAuth();
  if (usuario?.tipo === 'profesor') return <ListaAlumnosPage />;
  return <AlumnosPage />;
};
