from flask import Blueprint

# Import the individual blueprints
from .home_routes import home_bp
from .auth_routes import auth_bp
from .dashboard_routes import dashboard_bp
from .admin_routes import admin_bp

def register_blueprints(app):
    """
    Register all blueprints for the application.
    """
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(admin_bp)
