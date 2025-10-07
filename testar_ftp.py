#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar conectividade FTP
"""

import ftplib
import time

def testar_conectividade_ftp():
    """Testa conectividade com o servidor FTP"""
    
    print("🔍 TESTE DE CONECTIVIDADE FTP")
    print("=" * 35)
    
    # Configurações FTP
    FTP_HOST = "gpreto.space"
    FTP_USER = "u715606397.nova"
    FTP_PASSWORD = "]X9CC>t~ihWhdzNq"
    
    print(f"🌐 Servidor: {FTP_HOST}")
    print(f"👤 Usuário: {FTP_USER}")
    print(f"🔑 Senha: {'*' * len(FTP_PASSWORD)}")
    print()
    
    try:
        print("🔄 Tentando conectar...")
        start_time = time.time()
        
        # Testa conexão com timeout maior
        with ftplib.FTP(timeout=60) as ftp:
            ftp.connect(FTP_HOST, 21)
            print(f"✅ Conectado em {time.time() - start_time:.2f}s")
            
            print("🔄 Fazendo login...")
            ftp.login(FTP_USER, FTP_PASSWORD)
            print("✅ Login realizado com sucesso!")
            
            print("🔄 Listando diretórios...")
            files = ftp.nlst()
            print(f"✅ Encontrados {len(files)} itens no diretório raiz")
            
            print("🔄 Testando criação de diretório...")
            try:
                ftp.mkd('teste_conectividade')
                print("✅ Diretório de teste criado")
                
                # Remove o diretório de teste
                ftp.rmd('teste_conectividade')
                print("✅ Diretório de teste removido")
            except Exception as e:
                print(f"⚠️  Erro ao criar/remover diretório de teste: {e}")
            
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
    FTP_HOST = "gpreto.space"
    FTP_USER = "u715606397.nova"
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
            
            with open(test_filename, 'rb') as f:
                ftp.storbinary(f'STOR {test_filename}', f)
            
            print("✅ Upload realizado com sucesso!")
            
            # Remove arquivo de teste do servidor
            try:
                ftp.delete(test_filename)
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
    conectividade_ok = testar_conectividade_ftp()
    
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


