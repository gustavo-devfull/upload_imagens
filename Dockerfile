# Dockerfile para Sistema de Upload de Imagens Excel
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Instala dependências do sistema necessárias para Pillow e openpyxl
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia arquivos de requisitos
COPY requirements.txt .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos do projeto
COPY . .

# Expõe a porta (padrão 8080, mas pode ser sobrescrita por PORT)
EXPOSE 8080

# Variáveis de ambiente padrão (podem ser sobrescritas)
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Comando para iniciar o servidor
CMD ["python", "sistema_simples.py"]

