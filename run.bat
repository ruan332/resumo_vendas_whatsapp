@echo off
setlocal enabledelayedexpansion

REM ========================================
REM  SISTEMA DE RESUMO DE VENDAS WHATSAPP
REM  Versão otimizada para Agendador de Tarefas
REM ========================================

REM Definir diretório do script como diretório de trabalho
cd /d "%~dp0"

REM Configurar arquivo de log com timestamp
set "LOGFILE=%~dp0execution.log"
set "TIMESTAMP=%date% %time%"

REM Função para log
echo [%TIMESTAMP%] ========================================== >> "%LOGFILE%"
echo [%TIMESTAMP%] Iniciando execução do sistema >> "%LOGFILE%"
echo [%TIMESTAMP%] Diretório: %CD% >> "%LOGFILE%"

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [%TIMESTAMP%] ERRO: Python não encontrado >> "%LOGFILE%"
    echo ERRO: Python não encontrado. Verifique a instalação.
    exit /b 1
)

REM Verificar se .env existe
if not exist ".env" (
    echo [%TIMESTAMP%] AVISO: Arquivo .env não encontrado >> "%LOGFILE%"
    echo AVISO: Configure o arquivo .env com suas credenciais
)

REM Verificar se requirements.txt existe
if not exist "requirements.txt" (
    echo [%TIMESTAMP%] ERRO: requirements.txt não encontrado >> "%LOGFILE%"
    echo ERRO: Arquivo requirements.txt não encontrado
    exit /b 1
)

REM Log da versão do Python
for /f "tokens=*" %%i in ('python --version 2^>^&1') do (
    echo [%TIMESTAMP%] %%i >> "%LOGFILE%"
)

REM Executar o script principal
echo [%TIMESTAMP%] Executando main.py... >> "%LOGFILE%"
python main.py >> "%LOGFILE%" 2>&1

REM Capturar código de saída
set "EXIT_CODE=%ERRORLEVEL%"
echo [%TIMESTAMP%] Script finalizado com código: %EXIT_CODE% >> "%LOGFILE%"

if %EXIT_CODE% equ 0 (
    echo [%TIMESTAMP%] Execução bem-sucedida >> "%LOGFILE%"
    echo Execução concluída com sucesso
) else (
    echo [%TIMESTAMP%] Execução falhou >> "%LOGFILE%"
    echo Execução falhou. Verifique o log: %LOGFILE%
)

echo [%TIMESTAMP%] ========================================== >> "%LOGFILE%"

REM Script finaliza automaticamente sem pause
exit /b %EXIT_CODE%