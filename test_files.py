#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar arquivos Excel específicos
"""

import requests
import os

def test_excel_file(file_path):
    """Testa um arquivo Excel específico"""
    
    if not os.path.exists(file_path):
        print(f"❌ Arquivo não encontrado: {file_path}")
        return
    
    print(f"\n🔍 TESTANDO ARQUIVO: {file_path}")
    print("=" * 60)
    
    try:
        with open(file_path, 'rb') as f:
            files = {'excel_file': f}
            response = requests.post('http://localhost:8080/upload', files=files)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Status: {result.get('success', 'N/A')}")
            print(f"📊 REFs Processadas: {result.get('total_refs', 0)}")
            print(f"🖼️  Imagens Encontradas: {result.get('images_found', 0)}")
            print(f"✅ Uploads Bem-sucedidos: {result.get('uploads_successful', 0)}")
            print(f"❌ Uploads Falharam: {result.get('uploads_failed', 0)}")
            
            if result.get('errors'):
                print(f"⚠️  Erros: {result['errors']}")
            
            if result.get('images'):
                print(f"🖼️  Imagens processadas: {len(result['images'])}")
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            print(f"Resposta: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro ao testar arquivo: {e}")

if __name__ == "__main__":
    # Lista de arquivos para testar
    test_files = [
        "fabrica_com_imagens.xlsx",
        "nova.xlsx",
        "produto.xlsx"
    ]
    
    for file_path in test_files:
        test_excel_file(file_path)

