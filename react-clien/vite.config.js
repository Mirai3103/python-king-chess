import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import { TanStackRouterVite } from '@tanstack/router-vite-plugin'
// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(), TanStackRouterVite()],
  define: {
    'API_URL': process.env.API_URL || 'localhost:1234',
    'SOCKET_URL': process.env.SOCKET_URL || 'localhost:1234'
  }
})
