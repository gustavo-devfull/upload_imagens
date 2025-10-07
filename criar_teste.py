#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar arquivo de teste na raiz do servidor
"""

import paramiko

def criar_arquivo_teste():
    """Cria um arquivo de teste na raiz do servidor"""
    
    print("🧪 CRIANDO ARQUIVO DE TESTE")
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
        
        print("✅ Conectado ao servidor SSH")
        
        # 1. Cria arquivo de teste na raiz
        print("\n📝 Criando arquivo de teste...")
        test_content = "Teste de acesso ao servidor - Sistema de imagens"
        stdin, stdout, stderr = ssh.exec_command(f'echo "{test_content}" > public_html/teste.txt')
        print("✅ Arquivo teste.txt criado")
        
        # 2. Ajusta permissões
        stdin, stdout, stderr = ssh.exec_command("chmod 644 public_html/teste.txt")
        print("✅ Permissões ajustadas")
        
        # 3. Testa acesso
        print("\n🧪 Testando acesso ao arquivo...")
        stdin, stdout, stderr = ssh.exec_command("curl -I https://gpreto.space/teste.txt")
        curl_output = stdout.read().decode()
        print("📡 Resposta do servidor:")
        print(curl_output)
        
        # 4. Cria diretório images na raiz
        print("\n📁 Criando diretório images na raiz...")
        stdin, stdout, stderr = ssh.exec_command("mkdir -p public_html/images/products")
        print("✅ Diretório images/products criado")
        
        # 5. Move imagens para images/products
        print("\n📦 Movendo imagens para images/products...")
        stdin, stdout, stderr = ssh.exec_command("cp public_html/wp-content/uploads/products/*.jpg public_html/images/products/")
        print("✅ Imagens movidas")
        
        # 6. Ajusta permissões
        stdin, stdout, stderr = ssh.exec_command("chmod 755 public_html/images public_html/images/products")
        stdin, stdout, stderr = ssh.exec_command("chmod 644 public_html/images/products/*.jpg")
        print("✅ Permissões ajustadas")
        
        # 7. Testa acesso às imagens
        print("\n🧪 Testando acesso às imagens...")
        stdin, stdout, stderr = ssh.exec_command("curl -I https://gpreto.space/images/products/T608.jpg")
        image_output = stdout.read().decode()
        print("📡 Resposta da imagem:")
        print(image_output)
        
        # 8. Lista conteúdo do diretório
        stdin, stdout, stderr = ssh.exec_command("ls -la public_html/images/products/")
        list_output = stdout.read().decode()
        print("📁 Conteúdo do diretório images/products:")
        print(list_output)
        
        ssh.close()
        
        print("\n🎉 Teste concluído!")
        print("\n🌐 URLs para testar:")
        print("   https://gpreto.space/teste.txt")
        print("   https://gpreto.space/images/products/T608.jpg")
        print("   https://gpreto.space/images/products/106-6S.jpg")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Criando Arquivo de Teste")
    print("   Sistema SSH/SFTP")
    print()
    
    if criar_arquivo_teste():
        print("\n🎉 Teste concluído!")
        print("   Verifique se os links estão funcionando.")
    else:
        print("\n❌ Erro no teste.")
    
    print("\n" + "="*50)

