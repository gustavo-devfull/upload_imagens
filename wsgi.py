#!/usr/bin/env python3
import sys
import os

# Adiciona o diretório do projeto ao path
path = '/home/moribrasil/sistema_upload_excel'
if path not in sys.path:
    sys.path.append(path)

# Importa a aplicação Flask
from sistema_fallback import app
application = app