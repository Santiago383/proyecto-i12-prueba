FROM python:3.12-slim

WORKDIR /app

# Copiamos requirements.txt y lo instalamos
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el código (aunque la carpeta ya está montada, esto ayuda en builds)
COPY . .

# Exponemos el puerto que usa Flask
EXPOSE 5000

# Comando por defecto
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--reload"]
