@echo off
title Actualizar Inventario Integro
color 0E

echo Actualizando sistema...
docker compose down
docker compose up -d --build

echo.
echo Ejecutando migraciones...
docker compose exec web python manage.py migrate --noinput

echo.
echo Recolectando estaticos...
docker compose exec web python manage.py collectstatic --noinput

echo.
echo Actualizacion finalizada.
start http://localhost:8000/

pause