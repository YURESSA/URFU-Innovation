from .auth import auth_bp
from .admin import admin_bp
from .test import test_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api')
    app.register_blueprint(test_bp, url_prefix='/api')
