@echo off
title Iniciar Inventario Integro
color 0A

echo Iniciando Inventario Integro...
docker compose up -d

echo.
echo Sistema iniciado.
echo Abriendo navegador...
start http://localhost:8000/

pause