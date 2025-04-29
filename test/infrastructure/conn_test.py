import pytest


from src.infrastructure.database.settings.connection import PGconnectionHandler

def test_connection_success():
    handler = PGconnectionHandler()
    
    # Teste de conexão
    conn = handler.get_conn()

    # Verifica se a conexão foi estabelecida com sucesso
    assert conn is not None
    conn.close()  # Fecha a conexão após o teste
