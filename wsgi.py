#!/usr/bin/env python3
"""
WSGI Configuration para PythonAnywhere
Arquivo de configuração WSGI para deploy no PythonAnywhere
"""

import sys
import os

# Adiciona o diretório do projeto ao path
path = '/home/seu_usuario/sistema_upload_excel'
if path not in sys.path:
    sys.path.append(path)

# Importa a aplicação Flask
from sistema_pythonanywhere import app

# Configuração para PythonAnywhere
if __name__ == "__main__":
    app.run()