"""
Configuration pour l'extension Flask-Vue.
Contient les templates et paramètres par défaut.
"""

# Template pour la configuration Vite avec Vue 3 et Tailwind CSS 4
# Note: outDir sera remplacé dynamiquement lors de l'initialisation
VITE_CONFIG_TEMPLATE = """
// vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [vue(), tailwindcss()],
  build: {
    // Générer le manifeste pour Flask
    manifest: true,
    
    // Définir le répertoire de sortie (sera ajusté dynamiquement)
    outDir: '../static/build',
    
    // Configurer les chemins pour qu'ils fonctionnent avec Flask sans hash
    rollupOptions: {
      input: {
        main: 'src/main.js',
      },
      output: {
        // Désactiver le hachage des noms de fichiers
        entryFileNames: '[name].js',
        chunkFileNames: '[name].js',
        assetFileNames: '[name].[ext]'
      }
    }
  },
  
  // En mode dev, serveur proxy vers Flask
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  }
})
"""

# Template minimal pour package.json avec Vue 3 et Tailwind CSS 4
PACKAGE_JSON_TEMPLATE = """
{
  "name": "flask-vue-app",
  "version": "0.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.3.4"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.0",
    "vite": "^5.2.0",
    "tailwindcss": "^4.0.0",
    "@tailwindcss/vite": "^4.0.0"
  }
}
"""

# Template HTML minimal pour Vue 3
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Flask + Vue 3 + Tailwind CSS</title>
</head>
<body>
  <div id="app"></div>
  <script type="module" src="/src/main.js"></script>
</body>
</html>
"""

# Template JavaScript minimal avec Vue 3
JS_TEMPLATE = """
// Fichier main.js - Point d'entrée de l'application
import { createApp } from 'vue'
import App from './App.vue'
import './style.css'

createApp(App).mount('#app')
"""

# Template App.vue pour Vue 3
APP_VUE_TEMPLATE = """
<template>
  <div class="flex min-h-screen flex-col items-center justify-center bg-gray-50 p-4">
    <div class="w-full max-w-md">
      <div class="rounded-xl bg-white p-8 shadow-md">
        <h1 class="mb-4 text-2xl font-bold text-gray-800">
          Bienvenue sur votre application Flask-Vue !
        </h1>
        
        <p class="mb-6 text-gray-600">
          Cette page est rendue par Vue 3 avec Tailwind CSS.
          Vous pouvez maintenant commencer à développer votre application.
        </p>
        
        <HelloWorld>
          <button class="rounded bg-blue-500 px-4 py-2 font-bold text-white hover:bg-blue-700">
            Connecté à Flask
          </button>
        </HelloWorld>
      </div>
    </div>
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'App',
  components: {
    HelloWorld
  }
}
</script>
"""

# Template CSS minimal avec Tailwind CSS 4
CSS_TEMPLATE = """
/* Import Tailwind CSS */
@import 'tailwindcss';

/* Styles personnalisés supplémentaires si nécessaire */
"""

# Paramètres par défaut pour l'extension
# Note: static_url_path sera configuré dans init_app car current_app n'est pas disponible à l'importation
DEFAULT_SETTINGS = {
    'static_url_path': '/static',  # Sera mis à jour dans init_app
    'assets_path': 'build/',
    'manifest_path': '.vite/manifest.json',
    'dev_server_url': 'http://localhost:5173',
    'entry_map': {
        'main.js': 'src/main.js',
        'main.css': 'src/style.css'
    },
    'plugins': {
        'vue_router': False,
        'pinia': False
    }
}