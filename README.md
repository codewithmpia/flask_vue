# Flask-Vue

![Flask-Vue](https://via.placeholder.com/800x200/0077be/ffffff?text=Flask+Vue)

Une extension Flask pour intégrer facilement Vue 3, Vite.js et Tailwind CSS 4 dans une application Flask, offrant une expérience de développement moderne pour les applications web full-stack.

## Table des matières

- [Caractéristiques](#caractéristiques)
- [Installation](#installation)
- [Démarrage rapide](#démarrage-rapide)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
  - [Commandes CLI](#commandes-cli)
  - [Helpers Jinja](#helpers-jinja)
  - [Modes de développement et production](#modes-de-développement-et-production)
- [Plugins Vue](#plugins-vue)
  - [Vue Router](#vue-router)
  - [Pinia (Store)](#pinia-store)
- [Architecture](#architecture)
- [Exemples](#exemples)
- [FAQ](#faq)
- [Dépannage](#dépannage)
- [Contribuer](#contribuer)
- [Licence](#licence)

## Caractéristiques

- **Intégration transparente** de Vue 3 dans une application Flask
- **Support du mode développement** avec Hot Module Replacement (HMR)
- **Utilisation de Vite.js** pour un développement frontend rapide et une construction optimisée
- **Intégration de Tailwind CSS 4** pour un styling moderne et efficace
- **Support de Vue Router** avec gestion des erreurs 404 et pages d'erreur
- **Support de Pinia** pour une gestion d'état avancée
- **Outils CLI** pour initialiser, installer, démarrer et construire votre projet Vue
- **Gestion automatique des assets** en production

## Installation

```bash
pip install flask-vue
```

## Démarrage rapide

1. **Dans votre application Flask, initialisez l'extension:**

```python
from flask import Flask
from flask_vue import Vue

app = Flask(__name__)
vue = Vue(app)

# Ou avec la factory pattern
# vue = Vue()
# vue.init_app(app)
```

2. **Initialisez un nouveau projet Vue dans votre application:**

```bash
# Projet Vue basique
flask vue init

# Avec Vue Router
flask vue init --router

# Avec Pinia (state management)
flask vue init --pinia

# Avec Vue Router et Pinia
flask vue init --router --pinia
```

3. **Installez les dépendances JavaScript:**

```bash
flask vue install
```

4. **Démarrez le serveur de développement Vue:**

```bash
flask vue start
```

5. **Dans vos templates Flask, utilisez les helpers Jinja:**

```html
<!DOCTYPE html>
<html>
<head>
    <title>Mon application Flask-Vue</title>
    {{ vue_hmr() }}
    {{ vue_css('main.css') }}
</head>
<body>
    <div id="app"></div>
    {{ vue_js('main.js') }}
</body>
</html>
```

6. **Pour déployer en production, construisez les assets:**

```bash
flask vue build
```

## Configuration

Vous pouvez configurer l'extension via des paramètres lors de l'initialisation:

```python
vue = Vue(app,
    # Mode de développement (si non spécifié, utilise app.config['VUE_MODE'] ou app.debug)
    dev_mode=True,  
    
    # URL du serveur de développement Vite (par défaut: http://localhost:5173)
    dev_server_url='http://localhost:3000',  
    
    # Chemin vers les assets dans le dossier static
    assets_path='vue/',  
    
    # Mappage personnalisé des points d'entrée
    entry_map={  
        'app.js': 'src/app.js',
        'admin.js': 'src/admin.js'
    },
    
    # Activer/désactiver les plugins Vue
    plugins={  
        'vue_router': True,
        'pinia': True
    }
)
```

Ou via les variables d'environnement ou la configuration Flask:

- `FLASK_VUE_MODE`: `development` ou `production`
- Définir `app.config['VUE_MODE']` à `development` ou `production`

## Utilisation

### Commandes CLI

L'extension fournit plusieurs commandes CLI pour gérer votre projet Vue:

- `flask vue init`: Initialise un nouveau projet Vue avec Vite et Tailwind CSS
  - `--router`: Active Vue Router avec pages d'exemple et gestion d'erreurs
  - `--no-router`: Désactive Vue Router (comportement par défaut)
  - `--pinia`: Active Pinia (gestion d'état) avec stores d'exemple
  - `--no-pinia`: Désactive Pinia (comportement par défaut)
  - `--path/-p`: Spécifie le chemin où initialiser le projet (défaut: `frontend`)
- `flask vue install`: Installe les dépendances NPM
  - `--path/-p`: Spécifie le chemin du projet (défaut: `frontend`)
- `flask vue start`: Démarre le serveur de développement Vite
  - `--path/-p`: Spécifie le chemin du projet (défaut: `frontend`)
- `flask vue build`: Construit les assets Vue pour la production
  - `--path/-p`: Spécifie le chemin du projet (défaut: `frontend`)

### Helpers Jinja

L'extension ajoute plusieurs fonctions d'aide à l'environnement Jinja:

- `vue_hmr()`: Génère la balise script pour le Hot Module Replacement en mode développement
- `vue_js(entry_point)`: Génère la balise script pour un point d'entrée JavaScript
- `vue_css(entry_point)`: Génère les balises CSS pour un point d'entrée
- `vue_asset(filename)`: Génère l'URL pour un asset
- `vue_has_router()`: Vérifie si Vue Router est activé
- `vue_has_pinia()`: Vérifie si Pinia est activé

### Modes de développement et production

**En mode développement:**
- Les assets sont servis depuis le serveur de développement Vite
- Le Hot Module Replacement (HMR) est activé
- Les modifications sont reflétées immédiatement dans le navigateur

**En mode production:**
- Les assets sont compilés via `flask vue build`
- Les fichiers sont optimisés et minifiés
- Les chemins sont simplifiés sans hachage pour une intégration facile avec Flask

## Plugins Vue

### Vue Router

Vue Router permet de créer des applications à page unique (SPA) avec navigation sans rechargement de page.

**Activation:**
```bash
flask vue init --router
```

Ou dans l'initialisation de l'extension:
```python
vue = Vue(app, plugins={'vue_router': True})
```

**Structure générée:**
- `src/router/index.js`: Configuration du routeur
- `src/views/`: Dossier contenant les composants de pages
  - `Home.vue`: Page d'accueil
  - `About.vue`: Page À propos
  - `NotFound.vue`: Page 404 pour les routes inexistantes
  - `ErrorPage.vue`: Page d'erreur générique

**Gestion des erreurs:**
- Gestion automatique des routes inexistantes (404)
- Gestion des erreurs pendant la navigation
- Redirection vers des pages d'erreur stylisées

### Pinia (Store)

Pinia est la bibliothèque de gestion d'état recommandée pour Vue 3, offrant une API intuitive et une intégration avec les outils de développement.

**Activation:**
```bash
flask vue init --pinia
```

Ou dans l'initialisation de l'extension:
```python
vue = Vue(app, plugins={'pinia': True})
```

**Structure générée:**
- `src/store/index.js`: Configuration des stores
  - Store utilisateur avec authentification
  - Store compteur pour exemple

## Architecture

Après l'initialisation, votre projet aura la structure suivante:

```
votre_app_flask/
├── app.py
├── frontend/
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   ├── public/
│   └── src/
│       ├── main.js
│       ├── App.vue
│       ├── style.css
│       ├── components/
│       │   └── HelloWorld.vue
│       ├── router/           # Si Vue Router est activé
│       │   └── index.js
│       ├── views/            # Si Vue Router est activé
│       │   ├── Home.vue
│       │   ├── About.vue
│       │   ├── NotFound.vue
│       │   └── ErrorPage.vue
│       └── store/            # Si Pinia est activé
│           └── index.js
└── static/
    └── build/
        └── (assets compilés en production)
```

## Exemples

### Configuration d'une application Flask avec Flask-Vue:

```python
# app.py
from flask import Flask, render_template
from flask_vue import Vue

app = Flask(__name__)
vue = Vue(
    app,
    dev_server_url="http://localhost:5173",
    plugins={
        'vue_router': True,
        'pinia': True
    }
)

@app.route('/')
@app.route('/<path:path>')
def index(path=None):
    """Toutes les routes sont gérées par Vue Router"""
    return render_template('index.html')

@app.route('/api/hello')
def hello_api():
    """API Flask pour être consommée par Vue"""
    return {
        'message': 'Bonjour depuis Flask!',
        'status': 'success'
    }

if __name__ == '__main__':
    app.run(debug=True)
```

### Template Flask avec vérification des plugins:

```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask-Vue App</title>
    {{ vue_hmr() }}
    {{ vue_css('main.css') }}
</head>
<body>
    <div id="app"></div>
    {{ vue_js('main.js') }}
    
    {% if vue_has_router() %}
    <!-- Configuration spécifique pour Vue Router si besoin -->
    <script>
        console.log('Vue Router est activé');
    </script>
    {% endif %}
</body>
</html>
```

## FAQ

**Q: Comment gérer les requêtes API entre Flask et Vue?**
R: Utilisez le module `fetch` pour appeler des endpoints Flask depuis Vue. Les endpoints Flask doivent retourner des réponses JSON.

**Q: Est-ce que les routes Flask sont nécessaires avec Vue Router?**
R: Vous avez besoin d'au moins une route Flask pour servir le template qui charge l'application Vue. Si vous utilisez Vue Router en mode history, vous devez également configurer Flask pour rediriger toutes les routes inconnues vers ce template.

**Q: Comment déployer une application Flask-Vue en production?**
R: Exécutez `flask vue build` pour compiler les assets Vue, puis déployez votre application Flask normalement. Assurez-vous que `dev_mode=False` dans la configuration de l'extension.

## Dépannage

### Le serveur de développement ne démarre pas

Vérifiez que Node.js et npm sont installés:
```bash
node -v
npm -v
```

### Les styles ne sont pas chargés en production

Vérifiez que le build a été correctement généré:
```bash
flask vue build
```
Et que les fichiers CSS existent dans `static/build/`.

### Les routes Vue Router ne fonctionnent pas

Assurez-vous que votre application Flask est configurée pour rediriger toutes les routes vers votre template principal:
```python
@app.route('/')
@app.route('/<path:path>')
def index(path=None):
    return render_template('index.html')
```

## Contribuer

Les contributions sont les bienvenues! Voici comment vous pouvez contribuer:

1. Fork le dépôt
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/amazing-feature`)
3. Committez vos changements (`git commit -m 'Add some amazing feature'`)
4. Pushez vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrez une Pull Request

## Licence

MIT