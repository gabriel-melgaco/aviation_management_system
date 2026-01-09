FROM python:3.11-slim

# Variáveis de ambiente para Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Instalar dependências do sistema
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install gunicorn

# Copiar o projeto
COPY . .

# Coletar arquivos estáticos
RUN python manage.py collectstatic --noinput || true

# Criar usuário não-root
RUN useradd -m -u 1000 django && \
    chown -R django:django /app
USER django

EXPOSE 8000

# Script de inicialização
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "app.wsgi:application"]