#!/bin/bash
# Script para gerar e configurar chaves SSH para PythonAnywhere

echo "🔑 Configurando Chaves SSH para PythonAnywhere..."

# Cria diretório .ssh se não existir
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Gera chave SSH ed25519 (mais segura que RSA)
echo "🔑 Gerando chave SSH ed25519..."
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N "" -C "u715606397@us-imm-web176.main-hosting.eu"

# Define permissões corretas
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub

echo "✅ Chave SSH gerada com sucesso!"
echo ""
echo "📋 Próximos passos:"
echo "1. Copie a chave pública abaixo:"
echo ""
cat ~/.ssh/id_ed25519.pub
echo ""
echo "2. Adicione esta chave ao servidor SSH:"
echo "   - Acesse o painel do seu provedor de hospedagem"
echo "   - Vá em 'SSH Keys' ou 'Chaves SSH'"
echo "   - Cole a chave pública acima"
echo ""
echo "3. Teste a conexão:"
echo "   ssh -i ~/.ssh/id_ed25519 u715606397@46.202.90.62 -p 65002"
echo ""
echo "4. Configure o sistema:"
echo "   python3 sistema_ssh_keys.py"
