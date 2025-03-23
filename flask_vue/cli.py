"""
Module CLI pour l'extension Flask-Vue.
Ajoute des commandes pour initialiser, installer, 
démarrer et construire une application Vite avec Vue 3.
"""
import os
import sys
import subprocess
import click
from flask import current_app
from flask.cli import with_appcontext


from .config import (
    VITE_CONFIG_TEMPLATE, 
    PACKAGE_JSON_TEMPLATE, 
    HTML_TEMPLATE, 
    JS_TEMPLATE, 
    CSS_TEMPLATE,
    APP_VUE_TEMPLATE
)
from .plugins import (
    configure_vue_router,
    configure_pinia,
    add_vue_router_files,
    add_pinia_files,
    get_main_js_template,
    get_app_vue_template
)

def create_vue_group(app):
    """Crée un groupe de commandes Flask pour Vue"""
    @app.cli.group('vue')
    def vue_group():
        """Commandes pour gérer l'intégration Vue."""
        pass

    @vue_group.command('init')
    @click.option('--path', '-p', default='frontend', 
                help='Chemin où initialiser le projet Vue')
    @click.option('--router/--no-router', default=False, 
                help='Ajouter Vue Router')
    @click.option('--pinia/--no-pinia', default=False, 
                help='Ajouter Pinia (state management)')
    @with_appcontext
    def init_command(path, router, pinia):
        """Initialise un nouveau projet Vue 3 avec Vite et Tailwind CSS 4."""
        try:
            init_vue_project(path, router=router, pinia=pinia)
        except Exception as e:
            click.echo(f"Erreur lors de l'initialisation: {str(e)}", err=True)
            sys.exit(1)

    @vue_group.command('install')
    @click.option('--path', '-p', default='frontend', 
                help='Chemin du projet Vue')
    @with_appcontext
    def install_command(path):
        """Installe les dépendances NPM."""
        try:
            install_dependencies(path)
        except Exception as e:
            click.echo(f"Erreur lors de l'installation: {str(e)}", err=True)
            sys.exit(1)

    @vue_group.command('start')
    @click.option('--path', '-p', default='frontend', 
                help='Chemin du projet Vue')
    @with_appcontext
    def start_command(path):
        """Démarre le serveur de développement Vite."""
        try:
            start_dev_server(path)
        except Exception as e:
            click.echo(f"Erreur lors du démarrage: {str(e)}", err=True)
            sys.exit(1)

    @vue_group.command('build')
    @click.option('--path', '-p', default='frontend', 
                help='Chemin du projet Vue')
    @with_appcontext
    def build_command(path):
        """Construit les assets Vue pour la production."""
        try:
            build_vue_assets(path)
        except Exception as e:
            click.echo(f"Erreur lors de la construction: {str(e)}", err=True)
            sys.exit(1)

