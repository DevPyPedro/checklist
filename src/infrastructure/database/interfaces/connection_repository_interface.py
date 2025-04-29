"""
Interface para repositórios que executam consultas no banco de dados.

Define o contrato que classes concretas devem seguir para implementar
a execução de queries, podendo ou não retornar resultados.
"""

from abc import ABC, abstractmethod
from typing import Optional
import pandas as pd  # type: ignore

class IDatabaseRepository(ABC):
    """Interface para executar queries no banco de dados."""

    @classmethod
    @abstractmethod
    def run_query(cls, query: str, will_return: bool) -> Optional[pd.DataFrame]:
        """
        Executa uma consulta no banco de dados.

        Args:
            query (str): Comando SQL que será executado.
            will_return (bool): 
                Se True, a função deve retornar um DataFrame com o resultado da consulta;
                se False, não haverá retorno.

        Returns:
            Optional[pd.DataFrame]: 
                Um DataFrame contendo os resultados da consulta, ou None se `will_return` for False.
        """
        pass
