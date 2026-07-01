@echo off
title Instalador - Inventario Integro
color 0A

echo ==========================================
echo   INSTALADOR INVENTARIO INTEGRO
echo ==========================================
echo.

echo Verificando Docker...
docker --version >nul 2>&1

if errorlevel 1 (
    echo ERROR: Docker no esta instalado o no esta abierto.
    echo Instala Docker Desktop y vuelve a intentar.
    pause
    exit /b
)

echo Docker encontrado correctamente.
echo.

echo Creando archivo .env si no existe...

if not exist ".env" (
    echo POSTGRES_DB=inventario_db>>.env
    echo POSTGRES_USER=inventario_user>>.env
    echo POSTGRES_PASSWORD=inventario_pass>>.env
    echo.>>.env
    echo DB_NAME=inventario_db>>.env
    echo DB_USER=inventario_user>>.env
    echo DB_PASSWORD=inventario_pass>>.env
    echo DB_HOST=db>>.env
    echo DB_PORT=5432>>.env
    echo.>>.env
    echo DEBUG=False>>.env
    echo ALLOWED_HOSTS=localhost,127.0.0.1>>.env
    echo.>>.env
    echo DJANGO_SUPERUSER_USERNAME=admin>>.env
    echo DJANGO_SUPERUSER_EMAIL=admin@local.com>>.env
    echo DJANGO_SUPERUSER_PASSWORD=Admin12345>>.env
)

echo.
echo Construyendo y levantando contenedores...
docker compose up -d --build

echo.
echo Esperando que la base de datos inicie...
timeout /t 10 /nobreak >nul

echo.
echo Ejecutando migraciones...
docker compose exec web python manage.py migrate --noinput

echo.
echo Recolectando archivos estaticos...
docker compose exec web python manage.py collectstatic --noinput

echo.
echo Creando usuario administrador inicial...
docker compose exec web python manage.py createsuperuser --noinput

echo.
echo Creando pantallas, roles base y asignando administrador...
docker compose exec web python manage.py seed_roles

echo.
echo ==========================================
echo Instalacion finalizada.
echo Usuario: admin
echo Clave: Admin12345
echo URL: http://localhost:8000/
echo ==========================================
echo.

start http://localhost:8000/

pause