def init_vue_project(path, router=False, pinia=False):
    """Initialise un nouveau projet Vue avec Vite et Tailwind CSS 4."""
    # Vérifier si le dossier existe déjà
    if os.path.exists(path):
        if os.path.isdir(path) and os.listdir(path):
            click.echo(f"Le dossier '{path}' existe déjà et n'est pas vide.")
            if not click.confirm("Voulez-vous continuer?"):
                click.echo("Initialisation annulée.")
                return
    else:
        os.makedirs(path)
    
    click.echo(f"Initialisation d'un nouveau projet Vue 3 avec Vite et Tailwind CSS 4 dans '{path}'...")
    
    # Créer la structure du projet
    os.makedirs(os.path.join(path, 'src'), exist_ok=True)
    os.makedirs(os.path.join(path, 'src', 'components'), exist_ok=True)
    os.makedirs(os.path.join(path, 'public'), exist_ok=True)
    
    # Déterminer le chemin relatif du dossier static pour outDir
    static_folder = current_app.static_folder
    frontend_path = os.path.abspath(path)
    build_path = os.path.join(static_folder, 'build')
    
    # Calculer le chemin relatif entre le dossier frontend et le dossier build
    rel_path = os.path.relpath(build_path, frontend_path)
    # Normaliser le chemin pour les slashes selon l'OS
    rel_path = rel_path.replace('\\', '/')
    
    click.echo(f"Chemin relatif vers static/build: {rel_path}")
    
    # Modifier le template vite.config.js pour utiliser le chemin relatif correct
    vite_config = VITE_CONFIG_TEMPLATE.replace("'../static/build'", f"'{rel_path}'")
    
    # Écrire les fichiers de base
    with open(os.path.join(path, 'vite.config.js'), 'w') as f:
        f.write(vite_config.strip())
    
    # Préparer package.json en fonction des plugins
    package_json = PACKAGE_JSON_TEMPLATE
    
    # Gérer les plugins
    if router or pinia:
        # Ajouter les dépendances au package.json
        if router:
            package_json = configure_vue_router(path, package_json)
        if pinia:
            package_json = configure_pinia(path, package_json)
    
    with open(os.path.join(path, 'package.json'), 'w') as f:
        f.write(package_json.strip())
    
    with open(os.path.join(path, 'index.html'), 'w') as f:
        f.write(HTML_TEMPLATE.strip())
    
    # Sélectionner le template main.js approprié
    main_js_content = get_main_js_template(router, pinia)
    if main_js_content is None:  # Utiliser le template par défaut
        main_js_content = JS_TEMPLATE
    
    with open(os.path.join(path, 'src', 'main.js'), 'w') as f:
        f.write(main_js_content.strip())
    
    # Sélectionner le template App.vue approprié
    app_vue_content = get_app_vue_template(router)
    if app_vue_content is None:  # Utiliser le template par défaut
        app_vue_content = APP_VUE_TEMPLATE
    
    with open(os.path.join(path, 'src', 'App.vue'), 'w') as f:
        f.write(app_vue_content.strip())
        
    # Ajouter les fichiers pour Vue Router si nécessaire
    if router:
        add_vue_router_files(path)
        
    # Ajouter les fichiers pour Pinia si nécessaire
    if pinia:
        add_pinia_files(path)
    
    with open(os.path.join(path, 'src', 'style.css'), 'w') as f:
        f.write(CSS_TEMPLATE.strip())
    
    # Créer un exemple de composant
    with open(os.path.join(path, 'src', 'components', 'HelloWorld.vue'), 'w') as f:
        f.write("""<template>
  <div class="p-4 bg-gray-100 rounded-lg shadow">
    <h2 class="text-2xl font-bold text-gray-800 mb-2">{{ title }}</h2>
    <p class="text-gray-600">{{ message }}</p>
    <div class="mt-4">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      default: 'Hello World'
    },
    message: {
      type: String,
      default: 'Bienvenue dans ce composant Vue 3 avec Tailwind CSS'
    }
  }
}
</script>
""")
    
    # Mettre à jour la configuration de l'extension
    vue_instance = current_app.extensions.get('vue')
    if vue_instance:
        vue_instance.plugins['vue_router'] = router
        vue_instance.plugins['pinia'] = pinia
        current_app.logger.info(f"Configuration de l'extension Flask-Vue mise à jour: Vue Router={router}, Pinia={pinia}")
    
    # Afficher le résumé
    click.echo(f"Projet Vue initialisé avec succès dans '{path}'!")
    click.echo(f"Structure créée:")
    click.echo(f"  {path}/")
    click.echo(f"  ├── vite.config.js (avec outDir='{rel_path}')")
    click.echo(f"  ├── package.json")
    click.echo(f"  ├── index.html")
    click.echo(f"  ├── public/")
    click.echo(f"  └── src/")
    click.echo(f"      ├── main.js")
    click.echo(f"      ├── App.vue")
    click.echo(f"      ├── style.css")
    click.echo(f"      ├── components/")
    click.echo(f"      │   └── HelloWorld.vue")
    
    if router:
        click.echo(f"      ├── router/")
        click.echo(f"      │   └── index.js")
        click.echo(f"      ├── views/")
        click.echo(f"      │   ├── Home.vue")
        click.echo(f"      │   └── About.vue")
    
    if pinia:
        click.echo(f"      ├── store/")
        click.echo(f"      │   └── index.js")
    
    click.echo("")
    click.echo("Vous pouvez maintenant exécuter:")
    click.echo(f"  flask vue install --path {path}")
    click.echo(f"  flask vue start --path {path}")

