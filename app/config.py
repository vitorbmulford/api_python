import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Configurações do Banco de Dados
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'relatorio_data')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_PORT = os.getenv('DB_PORT', '5432')

    # Configurações da Aplicação
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    SECRET_KEY = os.getenv('SECRET_KEY', 'segredo-muito-seguro')