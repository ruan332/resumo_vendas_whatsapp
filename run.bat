@echo off
echo ========================================
echo  SISTEMA DE RESUMO DE VENDAS WHATSAPP
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python não encontrado. Instale Python primeiro.
    pause
    exit /b 1
)

REM Verificar se requirements.txt existe
if not exist requirements.txt (
    echo ERRO: Arquivo requirements.txt não encontrado.
    pause
    exit /b 1
)

REM Instalar dependências se necessário
echo Verificando dependências...
pip install -r requirements.txt

echo.
echo Executando sistema...
echo.

REM Executar o script principal
python main.py

echo.
echo Execução finalizada.
pause