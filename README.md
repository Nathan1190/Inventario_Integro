# Inventario_Integro

## Instalación y uso con Docker

1. Instala [Docker Desktop](https://www.docker.com/products/docker-desktop/).
2. Clona este repositorio.
3. Copia el archivo `.env/db_config.env` (no se sube por seguridad).
4. En la terminal, corre: 
docker-compose up --build
5. Accede a la app en [http://localhost:8000/](http://localhost:8000/)

## Comandos útiles

- Migraciones: docker-compose exec web python manage.py migrate
- Crear superusuario: docker-compose exec web python manage.py createsuperuser