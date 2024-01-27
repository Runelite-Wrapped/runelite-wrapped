import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic':
          'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
      },
    },
    colors: {
      'osrslb': {
        100: '#FFF7E8',
        150: '#FFEDCC',
        200: '#D8BB7D',
        300: '#BBA26C',
        400: '#A58F60',
        500: '#96825A',
        600: '#7F6E4B',
        700: '#60533A',
        800: '#383020',
        900: '#282318'
      },
      'wikibrown': {
        100: '#FFE9CC',
        300: '#C0A886',
        500: '#C0A886',
        700: '#A08C70',
        800: '#54493A',
        900: '#28231C'

      }
    }
  },
  plugins: [],
}
export default config
