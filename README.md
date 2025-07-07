# Agenda FastAPI

Aplicación de agenda de contactos construida con FastAPI, SQLAlchemy, SQLite y Jinja2. Permite operaciones CRUD sobre contactos y cuenta con pruebas automatizadas y despliegue mediante Docker.

## Descripción
Esta agenda permite crear, listar, editar y eliminar contactos. Incluye una interfaz web sencilla y una API REST.

## Requisitos
- Python 3.11+
- Docker (ver Dockerfile en https://github.com/Chdezreyes76/contacts-app/blob/master/Dockerfile)
- Docker Compose (opcional, para despliegue rápido)

## Instalación y ejecución local
1. Clona el repositorio:
   ```bash
   git clone https://github.com/tuusuario/agenda-fastapi.git
   cd agenda-fastapi
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta la aplicación:
   ```bash
   uvicorn app.main:app --reload
   ```
4. Accede a la app en [http://localhost:8000](http://localhost:8000)

## Pruebas
Ejecuta las pruebas con:
```bash
pytest
```

## Uso con Docker
### Construir y ejecutar localmente
```bash
docker build -t agenda-fastapi .
docker run -d -p 8000:8000 agenda-fastapi
```
Accede a [http://localhost:8000](http://localhost:8000)

### Ejecutar desde Docker Hub con Docker Compose
Crea un archivo `docker-compose.yml` como este:

```yaml
version: '3.8'
services:
  agenda:
    image: chdezreyes76/agenda-fastapi:latest
    ports:
      - "8000:8000"
    restart: unless-stopped
```

Luego ejecuta:
```bash
docker-compose up -d
```

## CI/CD
El pipeline de GitHub Actions realiza:
- Instalación de dependencias
- Ejecución de pruebas
- Build de la imagen Docker
- Push automático a Docker Hub

En este archivo esta el pipeline de CI/CD: https://github.com/Chdezreyes76/contacts-app/blob/master/.github/workflows/ci.yml
Y las ejecuciones del pipeline se pueden ver en la pestaña "Actions" del repositorio: https://github.com/Chdezreyes76/contacts-app/actions

## Enlace a Docker Hub
[[https://hub.docker.com/r/chdezreyes76/agenda-fastapi](https://hub.docker.com/r/chdezreyes76/agenda-fastapi)]



---

