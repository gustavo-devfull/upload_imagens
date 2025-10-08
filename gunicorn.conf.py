# Configuração Gunicorn para Render
bind = "0.0.0.0:8080"
workers = 1
timeout = 120
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True
accesslog = "-"
errorlog = "-"
loglevel = "info"
