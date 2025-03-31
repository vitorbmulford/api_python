from ..models.database import DatabaseManager

class Operadora:
    @staticmethod
    def buscar_por_ans(registro_ans):
        try:
            # Converter para inteiro independente da entrada
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
            
            results = DatabaseManager.execute_query(query, (registro_int,))
            
            if not results:
                return None
                
            # Converter para dicionário
            operadora = dict(results[0])
            
            # Tratar encoding dos campos textuais
            for key, value in operadora.items():
                if isinstance(value, str):
                    try:
                        operadora[key] = value.encode('latin1').decode('utf-8')
                    except:
                        pass
            
            return operadora
            
        except ValueError:
            return None
        except Exception as e:
            print(f"Erro na busca: {e}")
            return None