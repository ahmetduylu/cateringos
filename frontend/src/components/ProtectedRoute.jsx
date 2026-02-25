import { Navigate, useLocation } from "react-router-dom";
import useAuthStore from "../store/authStore";

export default function ProtectedRoute({ children, requiredRole }) {
  const user = useAuthStore((s) => s.user);
  const token = useAuthStore((s) => s.token);
  const location = useLocation();

  if (!token || !user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (requiredRole && user.rol !== requiredRole) {
    return <Navigate to="/havuz" replace />;
  }

  return children;
}
