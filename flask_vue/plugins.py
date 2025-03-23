"""
Module plugins pour l'extension Flask-Vue.
Gère l'intégration des plugins Vue comme Vue Router et Pinia.
"""

# Template pour Vue Router (routes.js)
VUE_ROUTER_TEMPLATE = """
import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import About from '../views/About.vue'
import NotFound from '../views/NotFound.vue'
import ErrorPage from '../views/ErrorPage.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    component: About
  },
  {
    path: '/error',
    name: 'Error',
    component: ErrorPage,
    props: true
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Gestion des erreurs globales
router.onError((error) => {
  console.error('Erreur de routage:', error)
  router.push({ 
    name: 'Error', 
    params: { error: "Une erreur s'est produite lors du chargement de la page." } 
  })
})

export default router
"""

# Template pour Vue Router (App.vue avec router)
VUE_ROUTER_APP_TEMPLATE = """
<template>
  <div class="flex min-h-screen flex-col bg-gray-50">
    <header class="bg-white shadow">
      <div class="container mx-auto p-4">
        <nav class="flex space-x-4">
          <router-link to="/" class="text-gray-800 hover:text-blue-500">Accueil</router-link>
          <router-link to="/about" class="text-gray-800 hover:text-blue-500">À propos</router-link>
        </nav>
      </div>
    </header>
    
    <main class="container mx-auto flex-1 p-4">
      <router-view></router-view>
    </main>
    
    <footer class="bg-gray-100 border-t">
      <div class="container mx-auto p-4 text-center text-gray-600">
        Flask-Vue Application
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>
"""

# Template pour Home.vue
VUE_ROUTER_HOME_TEMPLATE = """
<template>
  <div class="rounded-xl bg-white p-8 shadow-md">
    <h1 class="mb-4 text-2xl font-bold text-gray-800">
      Bienvenue sur votre application Flask-Vue !
    </h1>
    
    <p class="mb-6 text-gray-600">
      Cette page est rendue par Vue 3 avec Vue Router et Tailwind CSS.
    </p>
    
    <HelloWorld>
      <button class="rounded bg-blue-500 px-4 py-2 font-bold text-white hover:bg-blue-700">
        Connecté à Flask
      </button>
    </HelloWorld>
  </div>
</template>

<script>
import HelloWorld from '../components/HelloWorld.vue'

export default {
  name: 'Home',
  components: {
    HelloWorld
  }
}
</script>
"""

# Template pour About.vue
VUE_ROUTER_ABOUT_TEMPLATE = """
<template>
  <div class="rounded-xl bg-white p-8 shadow-md">
    <h1 class="mb-4 text-2xl font-bold text-gray-800">À propos</h1>
    
    <p class="mb-4 text-gray-600">
      Cette application est construite avec Flask-Vue, intégrant:
    </p>
    
    <ul class="list-disc pl-6 mb-6">
      <li>Flask comme backend</li>
      <li>Vue 3 comme framework frontend</li>
      <li>Vite pour le développement rapide</li>
      <li>Vue Router pour la navigation</li>
      <li>Tailwind CSS 4 pour le style</li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'About'
}
</script>
"""

# Template pour NotFound.vue (404)
VUE_ROUTER_NOTFOUND_TEMPLATE = """
<template>
  <div class="rounded-xl bg-white p-8 shadow-md">
    <div class="flex flex-col items-center">
      <h1 class="mb-4 text-9xl font-bold text-gray-800">404</h1>
      <h2 class="mb-6 text-3xl font-semibold text-gray-600">Page non trouvée</h2>
      
      <p class="mb-6 text-center text-gray-600">
        La page que vous recherchez n'existe pas ou a été déplacée.
      </p>
      
      <router-link to="/" class="rounded bg-blue-500 px-4 py-2 font-bold text-white hover:bg-blue-700">
        Retour à l'accueil
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFound'
}
</script>
"""

# Template pour ErrorPage.vue
VUE_ROUTER_ERROR_TEMPLATE = """
<template>
  <div class="rounded-xl bg-white p-8 shadow-md">
    <div class="flex flex-col items-center">
      <svg class="mb-4 h-16 w-16 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
      </svg>
      
      <h1 class="mb-4 text-2xl font-bold text-gray-800">Une erreur s'est produite</h1>
      
      <p class="mb-6 text-center text-gray-600">
        {{ errorMessage }}
      </p>
      
      <div class="flex space-x-4">
        <button @click="goBack" class="rounded bg-gray-500 px-4 py-2 font-bold text-white hover:bg-gray-700">
          Retour
        </button>
        
        <router-link to="/" class="rounded bg-blue-500 px-4 py-2 font-bold text-white hover:bg-blue-700">
          Accueil
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ErrorPage',
  props: {
    error: {
      type: String,
      default: "Une erreur inconnue s'est produite."
    }
  },
  computed: {
    errorMessage() {
      return this.error || "Une erreur inconnue s'est produite.";
    }
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    }
  }
}
</script>
"""

# Template pour Pinia store
PINIA_STORE_TEMPLATE = """
import { defineStore } from 'pinia'

// Définition du store utilisateur
export const useUserStore = defineStore('user', {
  // État initial
  state: () => ({
    user: null,
    isAuthenticated: false,
    loading: false
  }),
  
  // Getters
  getters: {
    username: (state) => state.user?.username || 'Invité'
  },
  
  // Actions
  actions: {
    async login(username, password) {
      this.loading = true
      
      try {
        // Simulation d'une requête API
        // En production, utilisez fetch pour appeler votre API Flask
        await new Promise(resolve => setTimeout(resolve, 500))
        
        // Simuler une connexion réussie
        this.user = { username, id: 1 }
        this.isAuthenticated = true
        
        return true
      } catch (error) {
        console.error('Erreur de connexion:', error)
        return false
      } finally {
        this.loading = false
      }
    },
    
    logout() {
      this.user = null
      this.isAuthenticated = false
    }
  }
})

// Définition du store counter pour exemple
export const useCounterStore = defineStore('counter', {
  state: () => ({
    count: 0
  }),
  actions: {
    increment() {
      this.count++
    },
    decrement() {
      this.count--
    }
  }
})
"""

