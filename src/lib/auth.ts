export interface UserProfile {
  id: string;
  name: string;
  username: string;
  email: string;
  phone?: string;
  avatarUrl?: string;
  plan: 'free' | 'plus' | 'pro';
  createdAt: string;
}

export interface AuthSession {
  user: UserProfile | null;
  token: string | null;
  accounts: UserProfile[]; // For multi-account switching
}

const STORAGE_KEY = 'meena_auth_session';

export const authService = {
  getSession(): AuthSession {
    if (typeof window === 'undefined') {
      return { user: null, token: null, accounts: [] };
    }
    const data = localStorage.getItem(STORAGE_KEY);
    if (!data) {
      return { user: null, token: null, accounts: [] };
    }
    try {
      return JSON.parse(data);
    } catch {
      return { user: null, token: null, accounts: [] };
    }
  },

  setSession(user: UserProfile, token: string) {
    if (typeof window === 'undefined') return;
    const current = this.getSession();
    const existingAccounts = current.accounts || [];
    const accounts = [
      user,
      ...existingAccounts.filter((a) => a.email !== user.email)
    ];

    const session: AuthSession = { user, token, accounts };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(session));
  },

  logout() {
    if (typeof window === 'undefined') return;
    localStorage.removeItem(STORAGE_KEY);
    // Clear user cached messages or temporary session flags
    sessionStorage.clear();
  },

  switchAccount(email: string): UserProfile | null {
    if (typeof window === 'undefined') return null;
    const session = this.getSession();
    const target = session.accounts.find((a) => a.email === email);
    if (target) {
      this.setSession(target, `token_${Date.now()}`);
      return target;
    }
    return null;
  },

  updatePlan(plan: 'free' | 'plus' | 'pro') {
    if (typeof window === 'undefined') return;
    const session = this.getSession();
    if (session.user) {
      session.user.plan = plan;
      session.accounts = session.accounts.map((acc) =>
        acc.email === session.user?.email ? { ...acc, plan } : acc
      );
      localStorage.setItem(STORAGE_KEY, JSON.stringify(session));
    }
  }
};
