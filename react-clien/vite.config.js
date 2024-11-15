import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import { TanStackRouterVite } from '@tanstack/router-vite-plugin'
// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(), TanStackRouterVite()],
  define: {
    'process.env':JSON.stringify({
      'SOCKET_URL':process.env.SOCKET_URL||'ws://localhost:1234',
      'API_URL':process.env.API_URL||'http://localhost:1234',
    }),
  }
})
