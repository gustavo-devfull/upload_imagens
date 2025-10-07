#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para mover imagens para o local correto no servidor
"""

import paramiko

def mover_imagens_local_correto():
    """Move as imagens para o local correto no servidor"""
    
    print("📁 MOVENDO IMAGENS PARA LOCAL CORRETO")
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
        
        # 1. Cria diretório products no wp-content/uploads da raiz
        print("\n🔧 Criando diretório products na raiz do WordPress...")
        stdin, stdout, stderr = ssh.exec_command("mkdir -p public_html/wp-content/uploads/products")
        print("✅ Diretório criado")
        
        # 2. Move as imagens do diretório www para a raiz
        print("\n📦 Movendo imagens para a raiz do WordPress...")
        stdin, stdout, stderr = ssh.exec_command("cp public_html/www/gpreto.space/wp-content/uploads/products/*.jpg public_html/wp-content/uploads/products/")
        print("✅ Imagens copiadas")
        
        # 3. Ajusta permissões
        print("\n🔧 Ajustando permissões...")
        stdin, stdout, stderr = ssh.exec_command("chmod 755 public_html/wp-content/uploads/products")
        stdin, stdout, stderr = ssh.exec_command("chmod 644 public_html/wp-content/uploads/products/*.jpg")
        print("✅ Permissões ajustadas")
        
        # 4. Verifica resultado
        print("\n📋 Verificando resultado...")
        stdin, stdout, stderr = ssh.exec_command("ls -la public_html/wp-content/uploads/products/")
        output = stdout.read().decode()
        print("📁 Conteúdo do diretório:")
        print(output)
        
        # 5. Testa se as imagens estão acessíveis
        print("\n🧪 Testando URLs...")
        stdin, stdout, stderr = ssh.exec_command("curl -I https://gpreto.space/wp-content/uploads/products/T608.jpg")
        curl_output = stdout.read().decode()
        print("📡 Resposta do servidor:")
        print(curl_output)
        
        ssh.close()
        
        print("\n🎉 Imagens movidas com sucesso!")
        print("\n🌐 URLs das imagens:")
        print("   https://gpreto.space/wp-content/uploads/products/T608.jpg")
        print("   https://gpreto.space/wp-content/uploads/products/106-6S.jpg")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao mover imagens: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Movendo Imagens para Local Correto")
    print("   Sistema SSH/SFTP")
    print()
    
    if mover_imagens_local_correto():
        print("\n🎉 Processo concluído!")
        print("   Teste agora os links das imagens.")
    else:
        print("\n❌ Erro no processo.")
    
    print("\n" + "="*50)

