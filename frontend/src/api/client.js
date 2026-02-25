import axios from "axios";

const API_BASE = "https://cateringos.onrender.com";

const api = axios.create({
  baseURL: API_BASE,
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      window.location.href = "/login";
    }
    return Promise.reject(err);
  }
);

export const login = (email, password) => api.post("/auth/login", { email, password }).then(r => r.data);
export const getMe = () => api.get("/auth/me").then(r => r.data);
export const createUser = (data) => api.post("/auth/users", data).then(r => r.data);
export const listUsers = () => api.get("/auth/users").then(r => r.data);
export const getPool = (search = "") => api.get("/leads/pool", { params: { search } }).then(r => r.data);
export const assignLead = (lead_id) => api.post("/leads/assign", { lead_id }).then(r => r.data);
export const getMyLeads = (status_filter = "") => api.get("/leads/my-leads", { params: { status_filter } }).then(r => r.data);
export const getLeadDetail = (id) => api.get(`/leads/${id}`).then(r => r.data);
export const updateStatus = (id, status) => api.put(`/leads/${id}/status`, { status }).then(r => r.data);
export const addNote = (id, aciklama) => api.post(`/leads/${id}/note`, { aciklama }).then(r => r.data);
export const getTeamReport = () => api.get("/reports/team").then(r => r.data);
export const getPoolStats = () => api.get("/reports/pool-stats").then(r => r.data);
export const getDashboard = () => api.get("/reports/dashboard").then(r => r.data);

export default api;
