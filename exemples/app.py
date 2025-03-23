from flask import Flask, render_template
from flask.views import MethodView
from flask_vue import Vue


app = Flask(
    __name__,
    template_folder="assets/templates",
    static_folder="assets/static"
)

vue = Vue(app,
    # Mode de développement (si non spécifié, utilise app.config['VUE_MODE'] ou app.debug)
    dev_mode=True,  
    
    # URL du serveur de développement Vite (par défaut: http://localhost:5173)
    dev_server_url='   http://localhost:5173',   
    
    # Activer/désactiver les plugins Vue
    plugins={  
        'vue_router': True,
        'pinia': True
    }
)

class IndexView(MethodView):
    template_name = "index.html"

    def get(self, path=""):
        return render_template(self.template_name)
    


app.add_url_rule("/", view_func=IndexView.as_view("index"), defaults={"path": ""})
app.add_url_rule("/<path:path>/", view_func=IndexView.as_view("index_path"))

if __name__ == "__main__":
    app.run(debug=True)