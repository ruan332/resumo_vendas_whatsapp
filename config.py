"""
Configurações do sistema de resumo de vendas
"""
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# URLs das APIs
API_BASE_URL = os.getenv("API_BASE_URL", "http://lubnord.wmw.com.br:8087/lubnordws")
TOKEN_URL = f"{API_BASE_URL}/oauth/token"
VENDAS_URL = f"{API_BASE_URL}/integration/v1/fetch/pedido"
VENDEDORES_URL = f"{API_BASE_URL}/integration/v1/fetch/representante"
EMPRESAS_URL = f"{API_BASE_URL}/integration/v1/fetch/empresa"

# WhatsApp API
WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL", "https://api.chatweb.souchat.app/api/messages/send")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")

# Credenciais da API
API_AUTHORIZATION = os.getenv("API_AUTHORIZATION")
API_USERNAME = os.getenv("API_USERNAME")
API_PASSWORD = os.getenv("API_PASSWORD")

# Validação de variáveis obrigatórias
required_vars = ["WHATSAPP_TOKEN", "API_AUTHORIZATION", "API_USERNAME", "API_PASSWORD"]
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    raise ValueError(f"Variáveis de ambiente obrigatórias não encontradas: {', '.join(missing_vars)}")

# Mapeamento de empresas para UF
UF_MAPPING = {
    'LSO': 'CE',
    'LFO': 'CE', 
    'LTE': 'PI',
    'LTI': 'PI',
    'LSU': 'MA',
    'LCA': 'PB',
    'LPA': 'RN',
    'LIM': 'MA'
}

# Headers padrão
HEADERS_JSON = {
    'Content-Type': 'application/json'
}

HEADERS_FORM = {
    'Content-Type': 'application/x-www-form-urlencoded'
}