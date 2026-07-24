import { fileURLToPath, URL } from 'node:url'

import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import Components from 'unplugin-vue-components/vite';
import { PrimeVueResolver } from '@primevue/auto-import-resolver';

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const envDir = fileURLToPath(new URL('../environments', import.meta.url))
  const effectiveMode = process.env.SHORT_ENV ?? mode
  const env = loadEnv(effectiveMode, envDir, '')

  return {
    define: {
      'import.meta.env.BACKEND_URL': JSON.stringify(env.BACKEND_URL),
      'import.meta.env.WS_URL': JSON.stringify(env.WS_URL),
      'import.meta.env.WEBSERVER_URL': JSON.stringify(env.WEBSERVER_URL),
      'import.meta.env.IS_PRODUCTION': JSON.stringify(env.IS_PRODUCTION),
    },
    server: {
      host: '0.0.0.0',
      port: 5173,
    },
    plugins: [
      vue(),
      Components({
        resolvers: [
          PrimeVueResolver()
        ]
      })
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      }
    }
  }
})
