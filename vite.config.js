import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    outDir: 'dist',
    assetsDir: 'posts',  // Directorio para assets estáticos
    emptyOutDir: true
  }
})