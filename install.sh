#!/bin/bash
# Script de instalação e configuração do sistema

echo "🚀 Instalando Sistema de Extração de Imagens Excel → FTP"
echo "=================================================="

# Verifica se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado!"
    echo "   Instale Python 3 primeiro: https://python.org"
    exit 1
fi

echo "✅ Python 3 encontrado: $(python3 --version)"

# Verifica se pip está disponível
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 não encontrado!"
    echo "   Instale pip primeiro"
    exit 1
fi

echo "✅ pip3 encontrado"

# Instala dependências
echo ""
echo "📦 Instalando dependências..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependências instaladas com sucesso!"
else
    echo "❌ Erro ao instalar dependências"
    exit 1
fi

# Testa conectividade FTP
echo ""
echo "🌐 Testando conectividade com servidor FTP..."
python3 -c "
import ftplib
try:
    ftp = ftplib.FTP('46.202.90.62')
    ftp.login('u715606397.gpreto.space', '8:fRP;*OVPp3Oyc&')
    ftp.quit()
    print('✅ Conexão FTP bem-sucedida!')
except Exception as e:
    print(f'❌ Erro na conexão FTP: {e}')
    exit(1)
"

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO!"
    echo "=================================="
    echo ""
    echo "📋 Como usar:"
    echo "   1. Execute: python3 exemplo_uso.py"
    echo "   2. Digite o caminho para seu arquivo Excel"
    echo "   3. Aguarde o processamento"
    echo ""
    echo "📁 Arquivos criados:"
    echo "   • excel_image_extractor.py  - Sistema principal"
    echo "   • exemplo_uso.py            - Interface amigável"
    echo "   • process_excel.py          - Script simplificado"
    echo "   • requirements.txt          - Dependências"
    echo "   • README.md                 - Documentação"
    echo ""
    echo "🌐 Suas imagens estarão disponíveis em:"
    echo "   http://46.202.90.62/"
    echo ""
    echo "❓ Precisa de ajuda? Execute:"
    echo "   python3 exemplo_uso.py --help"
else
    echo ""
    echo "⚠️  Instalação concluída, mas há problemas de conectividade FTP"
    echo "   Verifique sua conexão com a internet"
fi

