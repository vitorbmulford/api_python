from flask import Flask
from .config import Config
import logging
from logging.handlers import RotatingFileHandler

def create_app():
    """Factory de criação da aplicação Flask"""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configuração de logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler('app.log', maxBytes=10000, backupCount=3),
            logging.StreamHandler()
        ]
    )

    # Registrar blueprints
    from .controllers.operadoras_controller import operadoras_bp
    app.register_blueprint(operadoras_bp)

    return app