# Template pour main.js avec Vue Router
VUE_ROUTER_MAIN_TEMPLATE = """
// Fichier main.js - Point d'entrée de l'application
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './style.css'

createApp(App)
  .use(router)
  .mount('#app')
"""

# Template pour main.js avec Pinia
PINIA_MAIN_TEMPLATE = """
// Fichier main.js - Point d'entrée de l'application
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import './style.css'

const app = createApp(App)
app.use(createPinia())
app.mount('#app')
"""

# Template pour main.js avec Vue Router et Pinia
ROUTER_PINIA_MAIN_TEMPLATE = """
// Fichier main.js - Point d'entrée de l'application
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './style.css'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
"""

# Template pour package.json avec Vue Router
VUE_ROUTER_PACKAGE_JSON = """
  "dependencies": {
    "vue": "^3.3.4",
    "vue-router": "^4.2.4"
  }
"""

# Template pour package.json avec Pinia
PINIA_PACKAGE_JSON = """
  "dependencies": {
    "vue": "^3.3.4",
    "pinia": "^2.1.6"
  }
"""

# Template pour package.json avec Vue Router et Pinia
ROUTER_PINIA_PACKAGE_JSON = """
  "dependencies": {
    "vue": "^3.3.4",
    "vue-router": "^4.2.4",
    "pinia": "^2.1.6"
  }
"""

def configure_vue_router(path, package_json_content):
    """Configure Vue Router dans un projet Vue existant"""
    import os
    import json
    
    # Mettre à jour package.json pour ajouter vue-router
    try:
        package_data = json.loads(package_json_content)
        if 'vue-router' not in package_data.get('dependencies', {}):
            # Ajouter vue-router aux dépendances
            package_data['dependencies']['vue-router'] = "^4.2.4"
        
        # Réécrire le fichier package.json
        return json.dumps(package_data, indent=2)
    except json.JSONDecodeError:
        # En cas d'erreur, utiliser un remplacement simple
        return package_json_content.replace(
            '"dependencies": {\n    "vue": "^3.3.4"',
            '"dependencies": {\n    "vue": "^3.3.4",\n    "vue-router": "^4.2.4"'
        )

def configure_pinia(path, package_json_content):
    """Configure Pinia dans un projet Vue existant"""
    import os
    import json
    
    # Mettre à jour package.json pour ajouter pinia
    try:
        package_data = json.loads(package_json_content)
        if 'pinia' not in package_data.get('dependencies', {}):
            # Ajouter pinia aux dépendances
            package_data['dependencies']['pinia'] = "^2.1.6"
        
        # Réécrire le fichier package.json
        return json.dumps(package_data, indent=2)
    except json.JSONDecodeError:
        # En cas d'erreur, utiliser un remplacement simple
        return package_json_content.replace(
            '"dependencies": {\n    "vue": "^3.3.4"',
            '"dependencies": {\n    "vue": "^3.3.4",\n    "pinia": "^2.1.6"'
        )

def add_vue_router_files(path):
    """Ajoute les fichiers nécessaires pour Vue Router"""
    import os
    
    # Créer le dossier router
    router_dir = os.path.join(path, 'src', 'router')
    os.makedirs(router_dir, exist_ok=True)
    
    # Créer le dossier views
    views_dir = os.path.join(path, 'src', 'views')
    os.makedirs(views_dir, exist_ok=True)
    
    # Ajouter le fichier router/index.js
    with open(os.path.join(router_dir, 'index.js'), 'w') as f:
        f.write(VUE_ROUTER_TEMPLATE.strip())
    
    # Ajouter les vues
    with open(os.path.join(views_dir, 'Home.vue'), 'w') as f:
        f.write(VUE_ROUTER_HOME_TEMPLATE.strip())
        
    with open(os.path.join(views_dir, 'About.vue'), 'w') as f:
        f.write(VUE_ROUTER_ABOUT_TEMPLATE.strip())
    
    # Ajouter les pages d'erreur
    with open(os.path.join(views_dir, 'NotFound.vue'), 'w') as f:
        f.write(VUE_ROUTER_NOTFOUND_TEMPLATE.strip())
    
    with open(os.path.join(views_dir, 'ErrorPage.vue'), 'w') as f:
        f.write(VUE_ROUTER_ERROR_TEMPLATE.strip())
    
    return True

def add_pinia_files(path):
    """Ajoute les fichiers nécessaires pour Pinia"""
    import os
    
    # Créer le dossier store
    store_dir = os.path.join(path, 'src', 'store')
    os.makedirs(store_dir, exist_ok=True)
    
    # Ajouter le fichier store/index.js
    with open(os.path.join(store_dir, 'index.js'), 'w') as f:
        f.write(PINIA_STORE_TEMPLATE.strip())
    
    return True

def get_main_js_template(router=False, pinia=False):
    """Retourne le template main.js approprié en fonction des plugins"""
    if router and pinia:
        return ROUTER_PINIA_MAIN_TEMPLATE
    elif router:
        return VUE_ROUTER_MAIN_TEMPLATE
    elif pinia:
        return PINIA_MAIN_TEMPLATE
    else:
        return None  # Template par défaut

def get_app_vue_template(router=False):
    """Retourne le template App.vue approprié en fonction des plugins"""
    if router:
        return VUE_ROUTER_APP_TEMPLATE
    else:
        return None  # Template par défaut