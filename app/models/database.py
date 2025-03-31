import psycopg2
from psycopg2 import extras
from ..config import Config
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    @staticmethod
    def get_connection():
        try:
            # String de conexão com encoding forçado
            conn = psycopg2.connect(
                host=Config.DB_HOST,
                dbname=Config.DB_NAME,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                port=Config.DB_PORT,
                options=f"-c client_encoding=LATIN1"  # Força LATIN1 na conexão
            )
            conn.set_client_encoding('LATIN1')  # Configuração adicional
            return conn
        except Exception as e:
            logger.error(f"Erro de conexão com encoding LATIN1: {str(e)}")
            # Tentativa fallback com UTF-8
            try:
                conn = psycopg2.connect(
                    host=Config.DB_HOST,
                    dbname=Config.DB_NAME,
                    user=Config.DB_USER,
                    password=Config.DB_PASSWORD,
                    port=Config.DB_PORT,
                    options=f"-c client_encoding=UTF8"
                )
                conn.set_client_encoding('UTF8')
                return conn
            except Exception as fallback_error:
                logger.critical(f"Erro na conexão fallback UTF-8: {str(fallback_error)}")
                raise

    @staticmethod
    def execute_query(query, params=None, fetch=True):
        conn = None
        try:
            conn = DatabaseManager.get_connection()
            with conn.cursor(cursor_factory=extras.DictCursor) as cur:
                # Log da query que será executada
                logger.debug(f"Executando query: {query}")
                logger.debug(f"Com parâmetros: {params}")
                
                cur.execute(query, params or ())
                if fetch:
                    result = cur.fetchall()
                    conn.commit()
                    return result
                conn.commit()
        except Exception as e:
            logger.error(f"Erro detalhado: {str(e)}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()