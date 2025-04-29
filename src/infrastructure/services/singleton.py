class SingletonMeta(type):
    """
    Metaclasse para implementar o padrão de design Singleton.

    Garante que uma classe tenha uma única instância, mesmo quando é chamada múltiplas vezes.
    Essa metaclasse intercepta a criação da classe e controla sua instância, criando-a apenas
    uma vez e retornando sempre a mesma instância em chamadas subsequentes.

    A classe que usa esta metaclasse deve ser instanciada uma única vez.
    """
    _instances = {}  # Dicionário que armazena as instâncias únicas das classes

    def __call__(cls, *args, **kwargs):
        """
        Intercepta a criação de novas instâncias e retorna a mesma instância existente
        se ela já foi criada.

        Args:
            *args: Argumentos a serem passados para o construtor da classe.
            **kwargs: Argumentos nomeados a serem passados para o construtor da classe.

        Returns:
            object: A instância única da classe.
        """
        # Verifica se a instância já foi criada
        if cls not in cls._instances:
            # Se não, cria e armazena a instância
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        # Retorna a instância existente
        return cls._instances[cls]
