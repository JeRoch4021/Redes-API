# Imagen base
FROM python:3.12.10-slim-bookworm

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia todos los archivos y carpetas desde esta carpeta (servidor_HTTP/) al contenedor
COPY . .

# Archivo para instalar las dependecias
RUN pip install -r requirements-dev.txt

# La app usa este puerto
EXPOSE 8000

# Comando para ejecutar FastAPI
ENTRYPOINT [ "uvicorn", "--host", "0.0.0.0", "main:app", "--reload", "--port", "8000" ]