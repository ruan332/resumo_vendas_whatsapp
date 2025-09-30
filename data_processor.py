"""
Processador de dados de vendas
"""

import logging
from config import UF_MAPPING

class DataProcessor:
    """Processador para manipulação e formatação dos dados"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def add_uf_to_empresas(self, empresas):
        """
        Adiciona coluna UF às empresas baseado no mapeamento
        
        Args:
            empresas (list): Lista de empresas
            
        Returns:
            list: Lista de empresas com UF adicionada
        """
        try:
            for empresa in empresas:
                sigla = empresa.get('NMEMPRESACURTO', '')
                empresa['UF'] = UF_MAPPING.get(sigla, 'DESCONHECIDO')
            
            self.logger.info(f"UF adicionada a {len(empresas)} empresas")
            return empresas
            
        except Exception as e:
            self.logger.error(f"Erro ao adicionar UF às empresas: {str(e)}")
            return empresas
    
    def relacionar_dados(self, vendas, vendedores, empresas):
        """
        Relaciona dados de vendas com vendedores e empresas
        
        Args:
            vendas (list): Lista de vendas
            vendedores (list): Lista de vendedores
            empresas (list): Lista de empresas
            
        Returns:
            list: Lista de vendas relacionadas
        """
        try:
            # Criar dicionários para lookup rápido
            vendedores_dict = {v['CDREPRESENTANTE']: v for v in vendedores}
            empresas_dict = {e['CDEMPRESA']: e for e in empresas}
            
            vendas_relacionadas = []
            
            for venda in vendas:
                cd_representante = venda.get('CDREPRESENTANTE')
                cd_empresa = venda.get('CDEMPRESA')
                
                # Buscar dados do vendedor
                vendedor = vendedores_dict.get(cd_representante)
                if not vendedor:
                    continue  # Pula vendas sem vendedor válido
                
                # Buscar dados da empresa
                empresa = empresas_dict.get(cd_empresa)
                if not empresa:
                    continue  # Pula vendas sem empresa válida
                
                # Criar registro relacionado
                venda_relacionada = {
                    'Base': empresa.get('NMEMPRESACURTO', ''),
                    'Consultor': vendedor.get('NMREPRESENTANTE', ''),
                    'Valor': venda.get('VLTOTALPEDIDO', '0'),
                    'Volume': venda.get('VLVOLUMEPEDIDO', '0'),
                    'DataEmissao': venda.get('DTEMISSAO', ''),
                    'UF': empresa.get('UF', 'DESCONHECIDO'),
                    'CDEMPRESA': cd_empresa,
                    'CDREPRESENTANTE': cd_representante
                }
                
                vendas_relacionadas.append(venda_relacionada)
            
            self.logger.info(f"Relacionadas {len(vendas_relacionadas)} vendas válidas de {len(vendas)} totais")
            return vendas_relacionadas
            
        except Exception as e:
            self.logger.error(f"Erro ao relacionar dados: {str(e)}")
            return []
    
    def agrupar_por_uf(self, vendas_relacionadas):
        """
        Agrupa vendas por UF
        
        Args:
            vendas_relacionadas (list): Lista de vendas relacionadas
            
        Returns:
            dict: Dicionário com vendas agrupadas por UF
        """
        try:
            vendas_por_uf = {}
            
            for venda in vendas_relacionadas:
                uf = venda.get('UF', 'DESCONHECIDO')
                
                if uf not in vendas_por_uf:
                    vendas_por_uf[uf] = []
                
                vendas_por_uf[uf].append(venda)
            
            self.logger.info(f"Vendas agrupadas em {len(vendas_por_uf)} UFs")
            return vendas_por_uf
            
        except Exception as e:
            self.logger.error(f"Erro ao agrupar por UF: {str(e)}")
            return {}
    
    def abreviar_nome(self, nome_completo):
        """
        Abrevia nome mantendo primeiro nome e inicial do último
        
        Args:
            nome_completo (str): Nome completo
            
        Returns:
            str: Nome abreviado
        """
        try:
            partes = nome_completo.strip().split(' ')
            if len(partes) > 1:
                return f"{partes[0]} {partes[-1][0]}."
            return nome_completo
        except:
            return nome_completo
    
    def gerar_relatorio_uf(self, vendas_uf):
        """
        Gera relatório formatado para uma UF
        
        Args:
            vendas_uf (list): Lista de vendas de uma UF
            
        Returns:
            str: Relatório formatado
        """
        try:
            if not vendas_uf:
                return "Nenhuma venda encontrada hoje."
            
            # Agregar vendas por consultor
            vendas_por_consultor = {}
            
            for venda in vendas_uf:
                consultor = venda.get('Consultor', 'Não informado')
                valor_raw = venda.get('Valor', 0)
                volume_raw = venda.get('Volume', 0)
                
                # Converter valor corretamente
                try:
                    # Se já é número, usar diretamente
                    if isinstance(valor_raw, (int, float)):
                        valor_numerico = float(valor_raw)
                    else:
                        # Se é string, limpar apenas caracteres de moeda
                        valor_string = str(valor_raw)
                        valor_limpo = valor_string.replace('R$', '').replace(' ', '').strip()
                        # Não remover pontos decimais - apenas converter
                        valor_numerico = float(valor_limpo)
                except:
                    valor_numerico = 0.0
                
                # Converter volume corretamente
                try:
                    # Se já é número, usar diretamente
                    if isinstance(volume_raw, (int, float)):
                        volume_numerico = float(volume_raw)
                    else:
                        # Se é string, converter para float
                        volume_string = str(volume_raw)
                        volume_limpo = volume_string.replace(' ', '').strip()
                        volume_numerico = float(volume_limpo)
                except:
                    volume_numerico = 0.0
                
                if consultor not in vendas_por_consultor:
                    vendas_por_consultor[consultor] = {'total': 0, 'volume_total': 0, 'quantidade': 0}
                
                vendas_por_consultor[consultor]['total'] += valor_numerico
                vendas_por_consultor[consultor]['volume_total'] += volume_numerico
                vendas_por_consultor[consultor]['quantidade'] += 1
            
            # Ordenar por maior valor
            consultores_ordenados = sorted(
                vendas_por_consultor.items(),
                key=lambda x: x[1]['total'],
                reverse=True
            )
            
            # Montar relatório
            relatorio = "📊 *RELATÓRIO DE VENDAS*\n\n"
            
            total_geral = 0
            total_volume = 0
            total_pedidos = 0
            
            for consultor, dados in consultores_ordenados:
                nome_abreviado = self.abreviar_nome(consultor)
                valor_formatado = f"R$ {dados['total']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                volume_formatado = f"{dados['volume_total']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                
                relatorio += f"👤 *{nome_abreviado}*\n"
                relatorio += f"   📦 Pedidos: {dados['quantidade']}\n"
                relatorio += f"   💰 Total: {valor_formatado}\n"
                relatorio += f"   🛢️ Volume: {volume_formatado} L\n\n"
                
                total_geral += dados['total']
                total_volume += dados['volume_total']
                total_pedidos += dados['quantidade']
            
            # Totais gerais
            total_formatado = f"R$ {total_geral:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            volume_total_formatado = f"{total_volume:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            relatorio += "=" * 30 + "\n"
            relatorio += f"🎯 *TOTAL GERAL*\n"
            relatorio += f"📦 Total de Pedidos: {total_pedidos}\n"
            relatorio += f"💰 Valor Total: {total_formatado}\n"
            relatorio += f"🛢️ Volume Total: {volume_total_formatado} L\n"
            
            return relatorio
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar relatório: {str(e)}")
            return "Erro ao gerar relatório de vendas."