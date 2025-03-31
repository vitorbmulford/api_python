from flask import Flask
from .config import Config
from .utils.logging_config import configure_logging
from .utils.error_handlers import register_error_handlers

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    configure_logging(app)
    register_error_handlers(app)
    
    from .controllers.operadoras_controller import operadoras_bp
    from .controllers.healthcheck_controller import healthcheck_bp
    
    app.register_blueprint(operadoras_bp)
    app.register_blueprint(healthcheck_bp)
    
    return app