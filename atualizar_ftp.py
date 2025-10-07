#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para atualizar o sistema FTP com configurações atuais
"""

import ftplib
import os
import sys

def update_ftp_system():
    """Atualiza o sistema FTP com configurações atuais"""
    
    print("🔄 ATUALIZANDO SISTEMA FTP")
    print("=" * 30)
    
    # Configurações FTP atualizadas
    FTP_HOST = "46.202.90.62"
    FTP_USER = "u715606397.ideolog.ia.br"
    FTP_PASSWORD = "]X9CC>t~ihWhdzNq"
    
    # Arquivos para atualizar
    files_to_update = [
        'index.html',
        'sistema.html',
        'upload.php', 
        'config.php',
        'index.php'
    ]
    
    print(f"🌐 Servidor: {FTP_HOST}")
    print(f"👤 Usuário: {FTP_USER}")
    print(f"📁 Diretório: public_html/excel-upload/")
    print()
    
    try:
        # Conecta ao FTP
        print("🔄 Conectando ao servidor FTP...")
        with ftplib.FTP(timeout=60) as ftp:
            ftp.connect(FTP_HOST, 21)
            ftp.login(FTP_USER, FTP_PASSWORD)
            print("✅ Conectado com sucesso!")
            
            # Navega para o diretório do sistema
            print("🔄 Navegando para excel-upload...")
            try:
                ftp.cwd('public_html/excel-upload')
                print("✅ Diretório excel-upload encontrado")
            except:
                print("⚠️  Diretório excel-upload não encontrado, criando...")
                ftp.cwd('public_html')
                ftp.mkd('excel-upload')
                ftp.cwd('excel-upload')
                print("✅ Diretório excel-upload criado")
            
            # Atualiza os arquivos
            print("\n📤 Atualizando arquivos...")
            updated_files = []
            
            for filename in files_to_update:
                if os.path.exists(filename):
                    print(f"🔄 Atualizando {filename}...")
                    
                    with open(filename, 'rb') as file:
                        ftp.storbinary(f'STOR {filename}', file)
                    
                    updated_files.append(filename)
                    print(f"✅ {filename} atualizado com sucesso!")
                else:
                    print(f"⚠️  Arquivo não encontrado: {filename}")
            
            print(f"\n🎉 Atualização concluída!")
            print(f"📊 Arquivos atualizados: {len(updated_files)}")
            
            # Lista arquivos no servidor
            print("\n📁 Arquivos no servidor:")
            files = ftp.nlst()
            for file in files:
                if file in updated_files:
                    print(f"   ✅ {file} (atualizado)")
                else:
                    print(f"   📄 {file}")
            
            print(f"\n🌐 Sistema atualizado disponível em:")
            print(f"   https://ideolog.ia.br/excel-upload/sistema.html")
            print(f"   https://ideolog.ia.br/excel-upload/index.html")
            print(f"   https://ideolog.ia.br/excel-upload/")
            
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

def test_updated_system():
    """Testa o sistema atualizado"""
    
    print("\n🧪 TESTANDO SISTEMA ATUALIZADO")
    print("=" * 35)
    
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
    print("   Atualização FTP")
    print("=" * 40)
    
    # Verifica se os arquivos existem
    required_files = ['index.html', 'sistema.html', 'upload.php', 'config.php']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ Arquivos não encontrados: {', '.join(missing_files)}")
        print("💡 Certifique-se de que todos os arquivos estão na pasta atual")
        return
    
    print("✅ Todos os arquivos encontrados")
    print("🔄 Iniciando atualização...")
    
    # Atualiza o sistema
    if update_ftp_system():
        print("\n🎉 Sistema atualizado com sucesso!")
        
        # Testa o sistema
        print("\n🧪 Testando sistema atualizado...")
        test_updated_system()
        
        print("\n📋 URLs do Sistema Atualizado:")
        print("1. Interface Principal: https://ideolog.ia.br/excel-upload/sistema.html")
        print("2. Interface Alternativa: https://ideolog.ia.br/excel-upload/index.html")
        print("3. Upload API: https://ideolog.ia.br/excel-upload/upload.php")
        print("4. Configurações: https://ideolog.ia.br/excel-upload/config.php")
        
        print("\n🎯 Próximos passos:")
        print("1. Acesse: https://ideolog.ia.br/excel-upload/sistema.html")
        print("2. Teste o upload de um arquivo Excel")
        print("3. Verifique se as imagens aparecem em: https://ideolog.ia.br/images/products/")
        
    else:
        print("\n❌ Falha na atualização!")
        print("💡 Verifique as credenciais FTP e conectividade")

if __name__ == "__main__":
    main()


