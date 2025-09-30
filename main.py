"""
Script principal para geração e envio de resumo de vendas via WhatsApp
"""

import logging
import sys
from datetime import datetime
from api_client import APIClient
from data_processor import DataProcessor
from whatsapp_sender import WhatsAppSender

def setup_logging():
    """Configura sistema de logs"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('resumo_vendas.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    """Função principal do sistema"""
    
    # Configurar logs
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("=" * 50)
    logger.info("INICIANDO SISTEMA DE RESUMO DE VENDAS")
    logger.info("=" * 50)
    
    try:
        # Inicializar componentes
        api_client = APIClient()
        data_processor = DataProcessor()
        whatsapp_sender = WhatsAppSender()
        
        # Etapa 1: Gerar token de autenticação
        logger.info("ETAPA 1: Gerando token de autenticação...")
        token = api_client.generate_token()
        if not token:
            logger.error("Falha ao gerar token. Encerrando execução.")
            return False
        
        # Etapa 2: Consultar dados da API
        logger.info("ETAPA 2: Consultando dados da API...")
        
        # Consultar vendas do dia
        vendas = api_client.fetch_vendas()
        if vendas is None:
            logger.error("Falha ao consultar vendas. Encerrando execução.")
            return False
        
        # Consultar vendedores
        vendedores = api_client.fetch_vendedores()
        if vendedores is None:
            logger.error("Falha ao consultar vendedores. Encerrando execução.")
            return False
        
        # Consultar empresas
        empresas = api_client.fetch_empresas()
        if empresas is None:
            logger.error("Falha ao consultar empresas. Encerrando execução.")
            return False
        
        # Etapa 3: Processar dados
        logger.info("ETAPA 3: Processando dados...")
        
        # Adicionar UF às empresas
        empresas_com_uf = data_processor.add_uf_to_empresas(empresas)
        
        # Relacionar dados
        vendas_relacionadas = data_processor.relacionar_dados(vendas, vendedores, empresas_com_uf)
        
        if not vendas_relacionadas:
            logger.warning("Nenhuma venda válida encontrada para processar.")
            # Ainda assim, enviar mensagem informando que não há vendas
            mensagem_sem_vendas = "📊 *RELATÓRIO DE VENDAS*\n\n❌ Nenhuma venda encontrada hoje."
            
            # Enviar para todos os grupos
            for uf in ['CE', 'PI', 'MA', 'PB', 'RN']:
                whatsapp_sender.send_relatorio_uf(uf, mensagem_sem_vendas)
            
            logger.info("Mensagens de 'sem vendas' enviadas para todos os grupos.")
            return True
        
        # Agrupar por UF
        vendas_por_uf = data_processor.agrupar_por_uf(vendas_relacionadas)
        
        # Etapa 4: Gerar relatórios
        logger.info("ETAPA 4: Gerando relatórios por UF...")
        relatorios_por_uf = {}
        
        for uf, vendas_uf in vendas_por_uf.items():
            if uf != 'DESCONHECIDO':
                relatorio = data_processor.gerar_relatorio_uf(vendas_uf)
                relatorios_por_uf[uf] = relatorio
                logger.info(f"Relatório gerado para {uf}: {len(vendas_uf)} vendas")
        
        # Etapa 5: Enviar mensagens WhatsApp
        logger.info("ETAPA 5: Enviando mensagens WhatsApp...")
        
        # Testar conexão primeiro
        if not whatsapp_sender.test_connection():
            logger.warning("Problema na conexão WhatsApp, mas continuando...")
        
        # Enviar relatórios
        resultados = whatsapp_sender.send_relatorios_todas_ufs(relatorios_por_uf)
        
        # Verificar resultados
        sucessos = sum(1 for resultado in resultados.values() if resultado)
        total = len(resultados)
        
        logger.info(f"Envios concluídos: {sucessos}/{total} sucessos")
        
        # Etapa 6: Resumo final
        logger.info("ETAPA 6: Resumo da execução...")
        logger.info(f"- Vendas processadas: {len(vendas_relacionadas)}")
        logger.info(f"- UFs com vendas: {len(relatorios_por_uf)}")
        logger.info(f"- Mensagens enviadas: {sucessos}/{total}")
        
        if sucessos == total:
            logger.info("✅ EXECUÇÃO CONCLUÍDA COM SUCESSO!")
            return True
        else:
            logger.warning("⚠️ EXECUÇÃO CONCLUÍDA COM ALGUMAS FALHAS")
            return False
            
    except Exception as e:
        logger.error(f"ERRO CRÍTICO na execução: {str(e)}")
        return False
    
    finally:
        logger.info("=" * 50)
        logger.info("FIM DA EXECUÇÃO")
        logger.info("=" * 50)

def test_apis():
    """Função para testar conectividade com as APIs"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("TESTANDO CONECTIVIDADE COM APIS...")
    
    # Testar API principal
    api_client = APIClient()
    token = api_client.generate_token()
    
    if token:
        logger.info("✅ API principal: OK")
        
        # Testar endpoints
        vendas = api_client.fetch_vendas()
        vendedores = api_client.fetch_vendedores()
        empresas = api_client.fetch_empresas()
        
        logger.info(f"✅ Vendas: {len(vendas) if vendas else 0} registros")
        logger.info(f"✅ Vendedores: {len(vendedores) if vendedores else 0} registros")
        logger.info(f"✅ Empresas: {len(empresas) if empresas else 0} registros")
    else:
        logger.error("❌ API principal: FALHA")
    
    # Testar WhatsApp
    whatsapp_sender = WhatsAppSender()
    if whatsapp_sender.test_connection():
        logger.info("✅ WhatsApp API: OK")
    else:
        logger.error("❌ WhatsApp API: FALHA")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_apis()
    else:
        success = main()
        sys.exit(0 if success else 1)