import { create } from "zustand";

const stored = localStorage.getItem("user");
const storedToken = localStorage.getItem("token");

const useAuthStore = create((set) => ({
  user: stored ? JSON.parse(stored) : null,
  token: storedToken || null,

  setAuth: (user, token) => {
    localStorage.setItem("user", JSON.stringify(user));
    localStorage.setItem("token", token);
    set({ user, token });
  },

  logout: () => {
    localStorage.removeItem("user");
    localStorage.removeItem("token");
    set({ user: null, token: null });
  },

  isAuthenticated: () => {
    const state = useAuthStore.getState();
    return !!state.token && !!state.user;
  },
}));

export default useAuthStore;
