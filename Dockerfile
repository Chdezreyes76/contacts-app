# Utiliza una imagen base oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de dependencias primero para aprovechar el cache de Docker
COPY requirements.txt ./

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt


# Copia el resto del código fuente de la aplicación
COPY ./app ./app

# Copia archivos estáticos y plantillas (por si acaso)
COPY ./app/static ./app/static
COPY ./app/templates ./app/templates

# Copia Alembic y su configuración
COPY ./alembic ./alembic
COPY alembic.ini ./

# Copia la carpeta de tests (para ejecución de pruebas en CI/CD)
COPY ./tests ./tests

# Copia archivos de configuración y base de datos si es necesario (opcional)
# COPY agenda.db ./

# Expone el puerto 8000 para FastAPI
EXPOSE 8000

# Ejecuta migraciones Alembic antes de arrancar la app
CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000
