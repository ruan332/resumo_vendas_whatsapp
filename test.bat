@echo off
echo ========================================
echo  TESTE DE CONECTIVIDADE DAS APIS
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python não encontrado. Instale Python primeiro.
    pause
    exit /b 1
)

echo Testando conectividade com as APIs...
echo.

REM Executar teste
python main.py --test

echo.
echo Teste finalizado.
pause