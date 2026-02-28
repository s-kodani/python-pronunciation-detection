/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'border': '#d0d0d0',
        'text-secondary': '#6b6b6b',
        'text-tertiary': '#4a4a4a',
        'bg-section': '#fafafa',
        'bg-primary': '#f5f5f5',
        'bg-card': '#ffffff',
        'text-primary': '#2d2d2d',
        'button-primary': '#6b6b6b',
        'button-hover': '#5a5a5a',
      },
      fontFamily: {
        sans: ['Inter', 'Noto Sans JP', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'sans-serif'],
      },
      spacing: {
        'section': '80px',
      },
      boxShadow: {
        'button': '0px 1px 2px 0px rgba(0,0,0,0.05)',
      },
    },
  },
  plugins: [],
}
