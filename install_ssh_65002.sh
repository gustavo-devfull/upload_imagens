#!/bin/bash
# Script de instalação para PythonAnywhere - Sistema SSH Porta 65002

echo "🚀 Instalando Sistema SSH Porta 65002 no PythonAnywhere..."

# Instala dependências
echo "📦 Instalando dependências..."
pip3.10 install --user flask openpyxl paramiko

# Cria diretório do projeto
echo "📁 Criando diretório do projeto..."
mkdir -p ~/sistema_upload_excel
cd ~/sistema_upload_excel

# Baixa arquivos do sistema
echo "⬇️ Baixando arquivos do sistema..."

# Sistema SSH Porta 65002
wget -O sistema_ssh_65002.py "https://raw.githubusercontent.com/gustavo-devfull/upload_imagens/main/sistema_ssh_65002.py"

# WSGI
wget -O wsgi.py "https://raw.githubusercontent.com/gustavo-devfull/upload_imagens/main/wsgi.py"

echo "✅ Instalação concluída!"
echo ""
echo "📋 Próximos passos:"
echo "1. Configure o web app no PythonAnywhere"
echo "2. Defina o arquivo WSGI como: wsgi.py"
echo "3. Reload o web app"
echo "4. Acesse: https://moribrasil.pythonanywhere.com/"
echo ""
echo "🔧 Configuração SSH:"
echo "   Host: 46.202.90.62"
echo "   Porta: 65002"
echo "   Usuário: u715606397"
echo ""
echo "🔧 Para testar conectividade SSH:"
echo "   python3 sistema_ssh_65002.py"
