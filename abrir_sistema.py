#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simples para abrir o sistema no navegador
"""

import webbrowser
import time

def main():
    print("🌐 Abrindo Sistema de Upload de Imagens Excel...")
    print("=" * 50)
    
    url = "http://localhost:8080"
    
    print(f"📁 URL: {url}")
    print("⏳ Aguardando 2 segundos...")
    
    time.sleep(2)
    
    try:
        webbrowser.open(url)
        print("✅ Navegador aberto com sucesso!")
        print("\n🎯 Instruções:")
        print("1. Arraste seu arquivo Excel (.xlsx) para a área de upload")
        print("2. Clique em 'Fazer Upload'")
        print("3. Acompanhe o progresso")
        print("4. Copie as URLs das imagens processadas")
        print("\n💡 As imagens serão salvas em: https://ideolog.ia.br/images/products/")
        
    except Exception as e:
        print(f"❌ Erro ao abrir navegador: {e}")
        print(f"💡 Acesse manualmente: {url}")

if __name__ == "__main__":
    main()

