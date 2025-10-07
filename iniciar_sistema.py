#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para iniciar o servidor Flask com frontend React
"""

import os
import sys
import subprocess
import webbrowser
import time
import threading

def check_dependencies():
    """Verifica se todas as dependências estão instaladas"""
    print("🔍 Verificando dependências...")
    
    try:
        import flask
        print("✅ Flask instalado")
    except ImportError:
        print("❌ Flask não encontrado. Instalando...")
        subprocess.run([sys.executable, "-m", "pip", "install", "flask"])
        print("✅ Flask instalado")
    
    try:
        import openpyxl
        print("✅ openpyxl instalado")
    except ImportError:
        print("❌ openpyxl não encontrado. Instalando...")
        subprocess.run([sys.executable, "-m", "pip", "install", "openpyxl"])
        print("✅ openpyxl instalado")
    
    try:
        import paramiko
        print("✅ paramiko instalado")
    except ImportError:
        print("❌ paramiko não encontrado. Instalando...")
        subprocess.run([sys.executable, "-m", "pip", "install", "paramiko"])
        print("✅ paramiko instalado")

def start_server():
    """Inicia o servidor Flask"""
    print("\n🚀 Iniciando servidor Flask...")
    print("=" * 50)
    
    # Verifica se os arquivos necessários existem
    required_files = ['server.py', 'frontend.html', 'upload_ftp_corrigido.py', 'excel_image_extractor.py']
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Arquivo não encontrado: {file}")
            return False
    
    print("✅ Todos os arquivos necessários encontrados")
    
    # Inicia o servidor
    try:
        subprocess.run([sys.executable, "server.py"])
    except KeyboardInterrupt:
        print("\n⏹️  Servidor interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        return False
    
    return True

def open_browser():
    """Abre o navegador após um delay"""
    time.sleep(2)
    try:
        webbrowser.open('http://localhost:8080')
        print("🌐 Navegador aberto automaticamente")
    except Exception as e:
        print(f"⚠️  Não foi possível abrir o navegador automaticamente: {e}")
        print("💡 Acesse manualmente: http://localhost:8080")

def main():
    """Função principal"""
    print("🎨 Sistema de Upload de Imagens Excel")
    print("   Frontend React + Backend Flask")
    print("=" * 50)
    
    # Verifica dependências
    check_dependencies()
    
    # Pergunta se deve abrir o navegador
    try:
        open_browser_choice = input("\n🌐 Abrir navegador automaticamente? (s/n): ").lower().strip()
        if open_browser_choice in ['s', 'sim', 'y', 'yes']:
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
    except KeyboardInterrupt:
        print("\n⏹️  Operação cancelada")
        return
    
    # Inicia servidor
    start_server()

if __name__ == "__main__":
    main()
