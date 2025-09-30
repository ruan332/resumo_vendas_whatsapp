# 📅 Configuração no Agendador de Tarefas do Windows

## 🔧 **Problema Identificado e Solucionado**

O problema do arquivo `run.bat` fechar imediatamente no Agendador de Tarefas foi **corrigido**. As principais causas eram:

1. **Comando `pause`** - Travava a execução esperando input do usuário
2. **Falta de logs** - Não havia como debugar problemas
3. **Diretório de trabalho** - Não estava definido corretamente
4. **Saída de erro** - Não era capturada adequadamente

---

## ✅ **Arquivos Criados/Modificados**

### 📄 `run.bat` (Atualizado)
- ✅ **Logs detalhados** em `execution.log`
- ✅ **Fecha automaticamente** após execução (sem pause)
- ✅ **Diretório de trabalho** definido automaticamente
- ✅ **Captura de erros** completa
- ✅ **Timestamps** em todas as operações

### 📄 `run_scheduled.bat` (Novo)
- ✅ **Arquivo específico** para o agendador
- ✅ **Chama o run.bat** com parâmetro `--scheduled`
- ✅ **Mais simples** e direto

---

## 🚀 **Como Configurar no Agendador de Tarefas**

### **Opção 1: Usar run_scheduled.bat (Recomendado)**

1. **Abrir Agendador de Tarefas**
   - Pressione `Win + R` → Digite `taskschd.msc` → Enter

2. **Criar Nova Tarefa**
   - Clique em "Criar Tarefa Básica..." ou "Criar Tarefa..."

3. **Configurações da Tarefa**
   - **Nome**: `Sistema Resumo Vendas WhatsApp`
   - **Descrição**: `Envio automático de resumo de vendas via WhatsApp`

4. **Disparador (Quando executar)**
   - **Diariamente** às `18:00` (ou horário desejado)
   - **Repetir**: Conforme necessário

5. **Ação (O que executar)**
   - **Programa/script**: `C:\Projetos\Scripts\resumo_vendas_whatsapp\run_scheduled.bat`
   - **Iniciar em**: `C:\Projetos\Scripts\resumo_vendas_whatsapp`

6. **Condições**
   - ✅ **Executar apenas se o computador estiver conectado à rede**
   - ✅ **Acordar o computador para executar esta tarefa** (se necessário)

7. **Configurações**
   - ✅ **Permitir que a tarefa seja executada sob demanda**
   - ✅ **Executar tarefa assim que possível após um início agendado perdido**
   - **Se a tarefa falhar, reiniciar a cada**: `1 minuto`
   - **Tentar reiniciar até**: `3 vezes`

### **Opção 2: Usar run.bat diretamente**

- **Programa/script**: `C:\Projetos\Scripts\resumo_vendas_whatsapp\run.bat`
- **Iniciar em**: `C:\Projetos\Scripts\resumo_vendas_whatsapp`

> **Nota**: Ambos os arquivos agora **fecham automaticamente** após a execução, sem necessidade de interação do usuário.

---

## 🔍 **Como Monitorar e Debugar**

### **1. Arquivo de Log Principal**
```
C:\Projetos\Scripts\resumo_vendas_whatsapp\execution.log
```
- **Contém**: Timestamps, status de execução, erros
- **Atualizado**: A cada execução
- **Formato**: `[DATA HORA] MENSAGEM`

### **2. Log Detalhado do Sistema**
```
C:\Projetos\Scripts\resumo_vendas_whatsapp\resumo_vendas.log
```
- **Contém**: Logs detalhados do Python
- **Inclui**: API calls, processamento, envios WhatsApp

### **3. Histórico do Agendador**
- **Agendador de Tarefas** → **Biblioteca do Agendador de Tarefas**
- Encontre sua tarefa → **Histórico**
- Veja execuções, sucessos e falhas

---

## ⚠️ **Troubleshooting**

### **Se a tarefa não executar:**

1. **Verificar Permissões**
   - Execute o Agendador como **Administrador**
   - Configure a tarefa para **executar com privilégios mais altos**

2. **Verificar Usuário**
   - Configure para executar **estando o usuário conectado ou não**
   - Use a conta **SYSTEM** se necessário

3. **Verificar Caminhos**
   - Certifique-se que todos os caminhos estão **absolutos**
   - Teste manualmente: `.\run_scheduled.bat`

4. **Verificar .env**
   - Confirme que o arquivo `.env` existe
   - Verifique se todas as credenciais estão corretas

### **Se houver erros:**

1. **Consultar execution.log**
   ```
   [30/09/2025 17:25:57,99] ERRO: Descrição do erro
   ```

2. **Consultar resumo_vendas.log**
   ```
   2025-09-30 17:25:58,748 - __main__ - ERROR - Detalhes do erro
   ```

3. **Testar manualmente**
   ```cmd
   cd C:\Projetos\Scripts\resumo_vendas_whatsapp
   .\run_scheduled.bat
   ```

---

## 📊 **Exemplo de Execução Bem-Sucedida**

### **execution.log**
```
[30/09/2025 17:25:57,99] ==========================================
[30/09/2025 17:25:57,99] Iniciando execução do sistema
[30/09/2025 17:25:57,99] Diretório: C:\Projetos\Scripts\resumo_vendas_whatsapp
[30/09/2025 17:25:57,99] Python 3.12.10
[30/09/2025 17:25:57,99] Executando main.py...
[30/09/2025 17:27:32,391] Script finalizado com código: 0
[30/09/2025 17:27:32,391] Execução bem-sucedida
[30/09/2025 17:27:32,391] ==========================================
```

### **Resultado Esperado**
- ✅ **356 vendas processadas**
- ✅ **5 UFs identificadas**
- ✅ **5/5 mensagens enviadas**
- ✅ **Código de saída: 0**

---

## 🎯 **Dicas Importantes**

1. **Teste sempre manualmente** antes de agendar
2. **Monitore os logs** nas primeiras execuções
3. **Configure alertas** se a tarefa falhar
4. **Mantenha backups** dos arquivos de configuração
5. **Documente mudanças** nas credenciais

---

## 📞 **Suporte**

Se ainda houver problemas:

1. **Verifique os logs** em ambos os arquivos
2. **Teste manualmente** com `.\run_scheduled.bat`
3. **Confirme as credenciais** no arquivo `.env`
4. **Verifique a conectividade** com as APIs

O sistema está **100% funcional** e **testado** ✅