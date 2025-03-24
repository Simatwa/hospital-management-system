/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#1E40AF',
          50: '#E6EBFA',
          100: '#BFCDF2',
          200: '#99AFE9',
          300: '#7391E1',
          400: '#4D73D8',
          500: '#2755CF',
          600: '#1E40AF',
          700: '#162F82',
          800: '#0F1F55',
          900: '#070E28'
        },
        accent: {
          DEFAULT: '#14B8A6',
          50: '#E7F8F6',
          100: '#B8EBE5',
          200: '#8ADED4',
          300: '#5CD1C3',
          400: '#2EC4B2',
          500: '#14B8A6',
          600: '#0F8C7E',
          700: '#0B6056',
          800: '#06342E',
          900: '#021816'
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif']
      }
    },
  },
  plugins: [],
}