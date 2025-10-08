#!/bin/bash
# Script de instalação para PythonAnywhere
# Execute este script no console do PythonAnywhere

echo "🚀 Instalando Sistema Upload Excel no PythonAnywhere..."

# Instala dependências
echo "📦 Instalando dependências..."
pip3.10 install --user flask openpyxl

# Cria diretório do projeto
echo "📁 Criando diretório do projeto..."
mkdir -p ~/sistema_upload_excel
cd ~/sistema_upload_excel

# Baixa arquivos do GitHub (substitua pelo seu repositório)
echo "⬇️ Baixando arquivos do GitHub..."
wget https://raw.githubusercontent.com/gustavo-devfull/upload_imagens/main/sistema_pythonanywhere.py
wget https://raw.githubusercontent.com/gustavo-devfull/upload_imagens/main/wsgi.py

# Configura permissões
echo "🔧 Configurando permissões..."
chmod +x wsgi.py

echo "✅ Instalação concluída!"
echo ""
echo "📋 Próximos passos:"
echo "1. Acesse o dashboard do PythonAnywhere"
echo "2. Vá em 'Web' > 'Add a new web app'"
echo "3. Escolha 'Manual configuration'"
echo "4. Configure o WSGI file: /home/seu_usuario/sistema_upload_excel/wsgi.py"
echo "5. Configure o Source code: /home/seu_usuario/sistema_upload_excel"
echo "6. Salve e acesse seu domínio PythonAnywhere"
echo ""
echo "🌐 URLs do sistema:"
echo "- Frontend: https://seu_usuario.pythonanywhere.com/"
echo "- Health Check: https://seu_usuario.pythonanywhere.com/health"
echo "- Upload API: https://seu_usuario.pythonanywhere.com/upload"
