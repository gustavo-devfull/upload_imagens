# Configuração Gunicorn para Render
# O Render usa porta 10000 internamente e faz proxy para 8080
bind = "0.0.0.0:10000"
workers = 1
timeout = 120
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True
accesslog = "-"
errorlog = "-"
loglevel = "info"
