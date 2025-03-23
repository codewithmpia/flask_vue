"""
Flask-Vue
----------
Une extension Flask pour intégrer Vite.js, Vue 3 et 
Tailwind CSS 4 dans une application Flask.
"""
import os
import copy
from flask import current_app, url_for
from markupsafe import Markup

from .config import DEFAULT_SETTINGS
from . import cli
from . import plugins  # Import du module plugins


class Vue:
    def __init__(self, app=None, **kwargs):
        self.app = app
        
        # Copier les paramètres par défaut pour éviter de les modifier globalement
        self.settings = copy.deepcopy(DEFAULT_SETTINGS)
        
        # Mettre à jour avec les kwargs fournis
        for key, value in kwargs.items():
            if key in self.settings:
                self.settings[key] = value
            elif key == 'plugins' and isinstance(value, dict):
                # Fusion des configurations de plugins
                for plugin_key, plugin_value in value.items():
                    if plugin_key in self.settings['plugins']:
                        self.settings['plugins'][plugin_key] = plugin_value
        
        # Configuration spécifique
        self.static_url_path = self.settings['static_url_path']
        self.assets_path = self.settings['assets_path']
        self.manifest_path = self.settings['manifest_path']
        self.dev_server_url = self.settings['dev_server_url']
        self.entry_map = self.settings['entry_map']
        self.plugins = self.settings['plugins']
        self.dev_mode = kwargs.get('dev_mode')
        
        self._manifest = None
        self._tried_loading_manifest = False

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialise l'extension avec l'application Flask"""
        app.extensions['vue'] = self
        
        # Mettre à jour static_url_path avec le chemin réel
        self.static_url_path = app.static_url_path
        self.static_folder = app.static_folder

        # Déterminer le mode développement
        if self.dev_mode is None:
            # Vérifier si FLASK_VUE_MODE est défini dans l'environnement ou la config
            env_mode = os.environ.get('FLASK_VUE_MODE')
            config_mode = app.config.get('VUE_MODE')
            
            if env_mode == 'development' or config_mode == 'development':
                self.dev_mode = True
                app.logger.info('Flask-Vue: Mode développement activé via configuration')
            elif env_mode == 'production' or config_mode == 'production':
                self.dev_mode = False
                app.logger.info('Flask-Vue: Mode production activé via configuration')
            else:
                # Par défaut, utiliser le mode DEBUG de Flask
                self.dev_mode = app.debug
                app.logger.info(f'Flask-Vue: Mode {"développement" if self.dev_mode else "production"} basé sur app.debug')
        else:
            app.logger.info(f'Flask-Vue: Mode {"développement" if self.dev_mode else "production"} forcé via paramètre')

        # Enregistrer les fonctions d'aide dans Jinja
        app.jinja_env.globals.update(
            vue_asset=self.asset_url,
            vue_hmr=self.hmr_script,
            vue_css=self.css_tags,
            vue_js=self.js_tag,
            vue_has_router=self.has_vue_router,
            vue_has_pinia=self.has_pinia
        )
        
        # Initialiser les commandes CLI
        cli.init_cli(app)

    def has_vue_router(self):
        """Vérifie si Vue Router est activé"""
        return self.plugins.get('vue_router', False)

    def has_pinia(self):
        """Vérifie si Pinia est activé"""
        return self.plugins.get('pinia', False)

    def hmr_script(self):
        """Génère la balise script pour le Hot Module Replacement (HMR) en mode dev"""
        if not self.dev_mode:
            return Markup('')
        
        # Assurez-vous que l'URL n'a pas de double slashes
        base_url = self.dev_server_url.rstrip('/')
        hmr_url = f"{base_url}/@vite/client"
        current_app.logger.debug(f"Générer HMR script tag -> {hmr_url}")
        return Markup(f'<script type="module" src="{hmr_url}"></script>')

    def js_tag(self, entry_point):
        """Génère la balise script pour un point d'entrée JavaScript"""
        if self.dev_mode:
            # Mode développement: pointer vers le serveur Vite
            base_url = self.dev_server_url.rstrip('/')
            
            # Utiliser le mappage pour obtenir le chemin réel en développement
            dev_entry_path = self.entry_map.get(entry_point, entry_point)
            dev_entry_path = dev_entry_path.lstrip('/')
                
            vite_url = f"{base_url}/{dev_entry_path}"
            current_app.logger.debug(f"MODE DEV: Générer script tag pour {entry_point} -> {vite_url}")
            return Markup(f'<script type="module" src="{vite_url}"></script>')
        
        # Mode production: utiliser un chemin simple sans hash
        # Pour les entrées comme 'src/main.js', extraire juste 'main.js'
        simple_name = os.path.basename(entry_point)
        
        # Construire le chemin vers le fichier dans assets/
        asset_url = url_for('static', filename=f"{self.assets_path}{simple_name}")
        current_app.logger.debug(f"MODE PROD: Générer script tag pour {entry_point} -> {asset_url}")
        return Markup(f'<script type="module" src="{asset_url}"></script>')

    def css_tags(self, entry_point):
        """Génère les balises CSS pour un point d'entrée"""
        if self.dev_mode:
            # En mode développement, si le point d'entrée est un fichier CSS explicite, 
            # générer une balise link vers le serveur de développement
            if entry_point.endswith('.css'):
                base_url = self.dev_server_url.rstrip('/')
                dev_css_path = self.entry_map.get(entry_point, entry_point)
                dev_css_path = dev_css_path.lstrip('/')
                css_url = f"{base_url}/{dev_css_path}"
                current_app.logger.debug(f"MODE DEV: Générer CSS link pour {entry_point} -> {css_url}")
                return Markup(f'<link rel="stylesheet" href="{css_url}">')
            
            # Si c'est un fichier JS, ne rien faire car Vite injecte le CSS via JavaScript
            return Markup('')
        
        # En mode production
        if entry_point.endswith('.css'):
            # Si on passe directement un fichier CSS
            css_name = os.path.basename(entry_point)
        else:
            # Si c'est un fichier JS, extraire la base du nom
            base_name = os.path.splitext(os.path.basename(entry_point))[0]  # 'main.js' -> 'main'
            css_name = f"{base_name}.css"
        
        # Vérifier si le fichier CSS existe
        css_path = os.path.join(current_app.static_folder, self.assets_path, css_name)
        if os.path.exists(css_path):
            css_url = url_for('static', filename=f"{self.assets_path}{css_name}")
            current_app.logger.debug(f"MODE PROD: Générer CSS link pour {entry_point} -> {css_url}")
            return Markup(f'<link rel="stylesheet" href="{css_url}">')
        else:
            # Essayer dans le sous-dossier 'assets' s'il existe
            assets_css_path = os.path.join(current_app.static_folder, self.assets_path, 'assets', css_name)
            if os.path.exists(assets_css_path):
                css_url = url_for('static', filename=f"{self.assets_path}assets/{css_name}")
                current_app.logger.debug(f"MODE PROD: Générer CSS link pour {entry_point} -> {css_url}")
                return Markup(f'<link rel="stylesheet" href="{css_url}">')
        
        current_app.logger.warning(f"Fichier CSS introuvable pour {entry_point}: {css_path}")
        return Markup('')

    def asset_url(self, filename):
        """Génère l'URL pour un asset"""
        if self.dev_mode:
            base_url = self.dev_server_url.rstrip('/')
            
            # Utiliser le mappage pour les assets aussi
            dev_file_path = self.entry_map.get(filename, filename)
            dev_file_path = dev_file_path.lstrip('/')
            
            return f"{base_url}/{dev_file_path}"

        # En production, utiliser le chemin simple dans assets/
        simple_name = os.path.basename(filename)
        return url_for('static', filename=f"{self.assets_path}{simple_name}")

    def get_static_folder(self):
        """Retourne le chemin absolu vers le dossier static"""
        return self.static_folder or current_app.static_folder