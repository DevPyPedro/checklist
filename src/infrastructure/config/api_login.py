"""
Módulo para carregar credenciais de login da API a partir de variáveis de ambiente.

Este script utiliza a biblioteca `dotenv` para carregar variáveis de ambiente 
armazenadas em um arquivo `.env`, e em seguida cria um dicionário contendo o 
usuário e a senha da API.
"""

import os
from dotenv import load_dotenv  # type: ignore

# Carrega as variáveis de ambiente do arquivo .env para o ambiente do sistema
load_dotenv()

# Cria um dicionário de login utilizando as variáveis de ambiente carregadas
login = {
    "User": os.getenv("API_USER"),  # Obtém o nome de usuário da variável de ambiente 'API_USER'
    "Pass": str(os.getenv("API_PASS")),  # Obtém a senha da variável 'API_PASS' e força para string
}
