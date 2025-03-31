from ..models.database import DatabaseManager
import logging

logger = logging.getLogger(__name__)

class OperadoraService:
    def buscar_por_ans(self, registro_ans):
        try:
            registro_int = int(registro_ans)
            
            # Query corrigida - verifique os espaços e quebras de linha
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
            
            # Debug: imprima a query para verificação
            print("Query a ser executada:")
            print(query.replace('\n', ' ').replace('  ', ' '))
            
            result = DatabaseManager.execute_query(query, (registro_int,))
            
            if not result:
                return None
                
            return dict(result[0])
            
        except Exception as e:
            logger.error(f"Erro na busca: {str(e)}")
            return None