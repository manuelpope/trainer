# Establecer la imagen base con Python y las dependencias de tu proyecto
FROM python:3.9-slim

# Copiar los archivos de tu proyecto al contenedor
COPY . /app

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Instalar las dependencias necesarias
RUN pip install -r req.txt

# Exponer el puerto que utilizará FastAPI (debe coincidir con el puerto configurado en el código FastAPI)
EXPOSE 8000

# Iniciar el Publisher API usando Uvicorn (asegúrate de que el código FastAPI tenga el nombre "main.py")
CMD ["python3", "main.py"]
