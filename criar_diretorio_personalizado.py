#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar diretório personalizado para imagens
"""

import paramiko

def criar_diretorio_personalizado():
    """Cria diretório personalizado para imagens"""
    
    print("📁 CRIANDO DIRETÓRIO PERSONALIZADO")
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
        
        # 1. Cria diretório personalizado em wp-content
        print("\n📁 Criando diretório personalizado...")
        stdin, stdout, stderr = ssh.exec_command("mkdir -p public_html/wp-content/products")
        print("✅ Diretório wp-content/products criado")
        
        # 2. Move as imagens para o novo diretório
        print("\n📦 Movendo imagens...")
        stdin, stdout, stderr = ssh.exec_command("cp public_html/images/products/*.jpg public_html/wp-content/products/")
        print("✅ Imagens movidas")
        
        # 3. Ajusta permissões
        print("\n🔧 Ajustando permissões...")
        stdin, stdout, stderr = ssh.exec_command("chmod 755 public_html/wp-content/products")
        stdin, stdout, stderr = ssh.exec_command("chmod 644 public_html/wp-content/products/*.jpg")
        print("✅ Permissões ajustadas")
        
        # 4. Testa acesso
        print("\n🧪 Testando acesso...")
        stdin, stdout, stderr = ssh.exec_command("curl -I https://gpreto.space/wp-content/products/T608.jpg")
        test_output = stdout.read().decode()
        print("📡 Resposta do servidor:")
        print(test_output)
        
        # 5. Lista conteúdo
        stdin, stdout, stderr = ssh.exec_command("ls -la public_html/wp-content/products/")
        list_output = stdout.read().decode()
        print("📁 Conteúdo do diretório:")
        print(list_output)
        
        ssh.close()
        
        print("\n🎉 Diretório personalizado criado!")
        print("\n🌐 URLs das imagens:")
        print("   https://gpreto.space/wp-content/products/T608.jpg")
        print("   https://gpreto.space/wp-content/products/106-6S.jpg")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar diretório: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Criando Diretório Personalizado")
    print("   Sistema SSH/SFTP")
    print()
    
    if criar_diretorio_personalizado():
        print("\n🎉 Processo concluído!")
        print("   Teste agora os links das imagens.")
    else:
        print("\n❌ Erro no processo.")
    
    print("\n" + "="*50)