def install_dependencies(path):
    """Installe les dépendances NPM."""
    if not os.path.exists(os.path.join(path, 'package.json')):
        raise Exception(f"Aucun fichier package.json trouvé dans '{path}'. "
                       f"Exécutez d'abord 'flask vue init --path {path}'.")
    
    click.echo(f"Installation des dépendances NPM dans '{path}'...")
    
    # Exécuter npm install
    try:
        subprocess.run(['npm', 'install'], cwd=path, check=True)
        click.echo("Dépendances installées avec succès!")
    except subprocess.CalledProcessError as e:
        raise Exception(f"Erreur lors de l'exécution de npm install: {str(e)}")
    except FileNotFoundError:
        raise Exception("La commande 'npm' n'a pas été trouvée. Assurez-vous que Node.js est installé.")

def start_dev_server(path):
    """Démarre le serveur de développement Vite."""
    if not os.path.exists(os.path.join(path, 'package.json')):
        raise Exception(f"Aucun fichier package.json trouvé dans '{path}'. "
                       f"Exécutez d'abord 'flask vue init --path {path}'.")
    
    click.echo(f"Démarrage du serveur de développement Vite dans '{path}'...")
    click.echo("Utilisez Ctrl+C pour arrêter le serveur.")
    
    # Vérifier si node_modules existe
    if not os.path.exists(os.path.join(path, 'node_modules')):
        click.echo("Le dossier node_modules n'existe pas. Installation des dépendances...")
        install_dependencies(path)
    
    # Exécuter npm run dev
    try:
        subprocess.run(['npm', 'run', 'dev'], cwd=path)
    except KeyboardInterrupt:
        click.echo("\nServeur arrêté.")
    except subprocess.CalledProcessError as e:
        raise Exception(f"Erreur lors du démarrage du serveur: {str(e)}")
    except FileNotFoundError:
        raise Exception("La commande 'npm' n'a pas été trouvée. Assurez-vous que Node.js est installé.")

def build_vue_assets(path):
    """Construit les assets Vue pour la production."""
    if not os.path.exists(os.path.join(path, 'package.json')):
        raise Exception(f"Aucun fichier package.json trouvé dans '{path}'. "
                       f"Exécutez d'abord 'flask vue init --path {path}'.")
    
    click.echo(f"Construction des assets Vue pour la production dans '{path}'...")
    
    # Vérifier si node_modules existe
    if not os.path.exists(os.path.join(path, 'node_modules')):
        click.echo("Le dossier node_modules n'existe pas. Installation des dépendances...")
        install_dependencies(path)
    
    # Exécuter npm run build
    try:
        subprocess.run(['npm', 'run', 'build'], cwd=path, check=True)
        
        # Vérifier que le build a réussi
        static_dir = current_app.static_folder
        build_dir = os.path.join(static_dir, 'build')
        
        if os.path.exists(build_dir):
            click.echo(f"Assets construits avec succès dans '{build_dir}'!")
        else:
            click.echo(f"Le dossier de build '{build_dir}' n'a pas été trouvé. "
                      f"Vérifiez la configuration dans vite.config.js.")
            
    except subprocess.CalledProcessError as e:
        raise Exception(f"Erreur lors de la construction des assets: {str(e)}")
    except FileNotFoundError:
        raise Exception("La commande 'npm' n'a pas été trouvée. Assurez-vous que Node.js est installé.")

# Cette fonction doit être appelée dans l'extension Flask-Vue pour enregistrer les commandes
def init_cli(app):
    """Initialise les commandes CLI pour Flask-Vue."""
    create_vue_group(app)