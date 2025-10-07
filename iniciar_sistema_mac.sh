#!/bin/bash
# 🚀 Sistema de Upload de Imagens Excel - Atalho para Mac
# Script simples para iniciar o sistema

echo "🎉============================================================🎉"
echo "🚀 SISTEMA DE UPLOAD DE IMAGENS EXCEL"
echo "📱 Atalho para Mac - Versão 1.0"
echo "🎉============================================================🎉"
echo

# Verifica se estamos no diretório correto
if [ ! -f "server.py" ]; then
    echo "❌ Arquivo server.py não encontrado!"
    echo "📁 Certifique-se de estar no diretório correto"
    exit 1
fi

# Verifica se o Python está disponível
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado!"
    echo "📦 Instale o Python3 primeiro"
    exit 1
fi

echo "🔍 Verificando dependências..."
if ! python3 -c "import flask, openpyxl, PIL" 2>/dev/null; then
    echo "📦 Instalando dependências..."
    python3 -m pip install -r requirements.txt
fi

echo "✅ Dependências verificadas"

# Verifica se o servidor já está rodando
if curl -s http://localhost:8080/health >/dev/null 2>&1; then
    echo "✅ Servidor já está rodando!"
else
    echo "🚀 Iniciando servidor Flask..."
    python3 server.py &
    SERVER_PID=$!
    
    # Aguarda o servidor inicializar
    echo "⏳ Aguardando servidor inicializar..."
    sleep 3
    
    # Verifica se o servidor está funcionando
    if curl -s http://localhost:8080/health >/dev/null 2>&1; then
        echo "✅ Servidor iniciado com sucesso!"
    else
        echo "❌ Erro ao iniciar servidor"
        exit 1
    fi
fi

echo "🌐 Abrindo navegador..."
open "http://localhost:8080"

echo
echo "============================================================"
echo "📋 INSTRUÇÕES DE USO:"
echo "============================================================"
echo "1. 🌐 Acesse: http://localhost:8080"
echo "2. 📁 Arraste seu arquivo Excel (.xlsx) para a área de upload"
echo "3. 🚀 Clique em 'Fazer Upload'"
echo "4. ⏳ Acompanhe o progresso"
echo "5. 📋 Copie as URLs das imagens processadas"
echo
echo "💡 As imagens serão salvas em:"
echo "   https://ideolog.ia.br/images/products/"
echo
echo "🔧 APIs Disponíveis:"
echo "   • Frontend: http://localhost:8080"
echo "   • Upload: http://localhost:8080/upload"
echo "   • Health: http://localhost:8080/health"
echo "   • Config: http://localhost:8080/config"
echo "============================================================"
echo
echo "🎊 Sistema iniciado com sucesso!"
echo "💡 Para parar o servidor, pressione Ctrl+C"
echo

# Mantém o script rodando
wait

