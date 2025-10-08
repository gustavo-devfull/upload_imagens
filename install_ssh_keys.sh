#!/bin/bash
# Script de instalação para PythonAnywhere - Sistema SSH com Chaves

echo "🚀 Instalando Sistema SSH com Chaves no PythonAnywhere..."

# Instala dependências
echo "📦 Instalando dependências..."
pip3.10 install --user flask openpyxl paramiko

# Cria diretório do projeto
echo "📁 Criando diretório do projeto..."
mkdir -p ~/sistema_upload_excel
cd ~/sistema_upload_excel

# Cria diretório .ssh se não existir
echo "🔑 Configurando diretório SSH..."
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Baixa arquivos do sistema
echo "⬇️ Baixando arquivos do sistema..."

# Sistema SSH com Chaves
wget -O sistema_ssh_keys.py "https://raw.githubusercontent.com/gustavo-devfull/upload_imagens/main/sistema_ssh_keys.py"

# WSGI
wget -O wsgi.py "https://raw.githubusercontent.com/gustavo-devfull/upload_imagens/main/wsgi.py"

# Script de geração de chave
wget -O gerar_chave_ssh.sh "https://raw.githubusercontent.com/gustavo-devfull/upload_imagens/main/gerar_chave_ssh.sh"

echo "✅ Instalação concluída!"
echo ""
echo "📋 Próximos passos:"
echo "1. Gere uma chave SSH:"
echo "   bash gerar_chave_ssh.sh"
echo ""
echo "2. Adicione a chave pública ao servidor SSH"
echo ""
echo "3. Configure o web app no PythonAnywhere"
echo "4. Defina o arquivo WSGI como: wsgi.py"
echo "5. Reload o web app"
echo "6. Acesse: https://moribrasil.pythonanywhere.com/"
echo ""
echo "🔧 Configuração SSH:"
echo "   Host: 46.202.90.62"
echo "   Porta: 65002"
echo "   Usuário: u715606397"
echo "   Chave: ~/.ssh/id_ed25519"
echo ""
echo "🔧 Para testar conectividade SSH:"
echo "   python3 sistema_ssh_keys.py"
