#!/bin/bash
# 🚀 Script para iniciar o Sistema Local Melhorado
# Versão simplificada para Mac/Linux

echo "🎉============================================================🎉"
echo "🚀 SISTEMA LOCAL MELHORADO - Upload Excel"
echo "📱 Versão 2.0 com Detecção Avançada"
echo "🎉============================================================🎉"
echo

# Verifica se estamos no diretório correto
if [ ! -f "sistema_local_melhorado.py" ]; then
    echo "❌ Arquivo sistema_local_melhorado.py não encontrado!"
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
if ! python3 -c "import openpyxl" 2>/dev/null; then
    echo "📦 Instalando openpyxl..."
    python3 -m pip install openpyxl
fi

echo "✅ Dependências verificadas"

# Verifica se o servidor já está rodando
if curl -s http://localhost:8080/health >/dev/null 2>&1; then
    echo "✅ Servidor já está rodando!"
    echo "🌐 Abrindo navegador..."
    open "http://localhost:8080" 2>/dev/null || xdg-open "http://localhost:8080" 2>/dev/null
else
    echo "🚀 Iniciando Sistema Local Melhorado..."
    echo
    echo "📋 INSTRUÇÕES:"
    echo "1. 🌐 Acesse: http://localhost:8080"
    echo "2. 📁 Use um dos arquivos recomendados:"
    echo "   • fabrica_com_imagens.xlsx (4 imagens)"
    echo "   • tartaruga.xlsx (1 imagem)"
    echo "   • carrinho.xlsx (2 imagens)"
    echo "3. 🚀 Faça upload e veja a detecção melhorada!"
    echo
    echo "⏳ Iniciando servidor..."
    python3 sistema_local_melhorado.py
fi

