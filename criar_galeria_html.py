#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar galeria HTML simples
"""

import paramiko

def criar_galeria_html():
    """Cria uma galeria HTML simples para servir as imagens"""
    
    print("🌐 CRIANDO GALERIA HTML SIMPLES")
    print("=" * 35)
    
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
        
        # 1. Cria diretório para galeria
        print("\n📁 Criando diretório para galeria...")
        stdin, stdout, stderr = ssh.exec_command("mkdir -p public_html/galeria")
        print("✅ Diretório criado")
        
        # 2. Move as imagens para galeria
        print("\n📦 Movendo imagens...")
        stdin, stdout, stderr = ssh.exec_command("cp public_html/images/products/*.jpg public_html/galeria/")
        print("✅ Imagens movidas")
        
        # 3. Cria arquivo HTML para galeria
        print("\n🌐 Criando galeria HTML...")
        html_content = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Galeria de Imagens - Sistema Excel</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { color: #333; text-align: center; }
        .gallery { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .image-card { background: white; border-radius: 8px; padding: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .image-card img { width: 100%; height: auto; border-radius: 4px; }
        .image-name { font-weight: bold; margin-top: 10px; color: #666; }
        .image-url { font-size: 12px; color: #999; word-break: break-all; margin-top: 5px; }
        .copy-btn { background: #007cba; color: white; border: none; padding: 5px 10px; border-radius: 3px; cursor: pointer; font-size: 12px; }
        .copy-btn:hover { background: #005a87; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🖼️ Galeria de Imagens - Sistema Excel</h1>
        <div class="gallery">
            <div class="image-card">
                <img src="T608.jpg" alt="T608">
                <div class="image-name">T608.jpg</div>
                <div class="image-url" id="url1">https://gpreto.space/galeria/T608.jpg</div>
                <button class="copy-btn" onclick="copyUrl('url1')">Copiar URL</button>
            </div>
            <div class="image-card">
                <img src="106-6S.jpg" alt="106-6S">
                <div class="image-name">106-6S.jpg</div>
                <div class="image-url" id="url2">https://gpreto.space/galeria/106-6S.jpg</div>
                <button class="copy-btn" onclick="copyUrl('url2')">Copiar URL</button>
            </div>
        </div>
    </div>
    
    <script>
        function copyUrl(elementId) {
            const urlElement = document.getElementById(elementId);
            const url = urlElement.textContent;
            navigator.clipboard.writeText(url).then(() => {
                alert('URL copiada: ' + url);
            });
        }
    </script>
</body>
</html>
'''
        
        stdin, stdout, stderr = ssh.exec_command(f'echo "{html_content}" > public_html/galeria/index.html')
        print("✅ Galeria HTML criada")
        
        # 4. Ajusta permissões
        print("\n🔧 Ajustando permissões...")
        stdin, stdout, stderr = ssh.exec_command("chmod 755 public_html/galeria")
        stdin, stdout, stderr = ssh.exec_command("chmod 644 public_html/galeria/index.html")
        stdin, stdout, stderr = ssh.exec_command("chmod 644 public_html/galeria/*.jpg")
        print("✅ Permissões ajustadas")
        
        # 5. Testa acesso
        print("\n🧪 Testando acesso...")
        stdin, stdout, stderr = ssh.exec_command("curl -I https://gpreto.space/galeria/")
        test_output = stdout.read().decode()
        print("📡 Resposta do servidor:")
        print(test_output)
        
        # 6. Testa acesso direto à imagem
        stdin, stdout, stderr = ssh.exec_command("curl -I https://gpreto.space/galeria/T608.jpg")
        image_output = stdout.read().decode()
        print("📡 Resposta da imagem:")
        print(image_output)
        
        # 7. Lista conteúdo
        stdin, stdout, stderr = ssh.exec_command("ls -la public_html/galeria/")
        list_output = stdout.read().decode()
        print("📁 Conteúdo do diretório:")
        print(list_output)
        
        ssh.close()
        
        print("\n🎉 Galeria HTML criada!")
        print("\n🌐 URLs da galeria:")
        print("   https://gpreto.space/galeria/")
        print("   https://gpreto.space/galeria/T608.jpg")
        print("   https://gpreto.space/galeria/106-6S.jpg")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar galeria: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Criando Galeria HTML Simples")
    print("   Sistema SSH/SFTP")
    print()
    
    if criar_galeria_html():
        print("\n🎉 Galeria criada!")
        print("   Acesse: https://gpreto.space/galeria/")
    else:
        print("\n❌ Erro ao criar galeria.")
    
    print("\n" + "="*50)

