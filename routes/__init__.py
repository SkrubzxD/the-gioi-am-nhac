from .library import library_bp
from .quiz import quiz_bp
from .thesis import thesis_bp
from .main import main_bp
from utils.nav import get_nav_items

def register_routes(app):
    app.register_blueprint(library_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(thesis_bp)
    app.register_blueprint(main_bp)

    @app.context_processor
    def inject_nav():
        try:
            nav_items = get_nav_items()
        except Exception:
            nav_items = []
        return {'nav_items': nav_items}
    
    @app.after_request
    def add_header(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
