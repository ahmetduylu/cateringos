import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Pool from "./pages/Pool";
import MyLeads from "./pages/MyLeads";
import ChiefDashboard from "./pages/ChiefDashboard";
import Layout from "./components/Layout";
import ProtectedRoute from "./components/ProtectedRoute";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public */}
        <Route path="/login" element={<Login />} />

        {/* Protected — tüm roller */}
        <Route element={<ProtectedRoute />}>
          <Route element={<Layout />}>
            <Route path="/havuz" element={<Pool />} />
            <Route path="/portfoyum" element={<MyLeads />} />

            {/* Sadece chief */}
            <Route element={<ProtectedRoute requiredRole="chief" />}>
              <Route path="/yonetim" element={<ChiefDashboard />} />
            </Route>
          </Route>
        </Route>

        {/* Varsayılan yönlendirme */}
        <Route path="/" element={<Navigate to="/havuz" replace />} />
        <Route path="*" element={<Navigate to="/havuz" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
