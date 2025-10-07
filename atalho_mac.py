#!/usr/bin/env python3
"""
🚀 Sistema de Upload de Imagens Excel - Atalho para Mac
Criado para facilitar o acesso ao sistema local
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def print_banner():
    print("🎉" + "="*60 + "🎉")
    print("🚀 SISTEMA DE UPLOAD DE IMAGENS EXCEL")
    print("📱 Atalho para Mac - Versão 1.0")
    print("🎉" + "="*60 + "🎉")
    print()

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    print("🔍 Verificando dependências...")
    
    try:
        import flask
        import openpyxl
        import PIL
        print("✅ Todas as dependências estão instaladas")
        return True
    except ImportError as e:
        print(f"❌ Dependência faltando: {e}")
        print("📦 Instalando dependências...")
        
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                         check=True, capture_output=True)
            print("✅ Dependências instaladas com sucesso")
            return True
        except subprocess.CalledProcessError:
            print("❌ Erro ao instalar dependências")
            return False

def start_server():
    """Inicia o servidor Flask"""
    print("🚀 Iniciando servidor Flask...")
    
    # Verifica se o servidor já está rodando
    try:
        import requests
        response = requests.get("http://localhost:8080/health", timeout=2)
        if response.status_code == 200:
            print("✅ Servidor já está rodando!")
            return True
    except:
        pass
    
    # Inicia o servidor em background
    try:
        # Usa o script server.py existente
        server_process = subprocess.Popen([sys.executable, "server.py"], 
                                       stdout=subprocess.PIPE, 
                                       stderr=subprocess.PIPE)
        
        # Aguarda o servidor inicializar
        print("⏳ Aguardando servidor inicializar...")
        time.sleep(3)
        
        # Verifica se o servidor está funcionando
        try:
            import requests
            response = requests.get("http://localhost:8080/health", timeout=5)
            if response.status_code == 200:
                print("✅ Servidor iniciado com sucesso!")
                return True
        except:
            print("❌ Erro ao iniciar servidor")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        return False

def open_browser():
    """Abre o navegador com o sistema"""
    print("🌐 Abrindo navegador...")
    
    try:
        webbrowser.open("http://localhost:8080")
        print("✅ Navegador aberto com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao abrir navegador: {e}")
        return False

def show_instructions():
    """Mostra instruções de uso"""
    print("\n" + "="*60)
    print("📋 INSTRUÇÕES DE USO:")
    print("="*60)
    print("1. 🌐 Acesse: http://localhost:8080")
    print("2. 📁 Arraste seu arquivo Excel (.xlsx) para a área de upload")
    print("3. 🚀 Clique em 'Fazer Upload'")
    print("4. ⏳ Acompanhe o progresso")
    print("5. 📋 Copie as URLs das imagens processadas")
    print()
    print("💡 As imagens serão salvas em:")
    print("   https://ideolog.ia.br/images/products/")
    print()
    print("🔧 APIs Disponíveis:")
    print("   • Frontend: http://localhost:8080")
    print("   • Upload: http://localhost:8080/upload")
    print("   • Health: http://localhost:8080/health")
    print("   • Config: http://localhost:8080/config")
    print("="*60)

def main():
    """Função principal"""
    print_banner()
    
    # Verifica se estamos no diretório correto
    if not os.path.exists("server.py"):
        print("❌ Arquivo server.py não encontrado!")
        print("📁 Certifique-se de estar no diretório correto")
        return
    
    # Verifica dependências
    if not check_dependencies():
        print("❌ Não foi possível instalar as dependências")
        return
    
    # Inicia o servidor
    if not start_server():
        print("❌ Não foi possível iniciar o servidor")
        return
    
    # Abre o navegador
    if not open_browser():
        print("⚠️  Navegador não foi aberto automaticamente")
        print("🌐 Acesse manualmente: http://localhost:8080")
    
    # Mostra instruções
    show_instructions()
    
    print("\n🎊 Sistema iniciado com sucesso!")
    print("💡 Para parar o servidor, pressione Ctrl+C")
    
    # Mantém o script rodando
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Sistema encerrado. Até logo!")

if __name__ == "__main__":
    main()

