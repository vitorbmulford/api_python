from flask import jsonify
import logging

logger = logging.getLogger(__name__)

def handle_api_error(error):
    """Tratamento padronizado de erros da API"""
    logger.error(f"Erro: {str(error)}", exc_info=True)
    return jsonify({"error": str(error)}), 500

def register_error_handlers(app):
    """Registra os manipuladores de erro na aplicação Flask"""
    app.register_error_handler(500, handle_api_error)
    app.register_error_handler(404, lambda e: (jsonify({"error": "Recurso não encontrado"}), 404))
    app.register_error_handler(400, lambda e: (jsonify({"error": "Requisição inválida"}), 400))