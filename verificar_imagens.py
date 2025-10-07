#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar e corrigir permissões das imagens no servidor SSH
"""

import paramiko
import os

def verificar_imagens_no_servidor():
    """Verifica se as imagens estão no servidor e corrige permissões"""
    
    print("🔍 VERIFICAÇÃO DE IMAGENS NO SERVIDOR")
    print("=" * 40)
    
    # Configurações SSH
    SSH_HOST = "46.202.90.62"
    SSH_PORT = 65002
    SSH_USER = "u715606397"
    SSH_PASSWORD = "]X9CC>t~ihWhdzNq"
    
    try:
        # Conecta via SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        ssh.connect(
            hostname=SSH_HOST,
            port=SSH_PORT,
            username=SSH_USER,
            password=SSH_PASSWORD,
            timeout=30
        )
        
        print("✅ Conectado ao servidor SSH")
        
        # Verifica se o diretório existe
        stdin, stdout, stderr = ssh.exec_command("ls -la images/")
        output = stdout.read().decode()
        
        if "No such file or directory" in output:
            print("❌ Diretório 'images' não encontrado")
            return False
        
        print("✅ Diretório 'images' encontrado")
        print(f"📁 Conteúdo do diretório images/:")
        print(output)
        
        # Verifica se o diretório products existe
        stdin, stdout, stderr = ssh.exec_command("ls -la images/products/")
        output = stdout.read().decode()
        
        if "No such file or directory" in output:
            print("❌ Diretório 'images/products' não encontrado")
            return False
        
        print("✅ Diretório 'images/products' encontrado")
        print(f"📁 Conteúdo do diretório images/products/:")
        print(output)
        
        # Lista arquivos de imagem
        stdin, stdout, stderr = ssh.exec_command("ls -la images/products/*.jpg")
        output = stdout.read().decode()
        
        if output.strip():
            print("✅ Imagens encontradas:")
            print(output)
            
            # Corrige permissões das imagens
            print("\n🔧 Corrigindo permissões...")
            stdin, stdout, stderr = ssh.exec_command("chmod 644 images/products/*.jpg")
            print("✅ Permissões das imagens ajustadas para 644")
            
            # Corrige permissões dos diretórios
            stdin, stdout, stderr = ssh.exec_command("chmod 755 images/ images/products/")
            print("✅ Permissões dos diretórios ajustadas para 755")
            
            # Verifica permissões finais
            stdin, stdout, stderr = ssh.exec_command("ls -la images/products/")
            output = stdout.read().decode()
            print(f"\n📋 Permissões finais:")
            print(output)
            
        else:
            print("❌ Nenhuma imagem encontrada no diretório")
            return False
        
        ssh.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return False

def testar_urls_das_imagens():
    """Testa se as URLs das imagens estão acessíveis"""
    
    print("\n🌐 TESTANDO URLs DAS IMAGENS")
    print("=" * 35)
    
    import urllib.request
    import urllib.error
    
    urls = [
        "https://gpreto.space/images/products/T608.jpg",
        "https://gpreto.space/images/products/106-6S.jpg"
    ]
    
    for url in urls:
        try:
            print(f"🔄 Testando: {url}")
            response = urllib.request.urlopen(url, timeout=10)
            if response.status == 200:
                print(f"✅ Acessível - Status: {response.status}")
                print(f"   Tamanho: {len(response.read())} bytes")
            else:
                print(f"❌ Erro - Status: {response.status}")
        except urllib.error.HTTPError as e:
            print(f"❌ Erro HTTP: {e.code} - {e.reason}")
        except urllib.error.URLError as e:
            print(f"❌ Erro de URL: {e.reason}")
        except Exception as e:
            print(f"❌ Erro: {e}")

def criar_arquivo_htaccess():
    """Cria arquivo .htaccess para permitir acesso às imagens"""
    
    print("\n📝 CRIANDO ARQUIVO .HTACCESS")
    print("=" * 30)
    
    # Configurações SSH
    SSH_HOST = "46.202.90.62"
    SSH_PORT = 65002
    SSH_USER = "u715606397"
    SSH_PASSWORD = "]X9CC>t~ihWhdzNq"
    
    try:
        # Conecta via SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        ssh.connect(
            hostname=SSH_HOST,
            port=SSH_PORT,
            username=SSH_USER,
            password=SSH_PASSWORD,
            timeout=30
        )
        
        # Cria arquivo .htaccess
        htaccess_content = """# Permitir acesso às imagens
<Files "*.jpg">
    Order allow,deny
    Allow from all
</Files>

<Files "*.jpeg">
    Order allow,deny
    Allow from all
</Files>

<Files "*.png">
    Order allow,deny
    Allow from all
</Files>

<Files "*.gif">
    Order allow,deny
    Allow from all
</Files>

# Configurações de cache
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType image/jpg "access plus 1 month"
    ExpiresByType image/jpeg "access plus 1 month"
    ExpiresByType image/png "access plus 1 month"
    ExpiresByType image/gif "access plus 1 month"
</IfModule>
"""
        
        # Salva arquivo .htaccess no diretório images/products
        stdin, stdout, stderr = ssh.exec_command(f'echo "{htaccess_content}" > images/products/.htaccess')
        
        # Ajusta permissões do .htaccess
        stdin, stdout, stderr = ssh.exec_command("chmod 644 images/products/.htaccess")
        
        print("✅ Arquivo .htaccess criado com sucesso")
        
        ssh.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar .htaccess: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Verificação e Correção de Imagens")
    print("   Sistema SSH/SFTP")
    print()
    
    # Verifica imagens no servidor
    if verificar_imagens_no_servidor():
        # Cria arquivo .htaccess
        criar_arquivo_htaccess()
        
        # Testa URLs
        testar_urls_das_imagens()
        
        print("\n🎉 Verificação concluída!")
        print("   Se as imagens ainda não aparecerem, pode ser:")
        print("   • Cache do navegador (limpe o cache)")
        print("   • Configuração do servidor web")
        print("   • DNS ainda não propagado")
    else:
        print("\n❌ Problemas encontrados no servidor")
    
    print("\n" + "="*50)

