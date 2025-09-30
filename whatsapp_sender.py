"""
Cliente para envio de mensagens WhatsApp
"""

import requests
import json
import logging
from config import WHATSAPP_API_URL, WHATSAPP_TOKEN

class WhatsAppSender:
    """Cliente para envio de mensagens via WhatsApp"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.grupos_config = self.load_grupos_config()
    
    def load_grupos_config(self):
        """
        Carrega configuração dos grupos WhatsApp
        
        Returns:
            dict: Configuração dos grupos
        """
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('grupos_whatsapp', {})
        except Exception as e:
            self.logger.error(f"Erro ao carregar configuração dos grupos: {str(e)}")
            return {}
    
    def send_message(self, numero, mensagem):
        """
        Envia mensagem para um número WhatsApp
        
        Args:
            numero (str): Número do WhatsApp
            mensagem (str): Mensagem a ser enviada
            
        Returns:
            bool: True se enviado com sucesso, False caso contrário
        """
        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {WHATSAPP_TOKEN}'
            }
            
            payload = {
                'number': numero,
                'body': mensagem
            }
            
            self.logger.info(f"Enviando mensagem para {numero}...")
            response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
            
            if response.status_code == 200:
                self.logger.info(f"Mensagem enviada com sucesso para {numero}")
                return True
            else:
                self.logger.error(f"Erro ao enviar mensagem para {numero}: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"Erro ao enviar mensagem para {numero}: {str(e)}")
            return False
    
    def send_relatorio_uf(self, uf, relatorio):
        """
        Envia relatório para o grupo da UF específica
        
        Args:
            uf (str): Sigla da UF
            relatorio (str): Relatório formatado
            
        Returns:
            bool: True se enviado com sucesso, False caso contrário
        """
        try:
            if uf not in self.grupos_config:
                self.logger.warning(f"Configuração não encontrada para UF: {uf}")
                return False
            
            grupo = self.grupos_config[uf]
            numero = grupo.get('numero')
            nome_grupo = grupo.get('nome', f'Grupo {uf}')
            
            if not numero:
                self.logger.error(f"Número não configurado para UF: {uf}")
                return False
            
            # Adicionar cabeçalho com UF
            mensagem_completa = f"🏢 *{nome_grupo.upper()}*\n"
            mensagem_completa += f"📅 {self.get_data_atual()}\n\n"
            mensagem_completa += relatorio
            
            return self.send_message(numero, mensagem_completa)
            
        except Exception as e:
            self.logger.error(f"Erro ao enviar relatório para UF {uf}: {str(e)}")
            return False
    
    def send_relatorios_todas_ufs(self, relatorios_por_uf):
        """
        Envia relatórios para todas as UFs
        
        Args:
            relatorios_por_uf (dict): Dicionário com relatórios por UF
            
        Returns:
            dict: Resultado dos envios por UF
        """
        resultados = {}
        
        for uf, relatorio in relatorios_por_uf.items():
            if uf == 'DESCONHECIDO':
                self.logger.warning("Pulando UF DESCONHECIDO")
                continue
                
            resultado = self.send_relatorio_uf(uf, relatorio)
            resultados[uf] = resultado
            
            if resultado:
                self.logger.info(f"Relatório enviado com sucesso para {uf}")
            else:
                self.logger.error(f"Falha ao enviar relatório para {uf}")
        
        return resultados
    
    def get_data_atual(self):
        """
        Retorna data atual formatada
        
        Returns:
            str: Data formatada
        """
        from datetime import datetime
        return datetime.now().strftime("%d/%m/%Y")
    
    def test_connection(self):
        """
        Testa conexão com a API do WhatsApp
        
        Returns:
            bool: True se conexão OK, False caso contrário
        """
        try:
            headers = {
                'Authorization': f'Bearer {WHATSAPP_TOKEN}'
            }
            
            # Fazer uma requisição simples para testar
            response = requests.get(WHATSAPP_API_URL.replace('/send', ''), headers=headers)
            
            if response.status_code in [200, 404]:  # 404 é esperado para GET na URL de send
                self.logger.info("Conexão com WhatsApp API OK")
                return True
            else:
                self.logger.error(f"Erro na conexão WhatsApp API: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"Erro ao testar conexão WhatsApp: {str(e)}")
            return False