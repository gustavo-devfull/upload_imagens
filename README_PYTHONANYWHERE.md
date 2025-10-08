# Sistema de Upload de Imagens Excel - PythonAnywhere
# Configuração para deploy no PythonAnywhere

# Arquivo principal: sistema_pythonanywhere.py
# Variável WSGI: app

# Dependências necessárias:
# - Flask
# - openpyxl
# - ftplib (built-in)

# Configurações específicas PythonAnywhere:
# - Usa /tmp para arquivos temporários
# - Não precisa de main() - PythonAnywhere gerencia o servidor
# - Variável 'app' é exportada para WSGI
# - Logs são enviados para console do PythonAnywhere

# Deploy:
# 1. Upload sistema_pythonanywhere.py para PythonAnywhere
# 2. Configurar WSGI para usar a variável 'app'
# 3. Instalar dependências via pip3.10 install flask openpyxl
# 4. Configurar domínio personalizado (opcional)
