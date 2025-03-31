import logging
from logging.handlers import RotatingFileHandler
import os

def configure_logging(app):
    """Configuração centralizada de logging"""
    
    # Criar diretório de logs se não existir
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configuração básica
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # File Handler (rotativo)
    file_handler = RotatingFileHandler(
        'logs/api.log',
        maxBytes=1024 * 1024 * 10,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    file_handler.setLevel(logging.INFO)
    
    # Adicionar handlers
    logger = logging.getLogger()
    logger.addHandler(file_handler)
    
    # Configurar nível de log do SQLAlchemy (se aplicável)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    
    app.logger = logger