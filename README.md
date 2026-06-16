# Inventario Íntegro

Sistema web para la gestión de inventario institucional, desarrollado con **Django**, **PostgreSQL** y **Docker**.

El proyecto está preparado para ejecutarse de forma local usando contenedores Docker. Esto evita instalar Python, PostgreSQL y dependencias directamente en Windows.

---

## Requisitos previos

Antes de instalar el sistema en una computadora nueva, se necesita:

1. **Docker Desktop** instalado y abierto.
2. **Git** instalado, si se va a clonar o actualizar el repositorio desde GitHub.
3. Acceso al repositorio del proyecto.
4. Archivo `.env` configurado en la raíz del proyecto.

---

## `.env` de ejemplo

POSTGRES_DB=inventario_db
POSTGRES_USER=inventario_user
POSTGRES_PASSWORD=inventario_pass

DB_NAME=inventario_db
DB_USER=inventario_user
DB_PASSWORD=inventario_pass
DB_HOST=db
DB_PORT=5432

DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

---

## Instalación rápida con archivos `.bat`

La forma más sencilla de instalar y ejecutar el sistema en Windows es usando archivos `.bat`.

Se recomienda tener estos archivos en la raíz del proyecto:

```text
Inventario_Integro/
├── INSTALAR.bat
├── INICIAR.bat
├── DETENER.bat
├── ACTUALIZAR.bat
├── ABRIR_SISTEMA.bat
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── manage.py
└── .env

