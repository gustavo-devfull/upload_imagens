#!/bin/bash
# 🚀 Script de Inicialização - Sistema Flask Seguindo Orientações FTP

echo "🚀 INICIANDO SISTEMA FLASK COM ORIENTAÇÕES FTP INICIAIS"
echo "=================================================="

# Verificar se está no diretório correto
if [ ! -f "sistema_flask_orientacoes_ftp.py" ]; then
    echo "❌ Arquivo sistema_flask_orientacoes_ftp.py não encontrado!"
    echo "   Execute este script no diretório correto."
    exit 1
fi

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Verificar dependências
echo "🔍 Verificando dependências..."
python -c "import flask, ftplib, openpyxl" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Dependências não encontradas!"
    echo "   Execute: pip install flask openpyxl"
    exit 1
fi

# Verificar detector integrado
echo "🔍 Verificando detector integrado..."
python -c "from detector_integrado import DetectorImagensIntegrado" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️ Detector integrado não encontrado!"
    echo "   Certifique-se de que detector_integrado.py existe."
fi

echo "✅ Dependências verificadas!"

# Mostrar configuração
echo ""
echo "📋 CONFIGURAÇÃO ATUAL:"
echo "   • Servidor FTP: 46.202.90.62"
echo "   • Usuário: u715606397.ideolog.ia.br"
echo "   • Diretório: public_html/images/products/"
echo "   • URLs: https://ideolog.ia.br/images/products/"
echo "   • Coluna REF: A | Coluna PHOTO: H | Linha inicial: 4"
echo ""

# Iniciar servidor
echo "🚀 Iniciando servidor Flask..."
echo "   Acesse: http://localhost:8087"
echo "   Pressione Ctrl+C para parar"
echo ""

python sistema_flask_orientacoes_ftp.py

