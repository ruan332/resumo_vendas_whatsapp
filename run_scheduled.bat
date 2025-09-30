@echo off
REM ========================================
REM  EXECUTAR SISTEMA VIA AGENDADOR DE TAREFAS
REM  Este arquivo é específico para uso no Agendador
REM ========================================

REM Definir diretório do script
cd /d "%~dp0"

REM Executar o run.bat (agora sempre fecha automaticamente)
call "%~dp0run.bat"

REM Sair com o mesmo código de saída
exit /b %ERRORLEVEL%