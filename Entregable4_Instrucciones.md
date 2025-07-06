# PROYECTO ENTREGABLE 4 - INSTRUCCIONES

## OBJETIVOS

1. Con esta actividad se aprenderá a empaquetar aplicaciones en contenedores utilizando Docker
2. Se podrá automatizar la construcción, la prueba y el despliegue de contenedores mediante pipelines de integración continua con GitHub Actions.
3. Se desallollaran habilidades para garantizar la reproducibilidad y portabilidad de aplicaciones a través de contenedores.
4. Se evaluarán las ventajas de la integracion continua en la automatizacion del ciclo de vida de aplicaciones.

## ENUNCIADO

Crear y desplegar una aplicacion utilizando FAST API, contenerizada con Docker y configurada con un pipeline de integración continua en GitHub Actions.

### Requisitos

1. Tener conocimientos básicos de Python y FastAPI.
2. contenerizar la aplicación utilizando Docker, con un archivo Dockerfike que:
   1. Utilice una imagen base oficial de Python.
   2. Instale las dependencias necesarias en el archivo requirements.txt.
   3. Se exponga el puerto 8000.
   4. Se configure el comando necesario para ejecutar la aplicación FastAPI.
3. Crear un pipeline de integracion continua en GitHub Actions que:
   1. Descargue el código del repositorio.
   2. Construya la imagen Docker utilizando el Dockerfile.
   3. Suba la imagen a Docker Hub.
   4. Inluya pruebas automatizadas usando pytest para asegurar que la aplicación funciona correctamente.

### Pasos adicionales

1. Configurar los secretos necesarios de Docker Hub en GitHub para permitir el acceso y la subida de imágenes.
2. Añadir pruebas unitarias con pytest para verificar que la aplicacion funciona correctamente antes de construir la imagen Docker.
3. Documentar el proceso de construcción y despliegue en el README del repositorio.

### Pautas de elaboración

1. Preparación del entorno:
   1. Crear un proyecto en GitHub con  una aplicacion sencilla de FastAPI.
   2. Asegurar de tener configurado Docker en tu máquina local y una cuenta activa en Docker Hub.
2. Creación del Dockerfile:
   1. Crear un archivo `Dockerfile` en la raíz del proyecto con las instrucciones necesarias para contenerizar la aplicación FastAPI.
      1. Imagen base oficial de Python.
      2. Instalar las dependencias desde `requirements.txt`.
      3. Exponer el puerto 8000.
      4. Configurar el comando para ejecutar la aplicación FastAPI.
3. Autmoatizacion del pipeline.
   1. Define un pipeline de CI para construir y desplegar la imagen Docker.
   2. Usa GitHub Actions para definir el flujo de trabajo.
      1. Etapa de build: Construir la imagen Docker.
      2. Etapa de test: Ejecutar pruebas unitarias con pytest.
      3. Etapa de push: Subir la imagen a Docker Hub.
4. Ejecución y Verificacion
   1. Ejecutar el pipeline de CI en GitHub Actions.
   2. Verificar que la imagen se construye correctamente y se sube a Docker Hub.
   3. Probar la aplicación FastAPI en un entorno local o desplegarla en un servicio de contenedores
5. Entrega:
   1. Sube tu proyecto a GitHub, incluyendo el Dockerfile, el pipeline de CI y las pruebas unitarias.
   2. Asegúrate de que el README del repositorio documente claramente el proceso de construcción y despliegue, así como las instrucciones para ejecutar la aplicación.

## RUBRICA

| Criterio | Descripción | Puntuación | Peso %
|----------|-------------|------------|-------
| Creación del Dockerfile | El dockerfile esta bien estructurado y funcional | 2 | 20%
| Configuracion del Pipeline | Pipeline bien definido con etapas claras | 3 | 30%
| Automatizacion de pruebas | Pruebas ejecutadas correctamente dentro del Pipeline | 2 | 20%
| Subida y despliegue del contenedor | Imagen subida y funcional en Docker Hub | 2 | 20%
| Documentación | README claro y completo con instrucciones de uso | 1 | 10%


### Notas adicionales.

- Apliacion creada con FastAPI y contenerizada con Docker.
- Tiene que estar disponible el dockerfile porque se evaluará la correcta contenerización de la aplicación.
- El pipeline debe estar disponible (fichero .yml) y debe contener las etapas de construcción, pruebas y despliegue.
- Las pruebas deben estar implementadas con pytest y ejecutarse dentro del pipeline.
- El README debe contener instrucciones claras sobre cómo construir, probar y desplegar la aplicación.