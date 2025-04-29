import pandas as pd  # type: ignore
import logging

from src.infrastructure.database.interfaces.connection_repository_interface import IDatabaseRepository
from src.infrastructure.database.settings.connection import PGconnectionHandler

class DatabaseRepository(IDatabaseRepository):
    """
    Implementação do repositório de banco de dados para executar queries SQL.

    Esta classe implementa a interface `IDatabaseRepository` e fornece 
    métodos para executar consultas SQL, com ou sem retorno de dados.
    """

    @classmethod
    def run_query(cls, query: str, will_return: bool = False):
        """
        Executa uma consulta no banco de dados.

        Dependendo do valor de `will_return`, o método executa uma consulta 
        SQL e retorna os dados em forma de DataFrame ou apenas executa a consulta 
        sem retornar dados.

        Args:
            query (str): A consulta SQL que será executada.
            will_return (bool, opcional): Se True, a consulta retornará um DataFrame 
                                          com os resultados. Se False, a consulta 
                                          será executada sem retorno de dados. O padrão é False.

        Returns:
            Optional[pd.DataFrame]: Retorna um DataFrame com os resultados da consulta, 
                                    ou True se a execução foi bem-sucedida e `will_return` for False.

        Raises:
            Exception: Se ocorrer algum erro ao executar a consulta, uma exceção será levantada.
        """
        try:
            # Cria um handler para a conexão com o banco de dados
            db_handler = PGconnectionHandler()
            
            # Estabelece a conexão com o banco e executa a consulta
            with db_handler as conn:
                # Se for necessário retornar dados, executa a consulta e retorna um DataFrame
                if will_return:
                    for q in query:
                        df = pd.read_sql(q, conn)  # Executa a consulta e carrega o resultado no DataFrame
                        conn.commit()  # Confirma a transação
                    return df
                
                # Se não for necessário retornar dados, apenas executa a consulta
                else:
                    cursor = conn.cursor()
                    for q in query:
                        cursor.execute(q)  # Executa a consulta
                        conn.commit()  # Confirma a transação
                    return True  # Indica que a execução foi bem-sucedida
                
        except Exception as e:
            # Exibe uma mensagem de erro no console
            print(f'Erro ao executar a query: {query}: {e}')
            # Registra o erro no log
            logging.error(f"\nErro ao executar a query: {query}: {e}\n")
