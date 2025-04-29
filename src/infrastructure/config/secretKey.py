"""
Módulo para carregar parâmetros relacionados a chaves secretas e algoritmos
de autenticação a partir de variáveis de ambiente.

Este script utiliza a biblioteca `dotenv` para carregar as variáveis de ambiente 
armazenadas em um arquivo `.env`, e cria um dicionário com as informações necessárias
para autenticação (por exemplo, para geração/validação de tokens).
"""

import os
from dotenv import load_dotenv  # type: ignore

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Cria um dicionário com os parâmetros de chave secreta e algoritmo
secretKeyParamns = {
    "SecretKey": os.getenv("SECRETKEY"),         # Chave secreta usada na autenticação
    "algoritimo": str(os.getenv("ALGORITHMS")),  # Algoritmo de assinatura (forçado para string)
}
