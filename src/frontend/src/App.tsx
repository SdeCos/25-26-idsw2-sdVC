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
import { ImportarListasAlumnosPage } from './pages/ImportarListasAlumnosPage';
import { MatriculasPage } from './pages/MatriculasPage';
import { ImportarMatriculasPage } from './pages/ImportarMatriculasPage';
import { ConsultarDetalleMatriculaPage } from './pages/ConsultarDetalleMatriculaPage';
import { CrearSolicitudDispensaSecretariaPage } from './pages/CrearSolicitudDispensaSecretariaPage';
import { Layout } from './components/Layout';
import { RequireAuth } from './components/RequireAuth';
import type { TipoUsuario } from './types/auth';

const gate = (roles: TipoUsuario[], page: React.ReactNode) => (
  <RequireAuth roles={roles}>
    <Layout>{page}</Layout>
  </RequireAuth>
);

const adminOnly = (page: React.ReactNode) => gate(['administrador'], page);
const directorOnly = (page: React.ReactNode) => gate(['director'], page);
const secretariaOnly = (page: React.ReactNode) => gate(['secretaria'], page);
const alumnoOSecretaria = (page: React.ReactNode) =>
  gate(['alumno', 'secretaria'], page);
const lectura = (page: React.ReactNode) =>
  gate(['alumno', 'director', 'secretaria'], page);

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

    {/* Secretaria — alumnos y matrículas */}
    <Route path="/alumnos" element={secretariaOnly(<AlumnosPage />)} />
    <Route path="/alumnos/importar" element={secretariaOnly(<ImportarListasAlumnosPage />)} />
    <Route path="/matriculas" element={secretariaOnly(<MatriculasPage />)} />
    <Route path="/matriculas/importar" element={secretariaOnly(<ImportarMatriculasPage />)} />
    <Route path="/matriculas/:id" element={secretariaOnly(<ConsultarDetalleMatriculaPage />)} />

    {/* Dispensas — abiertas a los tres roles */}
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
