#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar conectividade FTP e estrutura de diretórios
"""

import ftplib

def testar_ftp():
    """Testa conectividade FTP e estrutura de diretórios"""
    
    print("🔍 TESTE DE CONECTIVIDADE FTP")
    print("=" * 35)
    
    # Configurações FTP
    FTP_HOST = "46.202.90.62"
    FTP_USER = "u715606397.ideolog.ia.br"
    FTP_PASSWORD = "]X9CC>t~ihWhdzNq"
    
    print(f"🌐 Servidor: {FTP_HOST}")
    print(f"👤 Usuário: {FTP_USER}")
    print(f"🔑 Senha: {'*' * len(FTP_PASSWORD)}")
    print()
    
    try:
        print("🔄 Tentando conectar...")
        
        # Testa conexão FTP
        with ftplib.FTP(timeout=60) as ftp:
            ftp.connect(FTP_HOST, 21)
            print("✅ Conectado ao servidor FTP")
            
            print("🔄 Fazendo login...")
            ftp.login(FTP_USER, FTP_PASSWORD)
            print("✅ Login realizado com sucesso!")
            
            print("🔄 Listando diretórios na raiz...")
            files = ftp.nlst()
            print(f"✅ Encontrados {len(files)} itens no diretório raiz:")
            for file in files:
                print(f"   - {file}")
            
            # Verifica se public_html existe
            if 'public_html' in files:
                print("\n✅ Diretório 'public_html' encontrado!")
                
                print("🔄 Listando conteúdo de public_html...")
                ftp.cwd('public_html')
                public_files = ftp.nlst()
                print(f"✅ Encontrados {len(public_files)} itens em public_html:")
                for file in public_files:
                    print(f"   - {file}")
                
                # Volta para raiz
                ftp.cwd('/')
                
                # Tenta criar diretórios
                print("\n🔧 Testando criação de diretórios...")
                try:
                    ftp.mkd('public_html/images')
                    print("✅ Diretório 'public_html/images' criado")
                except Exception as e:
                    print(f"⚠️  Erro ao criar 'public_html/images': {e}")
                
                try:
                    ftp.cwd('public_html/images')
                    ftp.mkd('products')
                    print("✅ Diretório 'public_html/images/products' criado")
                except Exception as e:
                    print(f"⚠️  Erro ao criar 'public_html/images/products': {e}")
                
                # Volta para raiz
                ftp.cwd('/')
                
                # Verifica se consegue navegar
                print("\n🧪 Testando navegação...")
                try:
                    ftp.cwd('public_html/images/products')
                    print("✅ Conseguiu navegar para 'public_html/images/products'")
                    ftp.cwd('/')
                except Exception as e:
                    print(f"❌ Erro ao navegar: {e}")
                
            else:
                print("\n❌ Diretório 'public_html' não encontrado!")
                print("🔄 Tentando criar diretório 'public_html'...")
                try:
                    ftp.mkd('public_html')
                    print("✅ Diretório 'public_html' criado")
                except Exception as e:
                    print(f"❌ Erro ao criar 'public_html': {e}")
            
            print("\n🎉 Teste de conectividade bem-sucedido!")
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

def testar_upload_simples():
    """Testa upload de um arquivo pequeno"""
    
    print("\n🧪 TESTE DE UPLOAD SIMPLES")
    print("=" * 30)
    
    # Configurações FTP
    FTP_HOST = "46.202.90.62"
    FTP_USER = "u715606397.ideolog.ia.br"
    FTP_PASSWORD = "]X9CC>t~ihWhdzNq"
    
    try:
        # Cria arquivo de teste
        test_content = b"Teste de upload FTP - Sistema de imagens"
        test_filename = "teste_upload.txt"
        
        with open(test_filename, 'wb') as f:
            f.write(test_content)
        
        print(f"📁 Arquivo de teste criado: {test_filename}")
        
        # Faz upload
        with ftplib.FTP(timeout=60) as ftp:
            ftp.connect(FTP_HOST, 21)
            ftp.login(FTP_USER, FTP_PASSWORD)
            
            # Cria diretórios
            try:
                ftp.mkd('public_html')
            except:
                pass
            
            try:
                ftp.cwd('public_html')
                ftp.mkd('images')
            except:
                pass
            
            try:
                ftp.cwd('images')
                ftp.mkd('products')
            except:
                pass
            
            # Volta para raiz e faz upload
            ftp.cwd('/')
            with open(test_filename, 'rb') as f:
                ftp.storbinary(f'STOR public_html/images/products/{test_filename}', f)
            
            print("✅ Upload realizado com sucesso!")
            
            # Remove arquivo de teste do servidor
            try:
                ftp.delete(f'public_html/images/products/{test_filename}')
                print("✅ Arquivo de teste removido do servidor")
            except:
                print("⚠️  Não foi possível remover arquivo de teste do servidor")
        
        # Remove arquivo local
        import os
        os.remove(test_filename)
        print("✅ Arquivo de teste local removido")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de upload: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Teste de Conectividade FTP")
    print("   Sistema de Extração de Imagens")
    print()
    
    # Testa conectividade
    conectividade_ok = testar_ftp()
    
    if conectividade_ok:
        # Testa upload
        upload_ok = testar_upload_simples()
        
        if upload_ok:
            print("\n🎉 Todos os testes passaram!")
            print("   O sistema FTP está funcionando corretamente.")
        else:
            print("\n⚠️  Conectividade OK, mas upload falhou.")
    else:
        print("\n❌ Problemas de conectividade detectados.")
        print("   Verifique as credenciais e conectividade de rede.")
    
    print("\n" + "="*50)

