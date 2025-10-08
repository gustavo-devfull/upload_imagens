#!/usr/bin/env python3
"""
Script de Diagnóstico SSH - Porta 65002
Testa conectividade SSH e identifica problemas
"""

import socket
import time
import sys

def test_tcp_connection(host, port, timeout=10):
    """Testa conectividade TCP"""
    print(f"🔌 Testando TCP: {host}:{port}")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        start_time = time.time()
        result = sock.connect_ex((host, port))
        end_time = time.time()
        sock.close()
        
        if result == 0:
            print(f"✅ TCP conectado em {end_time - start_time:.2f}s")
            return True
        else:
            print(f"❌ TCP falhou (código: {result})")
            return False
    except Exception as e:
        print(f"❌ Erro TCP: {e}")
        return False

def test_ssh_connection(host, port, user, password, timeout=10):
    """Testa conectividade SSH"""
    print(f"🔐 Testando SSH: {user}@{host}:{port}")
    try:
        import paramiko
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        start_time = time.time()
        ssh.connect(host, port, user, password, timeout=timeout)
        end_time = time.time()
        
        # Testa SFTP
        sftp = ssh.open_sftp()
        sftp.close()
        ssh.close()
        
        print(f"✅ SSH funcionando em {end_time - start_time:.2f}s")
        return True
        
    except ImportError:
        print("❌ paramiko não instalado")
        return False
    except Exception as e:
        print(f"❌ SSH falhou: {e}")
        return False

def test_alternative_ports(host, user, password):
    """Testa portas alternativas"""
    ports_to_test = [22, 2222, 65002, 8022, 443, 80]
    
    print(f"\n🔍 Testando portas alternativas para {host}")
    working_ports = []
    
    for port in ports_to_test:
        print(f"\n--- Testando porta {port} ---")
        if test_tcp_connection(host, port, timeout=5):
            if test_ssh_connection(host, port, user, password, timeout=5):
                working_ports.append(port)
                print(f"✅ Porta {port} funcionando!")
            else:
                print(f"⚠️ Porta {port} TCP OK, mas SSH falhou")
        else:
            print(f"❌ Porta {port} não acessível")
    
    return working_ports

def main():
    print("🚀 DIAGNÓSTICO SSH - PORTA 65002")
    print("=" * 50)
    
    # Configurações
    host = "46.202.90.62"
    port = 65002
    user = "u715606397"
    password = "]X9CC>t~ihWhdzNq"
    
    print(f"Host: {host}")
    print(f"Porta: {port}")
    print(f"Usuário: {user}")
    print("=" * 50)
    
    # Teste principal
    print("\n🔍 TESTE PRINCIPAL")
    tcp_ok = test_tcp_connection(host, port)
    ssh_ok = False
    
    if tcp_ok:
        ssh_ok = test_ssh_connection(host, port, user, password)
    
    # Teste de portas alternativas
    if not ssh_ok:
        print("\n🔍 TESTANDO PORTAS ALTERNATIVAS")
        working_ports = test_alternative_ports(host, user, password)
        
        if working_ports:
            print(f"\n✅ Portas funcionando: {working_ports}")
            print("💡 Use uma dessas portas no sistema")
        else:
            print("\n❌ Nenhuma porta SSH funcionando")
            print("💡 Possíveis causas:")
            print("   • Firewall bloqueando conexões")
            print("   • Servidor SSH desligado")
            print("   • Credenciais incorretas")
            print("   • Restrições de rede")
    
    # Resumo
    print("\n📊 RESUMO")
    print("=" * 50)
    if ssh_ok:
        print("✅ SSH funcionando na porta 65002")
        print("💡 Sistema pode ser usado normalmente")
    else:
        print("❌ SSH não funcionando")
        print("💡 Considere usar FTP ou Google Drive")
    
    print("\n🔧 PRÓXIMOS PASSOS:")
    if ssh_ok:
        print("1. Use o sistema SSH normalmente")
        print("2. Teste upload com arquivo Excel")
    else:
        print("1. Verifique configurações de rede")
        print("2. Teste credenciais manualmente")
        print("3. Considere usar FTP ou Google Drive")
        print("4. Entre em contato com suporte do servidor")

if __name__ == "__main__":
    main()
