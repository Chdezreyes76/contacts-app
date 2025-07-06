# Plan de Trabajo Detallado - Entregable 4

## Fase 1: Diseño y preparación del entorno
- Definir los requisitos mínimos de la agenda (campos: nombre, email, teléfono, etc.).
- Crear el entorno de trabajo local y el repositorio en GitHub.
- Crear el archivo `requirements.txt` con las dependencias:
  - fastapi
  - uvicorn
  - jinja2
  - sqlalchemy
  - pydantic
  - aiosqlite (opcional para async)
  - pytest

## Fase 2: Estructura del proyecto
- Crear la estructura de carpetas:
  - `/app` (código fuente)
    - `/templates` (plantillas Jinja2)
    - `/static` (opcional, para CSS)
    - `main.py` (punto de entrada FastAPI)
    - `models.py` (modelos SQLAlchemy)
    - `schemas.py` (modelos Pydantic)
    - `database.py` (conexión y utilidades SQLite)
    - `crud.py` (operaciones CRUD)
    - `routes.py` (rutas de la API y vistas)
  - `/tests` (pruebas unitarias)

## Fase 3: Backend (FastAPI + SQLite + SQLAlchemy + Pydantic)
- Configurar la base de datos SQLite y los modelos con SQLAlchemy.
- Definir los esquemas de Pydantic para validación de datos.
- Implementar operaciones CRUD:
  - Crear contacto
  - Listar contactos
  - Editar contacto
  - Eliminar contacto
- Crear rutas API y vistas para cada operación.

## Fase 4: Frontend (Jinja2)
- Crear plantillas HTML sencillas para:
  - Listar contactos
  - Formulario de alta/edición de contacto
  - Confirmación de borrado
- Integrar las plantillas con las rutas FastAPI usando Jinja2.

## Fase 5: Pruebas
- Implementar pruebas unitarias con pytest para:
  - Operaciones CRUD
  - Validación de datos
- Probar la aplicación localmente y corregir errores.

## Fase 6: Contenerización con Docker
- Instalar y configurar Docker en la máquina local (si no está hecho).
- Crear el archivo `Dockerfile` en la raíz del proyecto:
  - Usar una imagen base oficial de Python.
  - Copiar el código y `requirements.txt` al contenedor.
  - Instalar dependencias.
  - Exponer el puerto 8000.
  - Definir el comando para ejecutar la app con Uvicorn.
- Probar la construcción y ejecución del contenedor localmente.

## Fase 7: Configuración del pipeline de CI/CD con GitHub Actions
- Crear el directorio `.github/workflows` y un archivo YAML para el workflow (por ejemplo, `ci.yml`).
- Definir las etapas del pipeline:
  - Checkout del código.
  - Instalación de dependencias.
  - Ejecución de pruebas con pytest.
  - Construcción de la imagen Docker.
  - Login a Docker Hub (usando secretos).
  - Push de la imagen a Docker Hub.
- Probar el pipeline y corregir errores si aparecen.

## Fase 8: Configuración de Docker Hub y secretos
- Crear una cuenta en Docker Hub (si no se tiene).
- Crear un repositorio en Docker Hub para la imagen.
- Configurar los secretos `DOCKERHUB_USERNAME` y `DOCKERHUB_TOKEN` en GitHub.

## Fase 9: Documentación
- Crear o actualizar el `README.md` con:
  - Descripción del proyecto.
  - Instrucciones para construir, probar y ejecutar la aplicación localmente y con Docker.
  - Instrucciones para ejecutar el pipeline y verificar el despliegue.
  - Información sobre las pruebas y cómo ejecutarlas.
  - Enlace a la imagen en Docker Hub.

## Fase 10: Verificación y entrega
- Verificar que todo el flujo funciona: pruebas, build, push a Docker Hub.
- Hacer pruebas finales de la aplicación desde el contenedor.
- Subir todos los archivos al repositorio y comprobar que el pipeline se ejecuta correctamente.
- Revisar la rúbrica y checklist de requisitos antes de entregar.
