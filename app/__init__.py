from flask import Flask
from .config import Config

def create_app():
    try:
        app = Flask(__name__)
        app.config.from_object(Config)
        
        # Registrar blueprints
        from .controllers.operadoras_controller import operadoras_bp
        from .controllers.healthcheck_controller import healthcheck_bp
        
        app.register_blueprint(operadoras_bp)
        app.register_blueprint(healthcheck_bp)
        
        # Registrar manipuladores de erro
        from .utils.error_handlers import register_error_handlers
        register_error_handlers(app)
        
        return app
        
    except ImportError as e:
        print(f"Erro de importação: {str(e)}")
        raise