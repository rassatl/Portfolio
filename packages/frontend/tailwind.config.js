/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'pastel-blue': '#E0F2FE',
        'pastel-yellow': '#FEF3C7',
        'pastel-red': '#FECACA',
        'pastel-green': '#D1FAE5',
      }
    },
  },
  plugins: [],
}
