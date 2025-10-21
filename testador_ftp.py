#!/usr/bin/env python3
"""
🔧 TESTADOR FTP - Verificar conexão e configuração
"""

import ftplib
import os

def testar_conexao_ftp():
    """Testa conexão FTP com as credenciais do projeto"""
    
    # Configurações FTP seguindo orientações iniciais
    FTP_HOST = "46.202.90.62"
    FTP_USER = "u715606397.ideolog.ia.br"
    FTP_PASS = "]X9CC>t~ihWhdzNq"
    
    print("🔧 TESTADOR FTP - VERIFICANDO CONEXÃO")
    print("=" * 50)
    print(f"🌐 Host: {FTP_HOST}")
    print(f"👤 Usuário: {FTP_USER}")
    print(f"🔒 Senha: {'*' * len(FTP_PASS)}")
    print("=" * 50)
    
    try:
        # Conectar
        print("🔗 Conectando ao FTP...")
        ftp = ftplib.FTP()
        ftp.connect(FTP_HOST, 21)
        ftp.login(FTP_USER, FTP_PASS)
        
        print("✅ Conexão FTP bem-sucedida!")
        
        # Listar diretório atual
        print("\n📁 Diretório atual:")
        files = ftp.nlst()
        for file in files[:10]:  # Mostrar apenas os primeiros 10
            print(f"   • {file}")
        if len(files) > 10:
            print(f"   ... e mais {len(files) - 10} arquivos")
        
        # Verificar/criar estrutura de diretórios
        print("\n📁 Verificando estrutura de diretórios...")
        
        # Criar public_html se não existir
        try:
            ftp.mkd('public_html')
            print("   ✅ Diretório 'public_html' criado")
        except:
            print("   ℹ️ Diretório 'public_html' já existe")
        
        # Criar images dentro de public_html
        try:
            ftp.cwd('public_html')
            ftp.mkd('images')
            print("   ✅ Diretório 'images' criado")
        except:
            print("   ℹ️ Diretório 'images' já existe")
        
        # Criar products dentro de images
        try:
            ftp.cwd('images')
            ftp.mkd('products')
            print("   ✅ Diretório 'products' criado")
        except:
            print("   ℹ️ Diretório 'products' já existe")
        
        # Volta para raiz
        ftp.cwd('/')
        
        # Testar upload
        print("\n📤 Testando upload...")
        test_content = b"Teste de conexao FTP - Sistema Flask"
        test_filename = "teste_conexao_flask.txt"
        
        try:
            # Criar arquivo temporário
            temp_path = f"/tmp/{test_filename}"
            with open(temp_path, 'wb') as f:
                f.write(test_content)
            
            # Fazer upload
            remote_path = f"public_html/images/products/{test_filename}"
            with open(temp_path, 'rb') as f:
                ftp.storbinary(f'STOR {remote_path}', f)
            
            # Remover arquivo temporário
            os.remove(temp_path)
            
            print(f"   ✅ Upload de teste bem-sucedido!")
            print(f"   📁 Arquivo: {remote_path}")
            
            # Verificar se foi criado
            ftp.cwd('public_html/images/products')
            files_after = ftp.nlst()
            if test_filename in files_after:
                print(f"   ✅ Arquivo confirmado no servidor!")
                
                # Remover arquivo de teste
                ftp.delete(test_filename)
                print(f"   🗑️ Arquivo de teste removido")
            else:
                print(f"   ❌ Arquivo não encontrado no servidor!")
            
        except Exception as e:
            print(f"   ❌ Erro no upload de teste: {e}")
        
        ftp.quit()
        print("\n🎉 TESTE CONCLUÍDO COM SUCESSO!")
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão FTP: {e}")
        print("\n💡 Possíveis soluções:")
        print("   • Verifique se o servidor FTP está online")
        print("   • Confirme as credenciais")
        print("   • Verifique firewall/proxy")
        return False

if __name__ == "__main__":
    testar_conexao_ftp()

