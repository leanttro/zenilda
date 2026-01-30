FROM python:3.9-slim

# Define diretório de trabalho
WORKDIR /app

# Variáveis de ambiente para evitar arquivos .pyc e buffer de log
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copia e instala requisitos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Expõe a porta 80
EXPOSE 80

# Comando para rodar com Gunicorn (Produção)
CMD ["gunicorn", "--bind", "0.0.0.0:80", "main:app"]