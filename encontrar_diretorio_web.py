#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para encontrar o diretório correto para as imagens no servidor
"""

import paramiko

def encontrar_diretorio_web():
    """Encontra o diretório correto para servir arquivos web"""
    
    print("🔍 PROCURANDO DIRETÓRIO WEB CORRETO")
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
        
        # Lista diretórios na raiz
        print("\n📁 Diretórios na raiz:")
        stdin, stdout, stderr = ssh.exec_command("ls -la")
        output = stdout.read().decode()
        print(output)
        
        # Verifica se existe public_html
        stdin, stdout, stderr = ssh.exec_command("ls -la public_html/")
        output = stdout.read().decode()
        
        if "No such file or directory" not in output:
            print("\n✅ Diretório 'public_html' encontrado!")
            print("📁 Conteúdo do public_html:")
            print(output)
            
            # Verifica se existe www
            stdin, stdout, stderr = ssh.exec_command("ls -la public_html/www/")
            www_output = stdout.read().decode()
            
            if "No such file or directory" not in www_output:
                print("\n✅ Diretório 'public_html/www' encontrado!")
                print("📁 Conteúdo do public_html/www:")
                print(www_output)
                
                # Verifica se existe domínio específico
                stdin, stdout, stderr = ssh.exec_command("ls -la public_html/www/gpreto.space/")
                domain_output = stdout.read().decode()
                
                if "No such file or directory" not in domain_output:
                    print("\n✅ Diretório do domínio encontrado!")
                    print("📁 Conteúdo do public_html/www/gpreto.space:")
                    print(domain_output)
                    
                    # Verifica se existe wp-content
                    stdin, stdout, stderr = ssh.exec_command("ls -la public_html/www/gpreto.space/wp-content/")
                    wp_output = stdout.read().decode()
                    
                    if "No such file or directory" not in wp_output:
                        print("\n✅ WordPress detectado!")
                        print("📁 Conteúdo do wp-content:")
                        print(wp_output)
                        
                        # Verifica se existe uploads
                        stdin, stdout, stderr = ssh.exec_command("ls -la public_html/www/gpreto.space/wp-content/uploads/")
                        uploads_output = stdout.read().decode()
                        
                        if "No such file or directory" not in uploads_output:
                            print("\n✅ Diretório de uploads do WordPress encontrado!")
                            print("📁 Conteúdo do wp-content/uploads:")
                            print(uploads_output)
                            
                            # Cria diretório para nossas imagens
                            stdin, stdout, stderr = ssh.exec_command("mkdir -p public_html/www/gpreto.space/wp-content/uploads/products/")
                            print("✅ Diretório 'products' criado no WordPress")
                            
                            # Move as imagens para o local correto
                            stdin, stdout, stderr = ssh.exec_command("mv images/products/*.jpg public_html/www/gpreto.space/wp-content/uploads/products/")
                            print("✅ Imagens movidas para o diretório WordPress")
                            
                            # Ajusta permissões
                            stdin, stdout, stderr = ssh.exec_command("chmod 755 public_html/www/gpreto.space/wp-content/uploads/products/")
                            stdin, stdout, stderr = ssh.exec_command("chmod 644 public_html/www/gpreto.space/wp-content/uploads/products/*.jpg")
                            print("✅ Permissões ajustadas")
                            
                            # Verifica resultado final
                            stdin, stdout, stderr = ssh.exec_command("ls -la public_html/www/gpreto.space/wp-content/uploads/products/")
                            final_output = stdout.read().decode()
                            print("\n📋 Resultado final:")
                            print(final_output)
                            
                            print("\n🌐 URLs corretas das imagens:")
                            print("https://gpreto.space/wp-content/uploads/products/T608.jpg")
                            print("https://gpreto.space/wp-content/uploads/products/106-6S.jpg")
                            
                            return True
        
        ssh.close()
        return False
        
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Encontrando Diretório Web Correto")
    print("   Sistema SSH/SFTP")
    print()
    
    if encontrar_diretorio_web():
        print("\n🎉 Imagens movidas para o local correto!")
        print("   Agora elas devem estar acessíveis via web.")
    else:
        print("\n❌ Não foi possível encontrar o diretório web correto.")
    
    print("\n" + "="*50)

