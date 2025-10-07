#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar servidor de imagens via PHP
"""

import paramiko

def criar_servidor_imagens_php():
    """Cria um servidor de imagens via PHP"""
    
    print("🐘 CRIANDO SERVIDOR DE IMAGENS VIA PHP")
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
        
        # 1. Cria diretório para imagens
        print("\n📁 Criando diretório para imagens...")
        stdin, stdout, stderr = ssh.exec_command("mkdir -p public_html/images/products")
        print("✅ Diretório criado")
        
        # 2. Move as imagens
        print("\n📦 Movendo imagens...")
        stdin, stdout, stderr = ssh.exec_command("cp public_html/wp-content/products/*.jpg public_html/images/products/")
        print("✅ Imagens movidas")
        
        # 3. Cria arquivo PHP para servir imagens
        print("\n🐘 Criando servidor PHP...")
        php_content = '''<?php
// Servidor de imagens
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET');
header('Access-Control-Allow-Headers: Content-Type');

$image = $_GET['img'] ?? '';
$path = __DIR__ . '/products/' . $image;

if (empty($image) || !file_exists($path)) {
    http_response_code(404);
    echo 'Imagem não encontrada';
    exit;
}

$extension = strtolower(pathinfo($path, PATHINFO_EXTENSION));
$allowed_extensions = ['jpg', 'jpeg', 'png', 'gif'];

if (!in_array($extension, $allowed_extensions)) {
    http_response_code(403);
    echo 'Tipo de arquivo não permitido';
    exit;
}

$mime_types = [
    'jpg' => 'image/jpeg',
    'jpeg' => 'image/jpeg',
    'png' => 'image/png',
    'gif' => 'image/gif'
];

header('Content-Type: ' . $mime_types[$extension]);
header('Content-Length: ' . filesize($path));
header('Cache-Control: public, max-age=31536000');

readfile($path);
?>
'''
        
        stdin, stdout, stderr = ssh.exec_command(f'echo "{php_content}" > public_html/images/index.php')
        print("✅ Servidor PHP criado")
        
        # 4. Ajusta permissões
        print("\n🔧 Ajustando permissões...")
        stdin, stdout, stderr = ssh.exec_command("chmod 755 public_html/images public_html/images/products")
        stdin, stdout, stderr = ssh.exec_command("chmod 644 public_html/images/index.php")
        stdin, stdout, stderr = ssh.exec_command("chmod 644 public_html/images/products/*.jpg")
        print("✅ Permissões ajustadas")
        
        # 5. Testa acesso via PHP
        print("\n🧪 Testando acesso via PHP...")
        stdin, stdout, stderr = ssh.exec_command("curl -I 'https://gpreto.space/images/?img=T608.jpg'")
        test_output = stdout.read().decode()
        print("📡 Resposta do servidor PHP:")
        print(test_output)
        
        # 6. Lista conteúdo
        stdin, stdout, stderr = ssh.exec_command("ls -la public_html/images/")
        list_output = stdout.read().decode()
        print("📁 Conteúdo do diretório images:")
        print(list_output)
        
        ssh.close()
        
        print("\n🎉 Servidor PHP criado!")
        print("\n🌐 URLs das imagens via PHP:")
        print("   https://gpreto.space/images/?img=T608.jpg")
        print("   https://gpreto.space/images/?img=106-6S.jpg")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar servidor PHP: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Criando Servidor de Imagens via PHP")
    print("   Sistema SSH/SFTP")
    print()
    
    if criar_servidor_imagens_php():
        print("\n🎉 Servidor PHP criado!")
        print("   Teste agora os links das imagens.")
    else:
        print("\n❌ Erro ao criar servidor.")
    
    print("\n" + "="*50)

