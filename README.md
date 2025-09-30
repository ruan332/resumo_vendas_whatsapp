# Sistema de Resumo de Vendas via WhatsApp

Sistema automatizado para coleta, processamento e envio de resumos de vendas via WhatsApp, integrado com APIs de vendas e WhatsApp.

## 🚀 Funcionalidades

- **Coleta automática de dados** de vendas, vendedores e empresas via API
- **Processamento inteligente** com mapeamento automático de UFs
- **Relatórios personalizados** por estado/região
- **Envio automático** via WhatsApp para grupos específicos
- **Logs detalhados** para monitoramento e debug
- **Configuração flexível** via variáveis de ambiente

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Acesso às APIs de vendas
- Token válido da API WhatsApp
- Conexão com internet

## 🔧 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/resumo_vendas_whatsapp.git
cd resumo_vendas_whatsapp
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente

Copie o arquivo de exemplo e configure suas credenciais:
```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:
```env
# Configurações da API Principal
API_BASE_URL=http://lubnord.wmw.com.br:8087/lubnordws
API_AUTHORIZATION=Basic_sua_autorizacao_aqui
API_USERNAME=seu_usuario_aqui
API_PASSWORD=sua_senha_aqui

# Configurações do WhatsApp
WHATSAPP_API_URL=https://api.chatweb.souchat.app/api/messages/send
WHATSAPP_TOKEN=seu_token_whatsapp_aqui
```

### 4. Configure os grupos WhatsApp

Edite o arquivo `config.json` com os números dos grupos:
```json
{
  "grupos_whatsapp": {
    "CE": {
      "nome": "Vendas Ceará",
      "numero": "5588999999999",
      "descricao": "Grupo para vendas do Ceará"
    }
  }
}
```

## 🎯 Uso

### Execução Principal
```bash
python main.py
```

### Teste de Conectividade
```bash
python main.py --test
```

### Usando os scripts batch (Windows)
```bash
# Execução principal
run.bat

# Teste de conectividade
test.bat
```

## 📊 Fluxo do Sistema

1. **Autenticação**: Gera token de acesso à API
2. **Coleta de Dados**: Busca vendas, vendedores e empresas
3. **Processamento**: Relaciona dados e mapeia UFs
4. **Geração de Relatórios**: Cria resumos por estado
5. **Envio WhatsApp**: Envia relatórios para grupos específicos

## 📁 Estrutura do Projeto

```
resumo_vendas_whatsapp/
├── main.py                 # Script principal
├── api_client.py          # Cliente para APIs
├── data_processor.py      # Processamento de dados
├── whatsapp_sender.py     # Envio via WhatsApp
├── config.py              # Configurações
├── config.json            # Grupos WhatsApp
├── requirements.txt       # Dependências
├── .env.example          # Template de variáveis
├── .gitignore            # Arquivos ignorados
├── run.bat               # Script Windows (execução)
├── test.bat              # Script Windows (teste)
└── README.md             # Documentação
```

## 🔐 Segurança

- **Credenciais protegidas**: Todas as credenciais são armazenadas em variáveis de ambiente
- **Arquivo .env**: Nunca commitado no repositório
- **Logs seguros**: Não expõem informações sensíveis
- **Validação**: Verifica variáveis obrigatórias na inicialização

## 📝 Logs

O sistema gera logs detalhados em:
- **Console**: Informações em tempo real
- **Arquivo**: `resumo_vendas.log` (rotacionado automaticamente)

Níveis de log:
- `INFO`: Operações normais
- `WARNING`: Situações de atenção
- `ERROR`: Erros que impedem execução

## 🛠️ Desenvolvimento

### Estrutura de Dados

**Vendas**: Contém `VLTOTALPEDIDO`, `CDREPRESENTANTE`, `CDEMPRESA`
**Vendedores**: Contém `CDREPRESENTANTE`, `NMREPRESENTANTE`
**Empresas**: Contém `CDEMPRESA`, `NMEMPRESA`, mapeadas para UF

### Mapeamento de UFs
```python
UF_MAPPING = {
    'LSO': 'CE',  # Ceará
    'LFO': 'CE',  # Ceará
    'LTE': 'PI',  # Piauí
    'LTI': 'PI',  # Piauí
    'LSU': 'MA',  # Maranhão
    'LCA': 'PB',  # Paraíba
    'LPA': 'RN',  # Rio Grande do Norte
    'LIM': 'MA'   # Maranhão
}
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Suporte

Para suporte ou dúvidas:
- Abra uma [issue](https://github.com/seu-usuario/resumo_vendas_whatsapp/issues)
- Entre em contato via email

## 🔄 Changelog

### v1.0.0
- ✅ Sistema completo de coleta e envio
- ✅ Integração com APIs de vendas e WhatsApp
- ✅ Processamento automático de dados
- ✅ Logs detalhados
- ✅ Configuração via variáveis de ambiente
- ✅ Scripts batch para Windows