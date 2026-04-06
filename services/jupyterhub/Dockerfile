FROM python:3.11-slim

# Устанавливаем Node.js и npm
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs git && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем configurable-http-proxy
RUN npm install -g configurable-http-proxy

# Устанавливаем JupyterHub и JupyterLab
RUN pip install --no-cache-dir \
    jupyterhub \
    jupyterlab \
    notebook

# СОЗДАЕМ ПОЛЬЗОВАТЕЛЯ admin
RUN useradd -m -s /bin/bash admin && \
    echo "admin:admin" | chpasswd

# Создаем директорию для конфига
RUN mkdir -p /etc/jupyterhub

# Копируем конфигурационный файл
COPY jupyterhub_config.py /etc/jupyterhub/jupyterhub_config.py

EXPOSE 8000

CMD ["jupyterhub", "-f", "/etc/jupyterhub/jupyterhub_config.py"]