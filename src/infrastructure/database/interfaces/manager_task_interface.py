"""
Interface para gerenciamento de tarefas.

Define o contrato que classes concretas devem seguir para adicionar tarefas
a uma fila que será processada por trabalhadores (workers).
"""

from abc import ABC, abstractmethod

class IManagerTask(ABC):
    """Interface para gerenciamento de tarefas que serão processadas por trabalhadores."""

    @abstractmethod
    def add_task(self, query: str, return_: bool) -> any:
        """
        Adiciona uma tarefa à fila para ser processada pelos trabalhadores.

        Args:
            query (str): A consulta ou comando a ser executado pelos trabalhadores.
            return_ (bool): Indica se a tarefa deve retornar algum valor ou não.

        Returns:
            any: O valor de retorno da tarefa, dependendo da implementação concreta.
        """
        pass
