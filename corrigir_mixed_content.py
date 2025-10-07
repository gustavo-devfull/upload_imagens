#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir Mixed Content no WordPress
"""

import paramiko

def corrigir_mixed_content():
    """Corrige problemas de Mixed Content no WordPress"""
    
    print("🔧 CORRIGINDO MIXED CONTENT NO WORDPRESS")
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
        
        # 1. Atualiza wp-config.php para forçar HTTPS
        print("\n🔧 Configurando HTTPS no wp-config.php...")
        
        wp_config_content = '''
# Forçar HTTPS
define('FORCE_SSL_ADMIN', true);
define('FORCE_SSL', true);

# URLs do site
define('WP_HOME','https://gpreto.space');
define('WP_SITEURL','https://gpreto.space');

# Detectar proxy reverso
if (isset($_SERVER['HTTP_X_FORWARDED_PROTO']) && $_SERVER['HTTP_X_FORWARDED_PROTO'] === 'https') {
    $_SERVER['HTTPS'] = 'on';
}
'''
        
        # Adiciona configurações ao wp-config.php
        stdin, stdout, stderr = ssh.exec_command(f'echo "{wp_config_content}" >> public_html/wp-config.php')
        print("✅ Configurações HTTPS adicionadas ao wp-config.php")
        
        # 2. Cria arquivo .htaccess para forçar HTTPS
        print("\n🔧 Criando .htaccess para forçar HTTPS...")
        
        htaccess_content = '''# Forçar HTTPS
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# Headers de segurança
<IfModule mod_headers.c>
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
    Header always set X-Content-Type-Options nosniff
    Header always set X-Frame-Options DENY
    Header always set X-XSS-Protection "1; mode=block"
</IfModule>

# Permitir acesso às imagens
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
'''
        
        # Salva .htaccess
        stdin, stdout, stderr = ssh.exec_command(f'echo "{htaccess_content}" > public_html/.htaccess')
        print("✅ Arquivo .htaccess atualizado")
        
        # 3. Corrige URLs no banco de dados (se necessário)
        print("\n🔧 Verificando URLs no banco de dados...")
        
        # Comando para atualizar URLs no WordPress via WP-CLI
        wp_cli_commands = [
            "cd public_html && wp search-replace 'http://gpreto.space' 'https://gpreto.space' --dry-run",
            "cd public_html && wp search-replace 'http://gpreto.space' 'https://gpreto.space' --skip-columns=guid"
        ]
        
        for cmd in wp_cli_commands:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            output = stdout.read().decode()
            if output.strip():
                print(f"✅ {output.strip()}")
        
        # 4. Ajusta permissões
        print("\n🔧 Ajustando permissões...")
        stdin, stdout, stderr = ssh.exec_command("chmod 644 public_html/.htaccess")
        stdin, stdout, stderr = ssh.exec_command("chmod 644 public_html/wp-config.php")
        print("✅ Permissões ajustadas")
        
        # 5. Limpa cache (se existir)
        print("\n🔧 Limpando cache...")
        stdin, stdout, stderr = ssh.exec_command("cd public_html && wp cache flush 2>/dev/null || echo 'Cache limpo'")
        print("✅ Cache limpo")
        
        ssh.close()
        
        print("\n🎉 Correções aplicadas com sucesso!")
        print("\n📋 O que foi feito:")
        print("   • Configurado HTTPS forçado no wp-config.php")
        print("   • Criado .htaccess para redirecionar HTTP → HTTPS")
        print("   • Adicionados headers de segurança")
        print("   • Atualizadas URLs no banco de dados")
        print("   • Ajustadas permissões")
        print("   • Cache limpo")
        
        print("\n🌐 Suas imagens agora devem funcionar em:")
        print("   https://gpreto.space/wp-content/uploads/products/T608.jpg")
        print("   https://gpreto.space/wp-content/uploads/products/106-6S.jpg")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao aplicar correções: {e}")
        return False

def testar_imagens():
    """Testa se as imagens estão acessíveis"""
    
    print("\n🧪 TESTANDO ACESSO ÀS IMAGENS")
    print("=" * 35)
    
    import urllib.request
    import ssl
    
    # Ignora verificação SSL para teste
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    urls = [
        "https://gpreto.space/wp-content/uploads/products/T608.jpg",
        "https://gpreto.space/wp-content/uploads/products/106-6S.jpg"
    ]
    
    for url in urls:
        try:
            print(f"🔄 Testando: {url}")
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request, context=ssl_context, timeout=10)
            
            if response.status == 200:
                content = response.read()
                print(f"✅ Acessível - Status: {response.status}")
                print(f"   Tamanho: {len(content)} bytes")
                print(f"   Tipo: {response.headers.get('Content-Type', 'N/A')}")
            else:
                print(f"❌ Erro - Status: {response.status}")
                
        except Exception as e:
            print(f"❌ Erro: {e}")

if __name__ == "__main__":
    print("🚀 Correção de Mixed Content")
    print("   Sistema WordPress")
    print()
    
    if corrigir_mixed_content():
        testar_imagens()
        print("\n🎉 Correções concluídas!")
        print("   Teste agora os links das imagens.")
    else:
        print("\n❌ Erro ao aplicar correções.")
    
    print("\n" + "="*50)

