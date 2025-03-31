from flask import Blueprint, jsonify
from datetime import datetime
import pytz

healthcheck_bp = Blueprint('healthcheck', __name__)

@healthcheck_bp.route('/api/healthcheck', methods=['GET'])
def healthcheck():
    """Endpoint para verificação do status da API"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now(pytz.timezone('America/Sao_Paulo')).isoformat(),
        "version": "1.0.0"
    })