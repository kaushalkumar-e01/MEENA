'use client';

import React, { useEffect } from 'react';
import { useMeenaStore, ACCENT_PALETTES } from '@/stores/meenaStore';

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const { preferences } = useMeenaStore();

  useEffect(() => {
    // Theme setup
    const isDark =
      preferences.theme === 'dark' ||
      (preferences.theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches);

    if (isDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }

    // Accent setup
    const palette = ACCENT_PALETTES[preferences.accentColor] || ACCENT_PALETTES.rose;
    Object.entries(palette).forEach(([varName, hex]) => {
      document.documentElement.style.setProperty(varName, hex);
    });

    // Font size setup
    const scaleMap = { small: '14px', default: '15px', large: '17px' };
    document.documentElement.style.fontSize = scaleMap[preferences.fontSize] || '15px';

  }, [preferences.theme, preferences.accentColor, preferences.fontSize]);

  return <>{children}</>;
}
