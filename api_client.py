"""
Cliente para comunicação com as APIs do sistema
"""

import requests
import logging
from datetime import datetime
from config import *

class APIClient:
    """Cliente para comunicação com as APIs"""
    
    def __init__(self):
        self.token = None
        self.logger = logging.getLogger(__name__)
    
    def generate_token(self):
        """
        Gera token de autenticação para a API
        
        Returns:
            str: Token de acesso ou None em caso de erro
        """
        try:
            headers = {
                'Authorization': API_AUTHORIZATION,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            data = {
                'grant_type': 'password',
                'username': API_USERNAME,
                'password': API_PASSWORD
            }
            
            self.logger.info("Gerando token de autenticação...")
            response = requests.post(TOKEN_URL, headers=headers, data=data)
            
            if response.status_code == 200:
                token_data = response.json()
                self.token = token_data.get('access_token')
                self.logger.info("Token gerado com sucesso")
                return self.token
            else:
                self.logger.error(f"Erro ao gerar token: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            self.logger.error(f"Erro ao gerar token: {str(e)}")
            return None
    
    def get_auth_headers(self):
        """
        Retorna headers com autorização Bearer
        
        Returns:
            dict: Headers com token de autorização
        """
        if not self.token:
            self.generate_token()
        
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
    
    def fetch_vendas(self, data_emissao=None):
        """
        Consulta vendas do dia
        
        Args:
            data_emissao (str): Data no formato DD/MM/YYYY. Se None, usa data atual
            
        Returns:
            list: Lista de vendas ou None em caso de erro
        """
        try:
            if not data_emissao:
                data_emissao = datetime.now().strftime("%d/%m/%Y")
            
            payload = {
                "fields": [
                    "CDEMPRESA",
                    "CDREPRESENTANTE", 
                    "CDUSUARIOEMISSAO",
                    "FLORIGEMPEDIDO",
                    "CDTIPOPAGAMENTO",
                    "DTEMISSAO",
                    "VLTOTALPEDIDO",
                    "VLVOLUMEPEDIDO",
                    "FLCONTROLEERP"
                ],
                "filters": {
                    "DTEMISSAO": data_emissao
                }
            }
            
            self.logger.info(f"Consultando vendas do dia {data_emissao}...")
            response = requests.post(VENDAS_URL, headers=self.get_auth_headers(), json=payload)
            
            if response.status_code == 200:
                vendas = response.json()
                self.logger.info(f"Encontradas {len(vendas)} vendas")
                return vendas
            else:
                self.logger.error(f"Erro ao consultar vendas: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            self.logger.error(f"Erro ao consultar vendas: {str(e)}")
            return None
    
    def fetch_vendedores(self):
        """
        Consulta lista de vendedores ativos
        
        Returns:
            list: Lista de vendedores ou None em caso de erro
        """
        try:
            payload = {
                "fields": [
                    "CDEMPRESA",
                    "CDREPRESENTANTE",
                    "NMREPRESENTANTE", 
                    "FLATIVO"
                ],
                "filters": {
                    "FLATIVO": "S",
                    "FLTIPOCADASTRO": "R"
                }
            }
            
            self.logger.info("Consultando vendedores...")
            response = requests.post(VENDEDORES_URL, headers=self.get_auth_headers(), json=payload)
            
            if response.status_code == 200:
                vendedores = response.json()
                self.logger.info(f"Encontrados {len(vendedores)} vendedores")
                return vendedores
            else:
                self.logger.error(f"Erro ao consultar vendedores: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            self.logger.error(f"Erro ao consultar vendedores: {str(e)}")
            return None
    
    def fetch_empresas(self):
        """
        Consulta lista de empresas ativas
        
        Returns:
            list: Lista de empresas ou None em caso de erro
        """
        try:
            payload = {
                "fields": [
                    "CDEMPRESA",
                    "NMEMPRESA",
                    "NMEMPRESACURTO"
                ],
                "filters": {
                    "FLATIVO": "S"
                }
            }
            
            self.logger.info("Consultando empresas...")
            response = requests.post(EMPRESAS_URL, headers=self.get_auth_headers(), json=payload)
            
            if response.status_code == 200:
                empresas = response.json()
                self.logger.info(f"Encontradas {len(empresas)} empresas")
                return empresas
            else:
                self.logger.error(f"Erro ao consultar empresas: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            self.logger.error(f"Erro ao consultar empresas: {str(e)}")
            return None