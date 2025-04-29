import threading
import queue
import os

from src.infrastructure.database.interfaces.connection_repository_interface import IDatabaseRepository
from src.infrastructure.database.interfaces.manager_task_interface import IManagerTask

class Task:
    """
    Representa uma tarefa a ser executada por um trabalhador (worker).

    Contém informações sobre a consulta (query) a ser executada, se a tarefa deve retornar
    dados ou não, o resultado da execução e um evento para sincronização.
    """
    def __init__(self, query, return_):
        """
        Inicializa uma nova instância de Task.

        Args:
            query (str): A consulta SQL que será executada.
            return_ (bool): Indica se a consulta deve retornar dados ou não.
        """
        self.query = query
        self.return_ = return_
        self.result = None
        self.event = threading.Event()

    def set_result(self, result):
        """
        Define o resultado da execução da tarefa e sinaliza o evento de conclusão.

        Args:
            result: O resultado da execução da tarefa (geralmente um DataFrame ou None).
        """
        self.result = result
        self.event.set()  # Sinaliza que a tarefa foi concluída


class ManagerTask(IManagerTask):
    """
    Gerenciador de tarefas que controla a execução das tarefas por múltiplos trabalhadores (workers).

    A classe utiliza threads para distribuir as tarefas em um pool de trabalhadores, 
    onde cada thread executa uma tarefa da fila de tarefas.
    """
    def __init__(self, database: IDatabaseRepository):
        """
        Inicializa o gerenciador de tarefas e inicia os trabalhadores.

        Args:
            database (IDatabaseRepository): A instância do repositório de banco de dados
                                             para executar as consultas.
        """
        self.Jobs_at_Queue = queue.Queue()  # Fila de tarefas a serem executadas
        self.InfoWorkers = {}  # Informações sobre os trabalhadores
        self.database = database  # Repositório de banco de dados
        self.StartWorker()  # Inicia os trabalhadores

    def add_task(self, query: str, return_: bool):
        """
        Adiciona uma nova tarefa à fila de execução.

        Args:
            query (str): A consulta SQL a ser executada.
            return_ (bool): Indica se a consulta deve retornar dados ou não.

        Returns:
            Task: A tarefa que foi adicionada à fila.
        """
        task = Task(query, return_)  # Cria uma nova tarefa
        self.Jobs_at_Queue.put(task)  # Adiciona a tarefa à fila
        return task  # Retorna a tarefa

    def StartWorker(self):
        """
        Inicia os trabalhadores (threads) para processar as tarefas da fila.

        Cria uma thread para cada trabalhador, baseado no número de núcleos de CPU disponíveis.
        """
        for id in range(os.cpu_count() - 2):  # Utiliza todos os núcleos, exceto 2
            self.InfoWorkers[id] = {}
            self.InfoWorkers[id]["Thread"] = threading.Thread(
                target=self.Worker,
                args=(
                    id,
                    self.Jobs_at_Queue,
                ),
                daemon=True,
            )
            self.InfoWorkers[id]["Thread"].start()  # Inicia o trabalhador

            # Verifica se o trabalhador está pronto para começar
            while True:
                if "OK" in self.InfoWorkers[id]:
                    if self.InfoWorkers[id]["OK"]:
                        break

    def Worker(self, id, Jobs_at_Queue):
        """
        Função executada por cada trabalhador para processar as tarefas.

        Cada trabalhador pega uma tarefa da fila e executa a consulta associada.

        Args:
            id (int): O identificador único do trabalhador.
            Jobs_at_Queue (queue.Queue): A fila de tarefas a serem executadas.
        """
        self.InfoWorkers[id]["OK"] = True  # Marca o trabalhador como pronto
        while True:
            task = Jobs_at_Queue.get()  # Pega a próxima tarefa na fila
            if task.return_ == True:
                # Executa a consulta e retorna o resultado como um DataFrame
                dataframe = self.database.run_query(task.query, task.return_)
                task.set_result(dataframe)  # Define o resultado da tarefa
            else:
                # Executa a consulta sem retornar dados
                self.database.run_query(task.query, task.return_)
                task.set_result(None)  # Define o resultado como None
