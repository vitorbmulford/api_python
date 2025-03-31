from flask import Blueprint, jsonify, request
from ..services.operadora_service import OperadoraService
from ..utils.error_handlers import handle_api_error
from flask import Blueprint, jsonify, current_app
from ..models.database import DatabaseManager

operadoras_bp = Blueprint('operadoras', __name__, url_prefix='/api')

@operadoras_bp.route('/teste-banco/<registro_ans>', methods=['GET'])
def teste_banco(registro_ans):
    """Endpoint temporário para teste direto do banco"""
    try:
        registro_int = int(registro_ans)
        query = "SELECT * FROM operadoras WHERE registro_ans = %s LIMIT 1"
        result = DatabaseManager.execute_query(query, (registro_int,))
        
        if not result:
            return jsonify({
                "error": "Não encontrado",
                "query": query,
                "params": registro_int
            }), 404
            
        return jsonify(dict(result[0]))
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
@operadoras_bp.route('/operadora/<registro_ans>', methods=['GET'])
def detalhe_operadora(registro_ans):
    try:
        current_app.logger.info(f"Requisição para ANS: {registro_ans}")
        
        # Validação robusta
        if not registro_ans or not str(registro_ans).isdigit():
            current_app.logger.error(f"ANS inválido: {registro_ans}")
            return jsonify({"error": "Registro ANS deve ser numérico"}), 400
            
        registro_int = int(registro_ans)
        
        existe = DatabaseManager.execute_query(
            "SELECT EXISTS(SELECT 1 FROM operadoras WHERE registro_ans = %s)",
            (registro_int,)
        )
        
        if not existe or not existe[0][0]:
            current_app.logger.warning(f"ANS {registro_int} não existe no banco")
            return jsonify({"error": f"Operadora não encontrada"}), 404
        
        operadora = OperadoraService().buscar_por_ans(registro_int)
        
        if not operadora:
            current_app.logger.error(f"Dados não retornados para ANS: {registro_int}")
            return jsonify({
                "error": "Dados da operadora não puderam ser processados",
                "sugestao": "Verifique os logs do servidor"
            }), 500
            
        return jsonify(operadora)
        
    except Exception as e:
        current_app.logger.critical(f"Falha inesperada: {str(e)}", exc_info=True)
        return jsonify({"error": "Falha interna no servidor"}), 500