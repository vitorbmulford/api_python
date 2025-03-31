import psycopg2
from psycopg2 import extras
from ..config import Config
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    @staticmethod
    def get_connection():
        """Estabelece conexão com o banco de dados"""
        try:
            conn = psycopg2.connect(
                host=Config.DB_HOST,
                dbname=Config.DB_NAME,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                port=Config.DB_PORT,
                options="-c client_encoding=UTF8"
            )
            conn.autocommit = False
            return conn
        except Exception as e:
            logger.error(f"Erro de conexão: {str(e)}")
            raise

    @staticmethod
    def execute_query(query, params=None, fetch=True, cursor_factory=extras.DictCursor):
        """Executa uma query no banco de dados"""
        conn = None
        try:
            conn = DatabaseManager.get_connection()
            with conn.cursor(cursor_factory=cursor_factory) as cur:
                logger.debug(f"Executando query: {query[:100]}...")  # Log parcial
                logger.debug(f"Com parâmetros: {params}")
                
                cur.execute(query, params or ())
                if fetch:
                    result = cur.fetchall()
                    conn.commit()
                    return result
                conn.commit()
        except Exception as e:
            logger.error(f"Erro na query: {str(e)}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()