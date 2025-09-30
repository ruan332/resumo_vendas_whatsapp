"""
Script para investigar todos os campos disponíveis na API de vendas
"""

import logging
from api_client import APIClient
import json

def setup_logging():
    """Configura sistema de logs"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    """Função principal do teste"""
    
    # Configurar logs
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("=" * 60)
    logger.info("INVESTIGAÇÃO DOS CAMPOS DISPONÍVEIS NA API")
    logger.info("=" * 60)
    
    try:
        # Inicializar componentes
        api_client = APIClient()
        
        # Gerar token
        logger.info("Gerando token...")
        token = api_client.generate_token()
        if not token:
            logger.error("Falha ao gerar token")
            return False
        
        # Fazer uma consulta sem especificar campos para ver todos os campos disponíveis
        logger.info("Fazendo consulta sem filtro de campos...")
        
        # Modificar temporariamente o método para não filtrar campos
        import requests
        from datetime import datetime
        
        # URL da API
        from config import VENDAS_URL
        url = VENDAS_URL
        
        # Data de hoje
        hoje = datetime.now().strftime('%d/%m/%Y')
        
        # Payload sem especificar campos (para ver todos)
        payload = {
            "filters": [
                {
                    "property": "DTEMISSAO",
                    "operator": "=",
                    "value": hoje
                }
            ],
            "limit": 1  # Apenas 1 registro para análise
        }
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        logger.info(f"Consultando URL: {url}")
        logger.info(f"Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('data') and len(data['data']) > 0:
                primeiro_registro = data['data'][0]
                
                logger.info("CAMPOS DISPONÍVEIS NO PRIMEIRO REGISTRO:")
                logger.info("-" * 50)
                
                # Listar todos os campos
                campos_ordenados = sorted(primeiro_registro.keys())
                
                for campo in campos_ordenados:
                    valor = primeiro_registro[campo]
                    tipo_valor = type(valor).__name__
                    
                    # Destacar campos que podem ser relacionados a volume
                    destaque = ""
                    if any(palavra in campo.upper() for palavra in ['VOLUME', 'LITRO', 'QTD', 'QUANTIDADE', 'LITR']):
                        destaque = " ⭐ POSSÍVEL CAMPO DE VOLUME"
                    
                    logger.info(f"{campo}: {valor} ({tipo_valor}){destaque}")
                
                logger.info("-" * 50)
                logger.info(f"Total de campos encontrados: {len(campos_ordenados)}")
                
                # Procurar especificamente por campos relacionados a volume
                campos_volume = [campo for campo in campos_ordenados 
                               if any(palavra in campo.upper() for palavra in ['VOLUME', 'LITRO', 'QTD', 'QUANTIDADE', 'LITR'])]
                
                if campos_volume:
                    logger.info("\nCAMPOS RELACIONADOS A VOLUME/QUANTIDADE:")
                    for campo in campos_volume:
                        valor = primeiro_registro[campo]
                        logger.info(f"  {campo}: {valor}")
                else:
                    logger.info("\nNenhum campo relacionado a volume encontrado.")
                
            else:
                logger.warning("Nenhum registro encontrado na consulta")
                
        else:
            logger.error(f"Erro na consulta: {response.status_code}")
            logger.error(f"Resposta: {response.text}")
        
        logger.info("=" * 60)
        logger.info("INVESTIGAÇÃO CONCLUÍDA")
        logger.info("=" * 60)
        
        return True
        
    except Exception as e:
        logger.error(f"Erro durante a investigação: {str(e)}")
        return False

if __name__ == "__main__":
    main()