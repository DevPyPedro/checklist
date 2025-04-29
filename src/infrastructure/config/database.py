"""
Módulo para carregar configurações de conexão com o banco de dados PostgreSQL
a partir de variáveis de ambiente.

Utiliza a biblioteca `dotenv` para carregar as variáveis de ambiente 
armazenadas em um arquivo `.env`, e cria um dicionário com os parâmetros
necessários para a conexão.
"""

import os
from dotenv import load_dotenv  # type: ignore

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Cria um dicionário com as configurações de conexão ao PostgreSQL
configPG = {
    "database": os.getenv("PGDATABASE"),  # Nome do banco de dados
    "user": os.getenv("PGUSER"),           # Nome do usuário
    "host": os.getenv("PGHOST"),           # Endereço do host do banco
    "password": os.getenv("PGPASSWORD"),   # Senha do usuário
    "port": int(os.getenv("PGPORT")),      # Porta de conexão (convertida para inteiro)
}
