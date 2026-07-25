FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

# OLLAMA_HOST debe apuntar a un Ollama accesible desde el contenedor
# (por ejemplo http://host.docker.internal:11434 en local, o la URL de
# un servidor remoto). Este contenedor no incluye Ollama.
ENV OLLAMA_HOST=http://host.docker.internal:11434
ENV OLLAMA_MODEL=llama3.1:8b

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
