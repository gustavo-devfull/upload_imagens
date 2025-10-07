#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar o sistema PHP online e diagnosticar problemas
"""

import requests
import os
import json

def testar_sistema_php():
    """Testa o sistema PHP online"""
    
    print("🔍 TESTANDO SISTEMA PHP ONLINE")
    print("=" * 50)
    
    # URLs para testar
    urls = [
        "https://ideolog.ia.br/excel-upload/",
        "https://ideolog.ia.br/excel-upload/sistema_completo.php",
        "https://ideolog.ia.br/excel-upload/sistema.html",
        "https://ideolog.ia.br/excel-upload/upload.php",
        "https://ideolog.ia.br/excel-upload/config.php"
    ]
    
    for url in urls:
        print(f"\n🌐 Testando: {url}")
        try:
            response = requests.get(url, timeout=10)
            print(f"   Status: {response.status_code}")
            print(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")
            
            if response.status_code == 200:
                content = response.text[:200]
                if "Sistema de Upload" in content or "Excel" in content:
                    print(f"   ✅ Sistema encontrado!")
                else:
                    print(f"   ⚠️  Conteúdo diferente: {content[:100]}...")
            else:
                print(f"   ❌ Erro HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Erro de conexão: {e}")
    
    # Testa upload de arquivo
    print(f"\n📤 TESTANDO UPLOAD DE ARQUIVO:")
    
    arquivo_teste = "/Users/gustavo/upload/tartaruga.xlsx"
    if os.path.exists(arquivo_teste):
        try:
            with open(arquivo_teste, 'rb') as f:
                files = {'excel_file': f}
                response = requests.post(
                    "https://ideolog.ia.br/excel-upload/upload.php",
                    files=files,
                    timeout=30
                )
            
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:500]}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   ✅ Upload bem-sucedido!")
                    print(f"   📊 Dados: {json.dumps(data, indent=2)}")
                except:
                    print(f"   ⚠️  Resposta não é JSON válido")
            else:
                print(f"   ❌ Erro no upload")
                
        except Exception as e:
            print(f"   ❌ Erro no upload: {e}")
    else:
        print(f"   ❌ Arquivo de teste não encontrado: {arquivo_teste}")

def criar_sistema_php_simples():
    """Cria um sistema PHP mais simples para teste"""
    
    print(f"\n🔧 CRIANDO SISTEMA PHP SIMPLES:")
    
    # Sistema PHP simples
    php_content = '''<?php
// Sistema de Upload Simples
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit(0);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['excel_file'])) {
    $file = $_FILES['excel_file'];
    
    // Verifica se é um arquivo Excel
    if ($file['type'] !== 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') {
        echo json_encode(['error' => 'Apenas arquivos .xlsx são permitidos']);
        exit;
    }
    
    // Simula processamento
    $result = [
        'success' => true,
        'message' => 'Arquivo recebido com sucesso',
        'filename' => $file['name'],
        'size' => $file['size'],
        'type' => $file['type'],
        'uploads_successful' => 1,
        'uploads_failed' => 0,
        'images' => [
            [
                'name' => 'Imagem de teste',
                'url' => 'https://ideolog.ia.br/images/products/teste.jpg'
            ]
        ]
    ];
    
    echo json_encode($result);
} else {
    echo json_encode(['error' => 'Método não permitido ou arquivo não enviado']);
}
?>'''
    
    # Salva o arquivo
    with open('upload_simples.php', 'w') as f:
        f.write(php_content)
    
    print(f"   ✅ Arquivo upload_simples.php criado")
    
    # Testa o arquivo local
    print(f"\n🧪 TESTANDO ARQUIVO LOCAL:")
    try:
        import subprocess
        result = subprocess.run(['php', '-l', 'upload_simples.php'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ Sintaxe PHP válida")
        else:
            print(f"   ❌ Erro de sintaxe: {result.stderr}")
    except Exception as e:
        print(f"   ⚠️  Não foi possível testar sintaxe PHP: {e}")

if __name__ == "__main__":
    testar_sistema_php()
    criar_sistema_php_simples()
