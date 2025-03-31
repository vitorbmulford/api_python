#!/usr/bin/env python3
from app import create_app
import os

# Cria a aplicação Flask
app = create_app()

if __name__ == '__main__':
    # Obtém a porta do ambiente ou usa 5001 como padrão
    port = int(os.environ.get('PORT', 5001))
    
    # Executa a aplicação
    app.run(
        host='0.0.0.0',  # Permite acesso de qualquer rede
        port=port,
        debug=os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    )