import { Link, useLocation } from "react-router-dom";
import useAuthStore from "../store/authStore";

export default function Sidebar() {
  const location = useLocation();
  const user = useAuthStore((s) => s.user);
  const logout = useAuthStore((s) => s.logout);

  const links = [
    { to: "/havuz", label: "Havuz", icon: "📥" },
    { to: "/portfoyum", label: "Portföyüm", icon: "📋" },
  ];

  if (user?.rol === "chief") {
    links.push({ to: "/yonetim", label: "Yönetim", icon: "📊" });
  }

  return (
    <div className="w-64 bg-white border-r h-full flex flex-col">
      <div className="p-4 border-b">
        <h1 className="text-xl font-bold text-blue-600">LocalCateringOS</h1>
        <p className="text-xs text-gray-500 mt-1">Hoş geldin, {user?.ad}</p>
      </div>
      <nav className="flex-1 p-4 space-y-1">
        {links.map((l) => (
          <Link key={l.to} to={l.to} className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${location.pathname === l.to ? "bg-blue-50 text-blue-600" : "text-gray-600 hover:bg-gray-100"}`}>
            <span>{l.icon}</span>
            <span className="font-medium">{l.label}</span>
          </Link>
        ))}
      </nav>
      <div className="p-4 border-t">
        <button onClick={logout} className="w-full text-left px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors">Çıkış Yap</button>
      </div>
    </div>
  );
}
