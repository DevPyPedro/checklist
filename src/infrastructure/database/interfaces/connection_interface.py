"""
Interface para o manipulador de conexão com o banco de dados.

Define o contrato que classes concretas devem seguir para implementar
o método de obtenção de uma conexão com o banco.
"""

from abc import ABC, abstractmethod
from typing import Optional
import psycopg2  # type: ignore

class IDBConnectionHandler(ABC):
    """Interface para criar uma conexão com o banco de dados PostgreSQL."""

    @abstractmethod
    def get_conn(self) -> Optional[psycopg2.extensions.connection]:
        """
        Obtém uma conexão ativa com o banco de dados.

        Returns:
            Optional[psycopg2.extensions.connection]: 
                Um objeto de conexão com o banco de dados, ou None se a conexão não puder ser estabelecida.
        """
        pass
