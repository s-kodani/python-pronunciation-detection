/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'border': '#e6e6e6',
        'text-secondary': '#828282',
        'text-tertiary': '#454545',
        'bg-section': '#f7f7f7',
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
