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

const TOKEN_KEY = 'auth_token';

/** Truy cập localStorage an toàn (có thể ném lỗi ở private mode / bị chặn). */
const storage = {
  get(): string | null {
    try {
      return typeof window !== 'undefined' ? window.localStorage.getItem(TOKEN_KEY) : null;
    } catch (error) {
      console.warn('[auth-store] Không đọc được token:', error);
      return null;
    }
  },
  set(token: string): void {
    try {
      window.localStorage.setItem(TOKEN_KEY, token);
    } catch (error) {
      console.warn('[auth-store] Không lưu được token:', error);
    }
  },
  remove(): void {
    try {
      window.localStorage.removeItem(TOKEN_KEY);
    } catch (error) {
      console.warn('[auth-store] Không xóa được token:', error);
    }
  },
};

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: storage.get(),
  isAuthenticated: Boolean(storage.get()),

  login: (user, token) => {
    storage.set(token);
    set({ user, token, isAuthenticated: true });
  },

  logout: () => {
    storage.remove();
    set({ user: null, token: null, isAuthenticated: false });
  },
}));
