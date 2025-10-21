#!/usr/bin/env python3
"""
🔍 TESTE DIRETO FTP - Verificar problema específico
"""

import ftplib
import os

def teste_upload_direto():
    """Teste direto de upload FTP"""
    print("🔍 TESTE DIRETO FTP")
    print("=" * 40)
    
    # Configurações FTP
    FTP_HOST = "46.202.90.62"
    FTP_USER = "u715606397.ideolog.ia.br"
    FTP_PASS = "]X9CC>t~ihWhdzNq"
    
    try:
        # Conectar
        print("🔗 Conectando ao FTP...")
        ftp = ftplib.FTP()
        ftp.connect(FTP_HOST, 21)
        ftp.login(FTP_USER, FTP_PASS)
        print("✅ Conectado!")
        
        # Verificar diretório atual
        print(f"📁 Diretório atual: {ftp.pwd()}")
        
        # Criar arquivo de teste
        test_content = b"Teste de upload direto - Sistema Flask"
        test_filename = "teste_direto.txt"
        
        print(f"📤 Fazendo upload de teste: {test_filename}")
        
        # Método 1: Upload direto para public_html/images/products/
        try:
            remote_path = f"public_html/images/products/{test_filename}"
            print(f"   📁 Caminho: {remote_path}")
            
            # Criar arquivo temporário
            temp_path = f"/tmp/{test_filename}"
            with open(temp_path, 'wb') as f:
                f.write(test_content)
            
            # Upload
            with open(temp_path, 'rb') as f:
                ftp.storbinary(f'STOR {remote_path}', f)
            
            # Remover arquivo temporário
            os.remove(temp_path)
            
            print("   ✅ Upload método 1 bem-sucedido!")
            
        except Exception as e:
            print(f"   ❌ Erro método 1: {e}")
        
        # Verificar se foi criado
        print("🔍 Verificando se arquivo foi criado...")
        try:
            ftp.cwd('public_html/images/products')
            files = ftp.nlst()
            print(f"   📁 Arquivos em public_html/images/products: {len(files)}")
            for file in files:
                if test_filename in file:
                    print(f"   ✅ {file} encontrado!")
                else:
                    print(f"   📄 {file}")
        except Exception as e:
            print(f"   ❌ Erro ao verificar: {e}")
        
        # Método 2: Navegar para diretório e fazer upload
        print(f"\\n📤 Método 2: Navegar para diretório...")
        try:
            ftp.cwd('/')
            ftp.cwd('public_html/images/products')
            print(f"   📁 Diretório atual: {ftp.pwd()}")
            
            # Upload direto no diretório
            with open(f"/tmp/{test_filename}", 'wb') as f:
                f.write(test_content)
            
            with open(f"/tmp/{test_filename}", 'rb') as f:
                ftp.storbinary(f'STOR {test_filename}', f)
            
            os.remove(f"/tmp/{test_filename}")
            print("   ✅ Upload método 2 bem-sucedido!")
            
        except Exception as e:
            print(f"   ❌ Erro método 2: {e}")
        
        # Verificar novamente
        print("🔍 Verificando novamente...")
        files = ftp.nlst()
        print(f"   📁 Arquivos em public_html/images/products: {len(files)}")
        for file in files:
            if test_filename in file:
                print(f"   ✅ {file} encontrado!")
            else:
                print(f"   📄 {file}")
        
        # Limpar arquivos de teste
        print("\\n🗑️ Limpando arquivos de teste...")
        try:
            if test_filename in files:
                ftp.delete(test_filename)
                print(f"   ✅ {test_filename} removido!")
        except Exception as e:
            print(f"   ⚠️ Erro ao remover: {e}")
        
        ftp.quit()
        print("\\n🎉 Teste concluído!")
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    teste_upload_direto()

