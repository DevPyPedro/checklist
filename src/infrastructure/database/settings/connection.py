from typing import Optional
import psycopg2  # type: ignore

from src.infrastructure.database.interfaces.connection_interface import IDBConnectionHandler
from src.infrastructure.config import configPG

class PGconnectionHandler(IDBConnectionHandler):
    """
    Classe para gerenciar a conexão com o banco de dados PostgreSQL.

    Implementa a interface `IDBConnectionHandler` e fornece métodos para criar e gerenciar
    uma conexão com o banco de dados PostgreSQL. Utiliza o contexto de gerenciamento de 
    recursos (with) para abrir e fechar conexões de forma segura.
    """

    def __init__(self) -> None:
        """
        Inicializa o manipulador de conexão com o banco de dados PostgreSQL.

        Define as configurações necessárias para estabelecer a conexão com o banco de dados.
        """
        self.__conn_pg = None
        self.__config_pg = {
            "database": configPG["database"],  # Nome do banco de dados
            "user": configPG["user"],          # Usuário para autenticação
            "host": configPG["host"],          # Host onde o banco de dados está localizado
            "password": configPG["password"],  # Senha para o usuário
            "port": configPG["port"],          # Porta do banco de dados
        }

    def __create_conn_pg(self) -> Optional[psycopg2.extensions.connection]:
        """
        Cria uma nova conexão com o banco de dados PostgreSQL.

        Tenta estabelecer uma conexão com o banco de dados usando as configurações fornecidas. 

        Returns:
            Optional[psycopg2.extensions.connection]: Retorna um objeto de conexão se a 
                                                     conexão for bem-sucedida, ou None se falhar.
        """
        try:
            self.__conn_pg = psycopg2.connect(**self.__config_pg)
            return self.__conn_pg
        except Exception as e:
            print(f"Error connecting to PostgreSQL: {e}")
            return None

    def get_conn(self) -> Optional[psycopg2.extensions.connection]:
        """
        Obtém a conexão ativa com o banco de dados PostgreSQL.

        Se a conexão já estiver estabelecida, ela é retornada; caso contrário, 
        uma nova conexão é criada.

        Returns:
            Optional[psycopg2.extensions.connection]: Retorna a conexão ativa ou None.
        """
        if self.__conn_pg is None:
            return self.__create_conn_pg()
        return self.__conn_pg
    
    def __enter__(self) -> Optional[psycopg2.extensions.connection]:
        """
        Permite o uso da classe como um gerenciador de contexto (usando 'with').

        Retorna a conexão ativa com o banco de dados.

        Returns:
            Optional[psycopg2.extensions.connection]: A conexão ativa ou None.
        """
        return self.get_conn()

    def __exit__(self, exc_type, exc_value, exc_tb):
        """
        Fechamento seguro da conexão com o banco de dados quando o bloco 'with' é finalizado.

        Fecha a conexão com o banco de dados se estiver ativa e limpa o objeto de conexão.

        Args:
            exc_type: Tipo da exceção, se houver.
            exc_value: Valor da exceção, se houver.
            exc_tb: Rastreamento de pilha da exceção, se houver.
        """
        if self.__conn_pg:
            self.__conn_pg.close()  # Fecha a conexão
            self.__conn_pg = None  # Limpa a referência da conexão
