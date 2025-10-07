#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para fazer upload do sistema para o servidor FTP
"""

import ftplib
import os
import sys

def upload_to_ftp():
    """Faz upload dos arquivos para o servidor FTP"""
    
    print("🚀 UPLOAD DO SISTEMA PARA SERVIDOR FTP")
    print("=" * 45)
    
    # Configurações FTP
    FTP_HOST = "46.202.90.62"
    FTP_USER = "u715606397.ideolog.ia.br"
    FTP_PASSWORD = "]X9CC>t~ihWhdzNq"
    
    # Arquivos para upload
    files_to_upload = [
        'index.html',
        'upload.php', 
        'config.php'
    ]
    
    print(f"🌐 Servidor: {FTP_HOST}")
    print(f"👤 Usuário: {FTP_USER}")
    print(f"📁 Diretório: public_html/")
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
            try:
                ftp.cwd('public_html')
                print("✅ Diretório public_html encontrado")
            except:
                print("⚠️  Diretório public_html não encontrado, criando...")
                ftp.mkd('public_html')
                ftp.cwd('public_html')
                print("✅ Diretório public_html criado")
            
            # Faz upload dos arquivos
            print("\n📤 Fazendo upload dos arquivos...")
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
            
            # Lista arquivos no servidor
            print("\n📁 Arquivos no servidor:")
            files = ftp.nlst()
            for file in files:
                if file in uploaded_files:
                    print(f"   ✅ {file}")
                else:
                    print(f"   📄 {file}")
            
            print(f"\n🌐 Sistema disponível em:")
            print(f"   https://ideolog.ia.br/")
            print(f"   https://ideolog.ia.br/index.html")
            
            return True
            
    except ftplib.error_perm as e:
        print(f"❌ Erro de permissão: {e}")
        return False
    except ftplib.error_temp as e:
        print(f"❌ Erro temporário: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False

def test_system():
    """Testa se o sistema está funcionando"""
    
    print("\n🧪 TESTANDO SISTEMA")
    print("=" * 25)
    
    import urllib.request
    import json
    
    try:
        # Testa health check
        print("🔄 Testando health check...")
        response = urllib.request.urlopen('https://ideolog.ia.br/config.php', timeout=10)
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
    print("   Instalação no Servidor FTP")
    print("=" * 50)
    
    # Verifica se os arquivos existem
    required_files = ['index.html', 'upload.php', 'config.php']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ Arquivos não encontrados: {', '.join(missing_files)}")
        print("💡 Certifique-se de que todos os arquivos estão na pasta atual")
        return
    
    print("✅ Todos os arquivos encontrados")
    
    # Pergunta se deve continuar
    try:
        continue_choice = input("\n🚀 Continuar com o upload? (s/n): ").lower().strip()
        if continue_choice not in ['s', 'sim', 'y', 'yes']:
            print("⏹️  Upload cancelado")
            return
    except KeyboardInterrupt:
        print("\n⏹️  Upload cancelado")
        return
    
    # Faz upload
    if upload_to_ftp():
        print("\n🎉 Upload concluído com sucesso!")
        
        # Pergunta se deve testar
        try:
            test_choice = input("\n🧪 Testar sistema? (s/n): ").lower().strip()
            if test_choice in ['s', 'sim', 'y', 'yes']:
                test_system()
        except KeyboardInterrupt:
            pass
        
        print("\n📋 Próximos passos:")
        print("1. Acesse: https://ideolog.ia.br/")
        print("2. Teste o upload de um arquivo Excel")
        print("3. Verifique se as imagens aparecem em: https://ideolog.ia.br/images/products/")
        
    else:
        print("\n❌ Upload falhou!")
        print("💡 Verifique as credenciais FTP e conectividade")

if __name__ == "__main__":
    main()

