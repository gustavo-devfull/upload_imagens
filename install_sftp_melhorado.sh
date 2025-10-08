#!/bin/bash
# Script de instalação para PythonAnywhere - Sistema SFTP Melhorado

echo "🚀 Instalando Sistema SFTP Melhorado no PythonAnywhere..."

# Instala dependências
echo "📦 Instalando dependências..."
pip3.10 install --user flask openpyxl paramiko

# Cria diretório do projeto
echo "📁 Criando diretório do projeto..."
mkdir -p ~/sistema_upload_excel
cd ~/sistema_upload_excel

# Baixa arquivos do sistema
echo "⬇️ Baixando arquivos do sistema..."

# Sistema SFTP Melhorado
wget -O sistema_sftp_melhorado.py "https://raw.githubusercontent.com/seu_usuario/sistema_upload_excel/main/sistema_sftp_melhorado.py"

# WSGI
wget -O wsgi.py "https://raw.githubusercontent.com/seu_usuario/sistema_upload_excel/main/wsgi.py"

echo "✅ Instalação concluída!"
echo ""
echo "📋 Próximos passos:"
echo "1. Configure o web app no PythonAnywhere"
echo "2. Defina o arquivo WSGI como: wsgi.py"
echo "3. Reload o web app"
echo "4. Acesse: https://moribrasil.pythonanywhere.com/"
echo ""
echo "🔧 Para testar conectividade SFTP:"
echo "   python3 sistema_sftp_melhorado.py"
