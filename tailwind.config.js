/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        base: {
          light: '#FAF7F2',
          dark: '#161214',
        },
        surface: {
          light: '#FFFFFF',
          dark: '#1F191C',
        },
        subdued: {
          light: '#F2ECE6',
          dark: '#292226',
        },
        border: {
          subtle: {
            light: '#E7DFD7',
            dark: '#382F34',
          },
          strong: {
            light: '#D4C9C0',
            dark: '#4A3E45',
          }
        },
        text: {
          primary: {
            light: '#2A2325',
            dark: '#F5ECEF',
          },
          secondary: {
            light: '#63585C',
            dark: '#BDB0B6',
          },
          muted: {
            light: '#9B8E93',
            dark: '#82757C',
          }
        },
        accent: {
          50: 'var(--accent-50)',
          100: 'var(--accent-100)',
          200: 'var(--accent-200)',
          300: 'var(--accent-300)',
          400: 'var(--accent-400)',
          500: 'var(--accent-500)',
          600: 'var(--accent-600)',
        }
      },
      fontFamily: {
        sans: ['var(--font-sans)', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
        'xl': '12px',
        '2xl': '18px',
      }
    },
  },
  plugins: [],
}
