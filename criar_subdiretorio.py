#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar sistema em subdiretório no servidor FTP
"""

import ftplib
import os

def create_system_in_subdirectory():
    """Cria o sistema em um subdiretório específico"""
    
    print("🚀 CRIANDO SISTEMA EM SUBDIRETÓRIO")
    print("=" * 40)
    
    # Configurações FTP
    FTP_HOST = "46.202.90.62"
    FTP_USER = "u715606397.ideolog.ia.br"
    FTP_PASSWORD = "]X9CC>t~ihWhdzNq"
    SUBDIRECTORY = "excel-upload"
    
    # Arquivos para upload
    files_to_upload = [
        'index.html',
        'upload.php', 
        'config.php'
    ]
    
    print(f"🌐 Servidor: {FTP_HOST}")
    print(f"👤 Usuário: {FTP_USER}")
    print(f"📁 Subdiretório: {SUBDIRECTORY}/")
    print()
    
    try:
        # Conecta ao FTP
        print("🔄 Conectando ao servidor FTP...")
        with ftplib.FTP(timeout=60) as ftp:
            ftp.connect(FTP_HOST, 21)
            ftp.login(FTP_USER, FTP_PASSWORD)
            print("✅ Conectado com sucesso!")
            
            # Navega para public_html
            print("🔄 Navegando para public_html...")
            ftp.cwd('public_html')
            
            # Cria subdiretório
            print(f"🔄 Criando subdiretório {SUBDIRECTORY}...")
            try:
                ftp.cwd(SUBDIRECTORY)
                print(f"✅ Subdiretório {SUBDIRECTORY} já existe")
            except:
                ftp.mkd(SUBDIRECTORY)
                ftp.cwd(SUBDIRECTORY)
                print(f"✅ Subdiretório {SUBDIRECTORY} criado")
            
            # Faz upload dos arquivos
            print(f"\n📤 Fazendo upload dos arquivos para {SUBDIRECTORY}/...")
            uploaded_files = []
            
            for filename in files_to_upload:
                if os.path.exists(filename):
                    print(f"🔄 Enviando {filename}...")
                    
                    with open(filename, 'rb') as file:
                        ftp.storbinary(f'STOR {filename}', file)
                    
                    uploaded_files.append(filename)
                    print(f"✅ {filename} enviado com sucesso!")
                else:
                    print(f"❌ Arquivo não encontrado: {filename}")
            
            print(f"\n🎉 Upload concluído!")
            print(f"📊 Arquivos enviados: {len(uploaded_files)}")
            
            # Lista arquivos no subdiretório
            print(f"\n📁 Arquivos em {SUBDIRECTORY}/:")
            files = ftp.nlst()
            for file in files:
                if file in uploaded_files:
                    print(f"   ✅ {file}")
                else:
                    print(f"   📄 {file}")
            
            print(f"\n🌐 Sistema disponível em:")
            print(f"   https://ideolog.ia.br/{SUBDIRECTORY}/")
            print(f"   https://ideolog.ia.br/{SUBDIRECTORY}/index.html")
            
            return True
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_subdirectory_system():
    """Testa o sistema no subdiretório"""
    
    print("\n🧪 TESTANDO SISTEMA NO SUBDIRETÓRIO")
    print("=" * 40)
    
    import urllib.request
    import json
    
    try:
        # Testa o sistema
        print("🔄 Testando sistema...")
        response = urllib.request.urlopen('https://ideolog.ia.br/excel-upload/config.php', timeout=10)
        data = json.loads(response.read().decode())
        
        print("✅ Sistema funcionando!")
        print(f"📊 Versão: {data['config']['version']}")
        print(f"🌐 Domínio: {data['config']['urls']['domain']}")
        
        if data['ftp_test']['success']:
            print("✅ Conexão FTP funcionando")
        else:
            print(f"❌ Problema FTP: {data['ftp_test']['error']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def main():
    """Função principal"""
    
    print("🎨 Sistema de Upload de Imagens Excel")
    print("   Instalação em Subdiretório")
    print("=" * 50)
    
    # Verifica se os arquivos existem
    required_files = ['index.html', 'upload.php', 'config.php']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ Arquivos não encontrados: {', '.join(missing_files)}")
        return
    
    print("✅ Todos os arquivos encontrados")
    
    # Cria sistema no subdiretório
    if create_system_in_subdirectory():
        print("\n🎉 Sistema criado com sucesso!")
        
        # Testa o sistema
        print("\n🧪 Testando sistema...")
        test_subdirectory_system()
        
        print("\n📋 URLs do Sistema:")
        print("1. Interface Principal: https://ideolog.ia.br/excel-upload/")
        print("2. Upload API: https://ideolog.ia.br/excel-upload/upload.php")
        print("3. Configurações: https://ideolog.ia.br/excel-upload/config.php")
        
    else:
        print("\n❌ Falha na criação do sistema!")

if __name__ == "__main__":
    main()

