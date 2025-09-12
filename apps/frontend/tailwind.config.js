/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}'
  ],
  theme: {
    extend: {
      fontFamily: {
        satoshi: ['Satoshi-Medium', 'Helvetica', 'Arial', 'sans-serif'],
        'satoshi-bold': ['Satoshi-Bold', 'Helvetica', 'Arial', 'sans-serif'],
      },
      colors: {
        // Will be bridged via CSS variables to keep theme toggle logic
        primary: 'var(--primary)',
        secondary: 'var(--secondary)',
        accent: 'var(--accent)',
        neutralBg: 'var(--neutral)',
        delete: {
          red: 'var(--delete-red)',
          white: 'var(--delete-white)'
        }
      },
      keyframes: {
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' }
        }
      },
      animation: {
        fadeInUp: 'fadeInUp 0.3s ease-out forwards'
      }
    }
  },
  plugins: []
};
