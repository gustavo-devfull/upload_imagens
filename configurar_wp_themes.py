#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para configurar sistema para usar wp-content/themes
"""

import paramiko

def configurar_wp_themes():
    """Configura sistema para usar wp-content/themes"""
    
    print("🎨 CONFIGURANDO SISTEMA PARA WP-CONTENT/THEMES")
    print("=" * 50)
    
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
        
        # 1. Cria diretório products em wp-content/themes
        print("\n📁 Criando diretório products em wp-content/themes...")
        stdin, stdout, stderr = ssh.exec_command("mkdir -p public_html/wp-content/themes/products")
        print("✅ Diretório criado")
        
        # 2. Move as imagens para wp-content/themes/products
        print("\n📦 Movendo imagens...")
        stdin, stdout, stderr = ssh.exec_command("cp public_html/galeria/*.jpg public_html/wp-content/themes/products/")
        print("✅ Imagens movidas")
        
        # 3. Ajusta permissões
        print("\n🔧 Ajustando permissões...")
        stdin, stdout, stderr = ssh.exec_command("chmod 755 public_html/wp-content/themes/products")
        stdin, stdout, stderr = ssh.exec_command("chmod 644 public_html/wp-content/themes/products/*.jpg")
        print("✅ Permissões ajustadas")
        
        # 4. Testa acesso
        print("\n🧪 Testando acesso...")
        stdin, stdout, stderr = ssh.exec_command("curl -I https://gpreto.space/wp-content/themes/products/T608.jpg")
        test_output = stdout.read().decode()
        print("📡 Resposta do servidor:")
        print(test_output)
        
        # 5. Lista conteúdo
        stdin, stdout, stderr = ssh.exec_command("ls -la public_html/wp-content/themes/products/")
        list_output = stdout.read().decode()
        print("📁 Conteúdo do diretório:")
        print(list_output)
        
        ssh.close()
        
        print("\n🎉 Sistema configurado!")
        print("\n🌐 URLs das imagens:")
        print("   https://gpreto.space/wp-content/themes/products/T608.jpg")
        print("   https://gpreto.space/wp-content/themes/products/106-6S.jpg")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na configuração: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Configurando Sistema para wp-content/themes")
    print("   Sistema SSH/SFTP")
    print()
    
    if configurar_wp_themes():
        print("\n🎉 Configuração concluída!")
        print("   Teste agora os links das imagens.")
    else:
        print("\n❌ Erro na configuração.")
    
    print("\n" + "="*50)

