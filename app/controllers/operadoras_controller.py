from flask import Blueprint, jsonify, request, current_app
from ..services.operadora_service import OperadoraService
from ..models.database import DatabaseManager
import logging

operadoras_bp = Blueprint('operadoras', __name__, url_prefix='/api')
logger = logging.getLogger(__name__)

@operadoras_bp.route('/operadora/<registro_ans>', methods=['GET'])
def detalhe_operadora(registro_ans):
    """Endpoint para detalhes de uma operadora específica"""
    try:
        # Validação do ANS
        if not registro_ans.isdigit() or len(registro_ans) > 10:
            logger.error(f"ANS inválido: {registro_ans}")
            return jsonify({"error": "Registro ANS inválido"}), 400

        registro_int = int(registro_ans)
        
        # Verificação de existência
        existe = DatabaseManager.execute_query(
            "SELECT EXISTS(SELECT 1 FROM operadoras WHERE registro_ans = %s)",
            (registro_int,)
        )[0][0]
        
        if not existe:
            logger.warning(f"ANS {registro_int} não encontrado")
            return jsonify({"error": "Operadora não encontrada"}), 404

        # Busca completa
        operadora = OperadoraService().buscar_por_ans(registro_int)
        
        if not operadora:
            logger.error(f"Falha ao recuperar dados para ANS: {registro_int}")
            return jsonify({"error": "Erro ao processar dados"}), 500
            
        return jsonify(operadora)
        
    except Exception as e:
        logger.critical(f"Erro fatal: {str(e)}", exc_info=True)
        return jsonify({"error": "Erro interno no servidor"}), 500

@operadoras_bp.route('/buscar', methods=['GET'])
def buscar_operadoras():
    """Endpoint de busca textual com paginação"""
    try:
        # Validação dos parâmetros
        termo = request.args.get('q', '').strip()
        if not termo or len(termo) < 2:
            return jsonify({
                "error": "Termo de busca deve ter pelo menos 2 caracteres",
                "exemplo": "/api/buscar?q=saude&limit=5&page=1"
            }), 400

        try:
            limit = int(request.args.get('limit', '10'))
            page = int(request.args.get('page', '1'))
            if limit <= 0 or page <= 0:
                raise ValueError
        except ValueError:
            return jsonify({
                "error": "Parâmetros limit e page devem ser números positivos",
                "exemplo": "/api/buscar?q=saude&limit=5&page=1"
            }), 400

        offset = (page - 1) * limit
        
        # Executar busca
        resultados = OperadoraService().buscar_operadoras(termo, limit, offset)
        
        return jsonify({
            'termo': termo,
            'pagina': page,
            'por_pagina': limit,
            'total_resultados': len(resultados),
            'resultados': resultados
        })
        
    except Exception as e:
        logger.error(f"Erro no endpoint de busca: {str(e)}", exc_info=True)
        return jsonify({"error": "Erro interno no servidor"}), 500

@operadoras_bp.route('/healthcheck', methods=['GET'])
def healthcheck():
    """Endpoint de verificação de saúde da API"""
    try:
        DatabaseManager.execute_query("SELECT 1")
        return jsonify({
            "status": "healthy",
            "versao": "1.0.0",
            "servicos": ["operadoras", "busca"]
        })
    except Exception as e:
        logger.error(f"Healthcheck falhou: {str(e)}")
        return jsonify({"status": "unhealthy"}), 500