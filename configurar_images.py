#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para configurar acesso ao diretório images
"""

import paramiko

def configurar_acesso_images():
    """Configura acesso ao diretório images"""
    
    print("🔧 CONFIGURANDO ACESSO AO DIRETÓRIO IMAGES")
    print("=" * 45)
    
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
        
        # 1. Cria diretório images/products na raiz
        print("\n📁 Criando diretório images/products...")
        stdin, stdout, stderr = ssh.exec_command("mkdir -p public_html/images/products")
        print("✅ Diretório criado")
        
        # 2. Move as imagens
        print("\n📦 Movendo imagens...")
        stdin, stdout, stderr = ssh.exec_command("cp public_html/wp-content/products/*.jpg public_html/images/products/")
        print("✅ Imagens movidas")
        
        # 3. Cria arquivo .htaccess para permitir acesso
        print("\n📝 Criando .htaccess para permitir acesso...")
        htaccess_content = '''# Permitir acesso às imagens
Options -Indexes
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

# Headers de segurança
<IfModule mod_headers.c>
    Header set Access-Control-Allow-Origin "*"
    Header set Cache-Control "public, max-age=31536000"
</IfModule>
'''
        
        stdin, stdout, stderr = ssh.exec_command(f'echo "{htaccess_content}" > public_html/images/.htaccess')
        print("✅ Arquivo .htaccess criado")
        
        # 4. Ajusta permissões
        print("\n🔧 Ajustando permissões...")
        stdin, stdout, stderr = ssh.exec_command("chmod 755 public_html/images public_html/images/products")
        stdin, stdout, stderr = ssh.exec_command("chmod 644 public_html/images/.htaccess")
        stdin, stdout, stderr = ssh.exec_command("chmod 644 public_html/images/products/*.jpg")
        print("✅ Permissões ajustadas")
        
        # 5. Testa acesso
        print("\n🧪 Testando acesso...")
        stdin, stdout, stderr = ssh.exec_command("curl -I https://gpreto.space/images/products/T608.jpg")
        test_output = stdout.read().decode()
        print("📡 Resposta do servidor:")
        print(test_output)
        
        # 6. Lista conteúdo
        stdin, stdout, stderr = ssh.exec_command("ls -la public_html/images/products/")
        list_output = stdout.read().decode()
        print("📁 Conteúdo do diretório:")
        print(list_output)
        
        ssh.close()
        
        print("\n🎉 Configuração concluída!")
        print("\n🌐 URLs das imagens:")
        print("   https://gpreto.space/images/products/T608.jpg")
        print("   https://gpreto.space/images/products/106-6S.jpg")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na configuração: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Configurando Acesso ao Diretório Images")
    print("   Sistema SSH/SFTP")
    print()
    
    if configurar_acesso_images():
        print("\n🎉 Configuração concluída!")
        print("   Teste agora os links das imagens.")
    else:
        print("\n❌ Erro na configuração.")
    
    print("\n" + "="*50)

