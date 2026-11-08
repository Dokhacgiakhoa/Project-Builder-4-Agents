import { beforeEach, describe, expect, it } from 'vitest';
import { useAuthStore, type User } from './use-auth-store';

const user: User = { id: '1', email: 'a@b.c', fullName: 'A', role: 'user' };

describe('useAuthStore', () => {
  beforeEach(() => {
    useAuthStore.getState().logout();
  });

  it('login stores the user and marks them authenticated', () => {
    useAuthStore.getState().login(user, 'tok');
    const s = useAuthStore.getState();
    expect(s.isAuthenticated).toBe(true);
    expect(s.token).toBe('tok');
    expect(s.user?.email).toBe('a@b.c');
  });

  it('logout clears all state', () => {
    useAuthStore.getState().login(user, 'tok');
    useAuthStore.getState().logout();
    const s = useAuthStore.getState();
    expect(s.user).toBeNull();
    expect(s.token).toBeNull();
    expect(s.isAuthenticated).toBe(false);
  });

  it('does not crash when localStorage throws', () => {
    const original = window.localStorage;
    Object.defineProperty(window, 'localStorage', {
      configurable: true,
      get() {
        throw new Error('blocked');
      },
    });
    try {
      expect(() => useAuthStore.getState().login(user, 'tok')).not.toThrow();
      expect(useAuthStore.getState().isAuthenticated).toBe(true);
    } finally {
      Object.defineProperty(window, 'localStorage', { configurable: true, value: original });
    }
  });
});
