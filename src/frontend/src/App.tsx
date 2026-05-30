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
const alumnoOnly = (page: React.ReactNode) => gate(['alumno'], page);
const directorOrAlumno = (page: React.ReactNode) => gate(['director', 'alumno'], page);

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
    <Route path="/usuarios" element={adminOnly(<UsuariosPage />)} />
    <Route path="/usuarios/nuevo" element={adminOnly(<CrearUsuarioPage />)} />
    <Route path="/usuarios/:id" element={adminOnly(<ConsultarUsuarioPage />)} />
    <Route path="/usuarios/:id/editar" element={adminOnly(<EditarUsuarioPage />)} />
    <Route path="/dispensas" element={directorOrAlumno(<DispensasPage />)} />
    <Route path="/dispensas/nuevo" element={alumnoOnly(<CrearSolicitudPage />)} />
    <Route path="/dispensas/:id" element={directorOrAlumno(<ConsultarDispensaPage />)} />
    <Route path="/dispensas/:id/editar" element={alumnoOnly(<EditarSolicitudPage />)} />
    <Route path="/dispensas/:id/veredicto" element={directorOnly(<EmitirVeredictoPage />)} />
    <Route path="*" element={<Navigate to="/dashboard" replace />} />
  </Routes>
);
