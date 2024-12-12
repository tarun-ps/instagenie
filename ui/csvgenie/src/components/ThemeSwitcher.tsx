import React from 'react';
import { useTheme } from '@/context/ThemeContext';

const ThemeSwitcher: React.FC = () => {
  const { theme, setTheme } = useTheme();

  return (
    <button onClick={() => setTheme(theme === 'sky' ? 'default' : 'sky')}>
      Switch to {theme === 'sky' ? 'Default' : 'Sky'} Theme
    </button>
  );
};

export default ThemeSwitcher; 