import os

# Получаем значения из переменных окружения (или используем значения по умолчанию)
ADMIN_USER = os.environ.get('JUPYTERHUB_ADMIN_USER', 'admin')
ADMIN_PASSWORD = os.environ.get('JUPYTERHUB_ADMIN_PASSWORD', 'admin')

# Настройки прокси
c.JupyterHub.proxy_class = 'jupyterhub.proxy.ConfigurableHTTPProxy'

# Простые фиксированные секреты (для локальной разработки)
c.JupyterHub.cookie_secret = b'my-super-secret-cookie-key-for-dev-only'
c.ConfigurableHTTPProxy.auth_token = 'my-super-secret-proxy-token-for-dev-only'

# Используем простую аутентификацию (DummyAuthenticator - любой пароль)
c.JupyterHub.authenticator_class = 'jupyterhub.auth.DummyAuthenticator'
c.DummyAuthenticator.password = ADMIN_PASSWORD

# Настройки спавнера (запуск пользовательских серверов)
c.JupyterHub.spawner_class = 'jupyterhub.spawner.LocalProcessSpawner'
c.LocalProcessSpawner.default_url = '/lab'  # Открываем сразу JupyterLab

# Настройки пользователей - только админ
c.Authenticator.admin_users = {ADMIN_USER}
c.Authenticator.allowed_users = {ADMIN_USER}

# База данных - SQLite в памяти (для простоты)
c.JupyterHub.db_url = 'sqlite:///jupyterhub.sqlite'

# Настройки сервера
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 8000
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_port = 8081

print(f"JupyterHub configured with admin user: {ADMIN_USER}")
print("Using simplified configuration for development")