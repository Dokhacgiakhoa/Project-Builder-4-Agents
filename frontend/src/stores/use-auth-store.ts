import { create } from 'zustand';

export interface User {
  id: string;
  email: string;
  fullName: string;
  role: 'admin' | 'user' | 'guest';
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (user: User, token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null,
  isAuthenticated: typeof window !== 'undefined' ? Boolean(localStorage.getItem('auth_token')) : false,
  
  login: (user, token) => {
    try {
      localStorage.setItem('auth_token', token);
    } catch {}
    set({ user, token, isAuthenticated: true });
  },

  logout: () => {
    try {
      localStorage.removeItem('auth_token');
    } catch {}
    set({ user: null, token: null, isAuthenticated: false });
  },
}));
