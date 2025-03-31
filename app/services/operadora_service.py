import logging
from ..models.database import DatabaseManager
from datetime import datetime

logger = logging.getLogger(__name__)

class OperadoraService:
    def buscar_por_ans(self, registro_ans):
        """Busca uma operadora específica pelo número ANS"""
        try:
            registro_int = int(registro_ans)
            
            query = """
            SELECT 
                registro_ans,
                razao_social,
                nome_fantasia,
                cnpj,
                modalidade,
                logradouro,
                numero,
                complemento,
                bairro,
                cidade,
                uf,
                cep,
                ddd,
                telefone,
                fax,
                endereco_eletronico as email,
                representante,
                cargo_representante,
                data_registro_ans
            FROM operadoras
            WHERE registro_ans = %s
            LIMIT 1
            """
            
            result = DatabaseManager.execute_query(query, (registro_int,))
            
            if not result:
                return None
                
            operadora = dict(result[0])
            
            # Tratamento de encoding e datas
            for key, value in operadora.items():
                if isinstance(value, str):
                    try:
                        operadora[key] = value.encode('latin1').decode('utf-8')
                    except:
                        pass
                elif isinstance(value, datetime):
                    operadora[key] = value.isoformat()
            
            return operadora
            
        except Exception as e:
            logger.error(f"Erro ao buscar operadora: {str(e)}", exc_info=True)
            return None

    def buscar_operadoras(self, termo, limit=10, offset=0):
        """Busca textual com paginação e ordenação por relevância"""
        try:
            termo_like = f"%{termo}%"
            
            query = """
            SELECT 
                registro_ans,
                razao_social,
                nome_fantasia,
                cnpj,
                cidade,
                uf,
                TS_RANK_CD(
                    TO_TSVECTOR('portuguese', 
                        COALESCE(razao_social, '') || ' ' || 
                        COALESCE(nome_fantasia, '') || ' ' || 
                        COALESCE(cidade, '') || ' ' || 
                        COALESCE(cnpj::text, '')),
                    PLAINTO_TSQUERY('portuguese', %s)
                ) AS relevancia
            FROM operadoras
            WHERE 
                razao_social ILIKE %s OR
                nome_fantasia ILIKE %s OR
                cnpj::text ILIKE %s OR
                cidade ILIKE %s OR
                uf ILIKE %s
            ORDER BY relevancia DESC, razao_social
            LIMIT %s OFFSET %s
            """
            
            params = (
                termo,  # Para TSQUERY
                termo_like, termo_like, termo_like, termo_like, termo_like,
                limit, offset
            )
            
            results = DatabaseManager.execute_query(query, params)
            
            operadoras = []
            for row in results:
                operadora = dict(row)
                # Tratamento de encoding
                for key, value in operadora.items():
                    if isinstance(value, str):
                        try:
                            operadora[key] = value.encode('latin1').decode('utf-8')
                        except:
                            pass
                operadoras.append(operadora)
                
            return operadoras
            
        except Exception as e:
            logger.error(f"Erro na busca textual: {str(e)}", exc_info=True)
            return []