#!/bin/bash
# 🚀 Script para iniciar o Sistema Flask Melhorado
# Versão que funciona sem problemas de upload

echo "🎉============================================================🎉"
echo "🚀 SISTEMA FLASK MELHORADO - Upload Excel"
echo "📱 Versão 2.0 com Detecção Avançada"
echo "🎉============================================================🎉"
echo

# Verifica se estamos no diretório correto
if [ ! -f "sistema_flask_melhorado.py" ]; then
    echo "❌ Arquivo sistema_flask_melhorado.py não encontrado!"
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
if ! python3 -c "import flask, openpyxl" 2>/dev/null; then
    echo "📦 Instalando dependências..."
    python3 -m pip install flask openpyxl
fi

echo "✅ Dependências verificadas"

# Verifica se a porta 8080 está livre
if curl -s http://localhost:8080/health >/dev/null 2>&1; then
    echo "⚠️  Porta 8080 ocupada, usando porta 8081"
    PORT=8081
else
    PORT=8080
fi

echo "🚀 Iniciando Sistema Flask Melhorado na porta $PORT..."
echo
echo "📋 INSTRUÇÕES:"
echo "1. 🌐 Acesse: http://localhost:$PORT"
echo "2. 📁 Use um dos arquivos recomendados:"
echo "   • fabrica_com_imagens.xlsx (4 imagens)"
echo "   • tartaruga.xlsx (1 imagem)"
echo "   • carrinho.xlsx (2 imagens)"
echo "3. 🚀 Faça upload e veja a detecção melhorada!"
echo
echo "⏳ Iniciando servidor..."

# Inicia o servidor Flask
PORT=$PORT python3 sistema_flask_melhorado.py

