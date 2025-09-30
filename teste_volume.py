"""
Script de teste para verificar se o campo vlvolumepedido está retornando valores corretos
"""

import logging
from api_client import APIClient
from data_processor import DataProcessor

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
    
    logger.info("=" * 50)
    logger.info("TESTE DO CAMPO VLVOLUMEPEDIDO")
    logger.info("=" * 50)
    
    try:
        # Inicializar componentes
        api_client = APIClient()
        data_processor = DataProcessor()
        
        # Gerar token
        logger.info("Gerando token...")
        token = api_client.generate_token()
        if not token:
            logger.error("Falha ao gerar token")
            return False
        
        # Consultar vendas
        logger.info("Consultando vendas...")
        vendas = api_client.fetch_vendas()
        if not vendas:
            logger.error("Nenhuma venda encontrada")
            return False
        
        # Analisar primeiras 5 vendas
        logger.info(f"Total de vendas encontradas: {len(vendas)}")
        logger.info("Analisando primeiras 5 vendas:")
        
        for i, venda in enumerate(vendas[:5]):
            valor = venda.get('VLTOTALPEDIDO', 'N/A')
            volume = venda.get('VLVOLUMEPEDIDO', 'N/A')
            empresa = venda.get('CDEMPRESA', 'N/A')
            
            logger.info(f"Venda {i+1}:")
            logger.info(f"  - Empresa: {empresa}")
            logger.info(f"  - Valor: {valor}")
            logger.info(f"  - Volume: {volume}")
            logger.info("-" * 30)
        
        # Verificar se há volumes diferentes de zero
        volumes_nao_zero = [v for v in vendas if v.get('VLVOLUMEPEDIDO', 0) not in [0, '0', '', None]]
        logger.info(f"Vendas com volume > 0: {len(volumes_nao_zero)} de {len(vendas)}")
        
        if volumes_nao_zero:
            logger.info("Exemplos de vendas com volume:")
            for i, venda in enumerate(volumes_nao_zero[:3]):
                valor = venda.get('VLTOTALPEDIDO', 'N/A')
                volume = venda.get('VLVOLUMEPEDIDO', 'N/A')
                logger.info(f"  Venda {i+1}: Valor={valor}, Volume={volume}")
        
        logger.info("=" * 50)
        logger.info("TESTE CONCLUÍDO")
        logger.info("=" * 50)
        
        return True
        
    except Exception as e:
        logger.error(f"Erro durante o teste: {str(e)}")
        return False

if __name__ == "__main__":
    main()