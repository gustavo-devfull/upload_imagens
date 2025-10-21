#!/usr/bin/env python3
"""
🔧 CONFIGURADOR FTP
Script para configurar e testar conexão FTP
"""

import ftplib
import os
import sys

def testar_conexao_ftp(host, user, password, directory="/"):
    """Testa conexão com servidor FTP"""
    try:
        print(f"🔗 Testando conexão FTP...")
        print(f"   Host: {host}")
        print(f"   Usuário: {user}")
        print(f"   Diretório: {directory}")
        
        # Conectar
        ftp = ftplib.FTP()
        ftp.connect(host, 21)
        ftp.login(user, password)
        ftp.cwd(directory)
        
        # Listar arquivos
        files = ftp.nlst()
        print(f"✅ Conexão bem-sucedida!")
        print(f"📁 Arquivos no diretório ({len(files)}):")
        for file in files[:10]:  # Mostrar apenas os primeiros 10
            print(f"   • {file}")
        if len(files) > 10:
            print(f"   ... e mais {len(files) - 10} arquivos")
        
        # Testar upload
        test_content = b"Teste de conexao FTP - " + str.encode(str(os.getpid()))
        test_filename = f"teste_conexao_{os.getpid()}.txt"
        
        print(f"📤 Testando upload: {test_filename}")
        ftp.storbinary(f'STOR {test_filename}', test_content)
        
        # Verificar se foi criado
        files_after = ftp.nlst()
        if test_filename in files_after:
            print(f"✅ Upload de teste bem-sucedido!")
            
            # Remover arquivo de teste
            ftp.delete(test_filename)
            print(f"🗑️ Arquivo de teste removido")
        else:
            print(f"❌ Upload de teste falhou!")
        
        ftp.quit()
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão FTP: {e}")
        return False

def configurar_sistema():
    """Configura o sistema FTP"""
    print("🔧 CONFIGURADOR FTP")
    print("=" * 50)
    
    # Solicitar dados FTP
    print("📝 Digite os dados do seu servidor FTP:")
    host = input("🌐 Host (ex: ftp.exemplo.com): ").strip()
    user = input("👤 Usuário: ").strip()
    password = input("🔒 Senha: ").strip()
    directory = input("📁 Diretório (ex: /uploads/ ou /): ").strip() or "/"
    
    print("\n" + "=" * 50)
    
    # Testar conexão
    if testar_conexao_ftp(host, user, password, directory):
        print("\n✅ CONFIGURAÇÃO VÁLIDA!")
        
        # Gerar código de configuração
        config_code = f'''
# Configurações FTP - Configure no arquivo sistema_flask_ftp.py
FTP_CONFIG = {{
    'host': '{host}',
    'user': '{user}',
    'password': '{password}',
    'directory': '{directory}'
}}
'''
        
        print("\n📋 CÓDIGO DE CONFIGURAÇÃO:")
        print("-" * 50)
        print(config_code)
        print("-" * 50)
        
        # Salvar em arquivo
        with open('ftp_config.txt', 'w') as f:
            f.write(config_code)
        
        print(f"\n💾 Configuração salva em: ftp_config.txt")
        print(f"📝 Copie o código acima para o arquivo sistema_flask_ftp.py")
        
        return True
    else:
        print("\n❌ CONFIGURAÇÃO INVÁLIDA!")
        print("Verifique os dados e tente novamente.")
        return False

def main():
    """Função principal"""
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        # Modo teste com dados específicos
        if len(sys.argv) >= 5:
            host = sys.argv[2]
            user = sys.argv[3]
            password = sys.argv[4]
            directory = sys.argv[5] if len(sys.argv) > 5 else "/"
            
            print("🧪 MODO TESTE")
            print("=" * 50)
            testar_conexao_ftp(host, user, password, directory)
        else:
            print("❌ Uso: python configurador_ftp.py test <host> <user> <password> [directory]")
    else:
        # Modo configuração interativa
        configurar_sistema()

if __name__ == "__main__":
    main()
