# 🔑 Sistema SSH com Chaves - Guia Completo

## 📋 **VANTAGENS DAS CHAVES SSH**

- ✅ **Mais Seguro:** Não expõe senhas em texto plano
- ✅ **Mais Confiável:** Menos propenso a falhas de autenticação
- ✅ **Melhor Performance:** Conexões mais rápidas
- ✅ **Padrão da Indústria:** Método recomendado para produção
- ✅ **Fallback Automático:** Se chave falhar, usa senha

## 🔧 **CONFIGURAÇÃO SSH**

**Host:** 46.202.90.62  
**Porta:** 65002  
**Usuário:** u715606397  
**Chave:** ~/.ssh/id_ed25519  
**Chave Pública:** ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILIBp9YM0fL/mJflPv8GPQEpK7cA17VoDCHUX4OIz43G u715606397@us-imm-web176.main-hosting.eu

## 📦 **INSTALAÇÃO NO PYTHONANYWHERE**

### **1. Instalar Dependências**
```bash
pip3.10 install --user flask openpyxl paramiko
```

### **2. Criar Diretório do Projeto**
```bash
mkdir -p ~/sistema_upload_excel
cd ~/sistema_upload_excel
```

### **3. Baixar Arquivos**
```bash
# Sistema SSH com Chaves
wget -O sistema_ssh_keys.py "https://raw.githubusercontent.com/gustavo-devfull/upload_imagens/main/sistema_ssh_keys.py"

# WSGI
wget -O wsgi.py "https://raw.githubusercontent.com/gustavo-devfull/upload_imagens/main/wsgi.py"

# Script de geração de chave
wget -O gerar_chave_ssh.sh "https://raw.githubusercontent.com/gustavo-devfull/upload_imagens/main/gerar_chave_ssh.sh"
```

### **4. Gerar Chave SSH**
```bash
bash gerar_chave_ssh.sh
```

### **5. Configurar Chave no Servidor**
1. Copie a chave pública gerada
2. Acesse o painel do seu provedor de hospedagem
3. Vá em "SSH Keys" ou "Chaves SSH"
4. Cole a chave pública
5. Salve as configurações

### **6. Testar Conexão SSH**
```bash
ssh -i ~/.ssh/id_ed25519 u715606397@46.202.90.62 -p 65002
```

### **7. Configurar Web App**
- Acesse o dashboard PythonAnywhere
- Vá em "Web" > "Add a new web app"
- Escolha "Manual configuration"
- Defina o arquivo WSGI como: `wsgi.py`
- Reload o web app

## 🚀 **TESTANDO O SISTEMA**

### **1. Acesse o Sistema**
```
https://moribrasil.pythonanywhere.com/
```

### **2. Verifique a Conectividade**
- O sistema mostra automaticamente o status da conexão SSH
- Testa autenticação com chave e senha
- Exibe método de autenticação usado

### **3. Teste o Upload**
- Selecione um arquivo Excel (.xlsx)
- O sistema detecta imagens na coluna H
- Faz upload automático via SSH com chave
- Mostra barra de progresso e timer

## 🔍 **TROUBLESHOOTING**

### **Problema: "Chave não encontrada"**
- **Causa:** Arquivo de chave SSH não existe
- **Solução:** Execute `bash gerar_chave_ssh.sh`

### **Problema: "SSH com chave falhou"**
- **Causa:** Chave não está configurada no servidor
- **Solução:** Adicione a chave pública ao servidor SSH

### **Problema: "SSH com senha também falhou"**
- **Causa:** Problema de conectividade ou credenciais
- **Solução:** Verifique host, porta e credenciais

### **Problema: "Arquivo sem imagens"**
- **Causa:** Arquivo Excel não tem imagens na coluna H
- **Solução:** Usar arquivo com imagens inseridas na coluna H

## 📊 **LOGS E DEBUG**

O sistema fornece logs detalhados:

- **Conectividade SSH:** Testa TCP e SSH automaticamente
- **Autenticação:** Mostra método usado (chave ou senha)
- **Processamento Excel:** Mostra REFs e imagens encontradas
- **Upload:** Detalha cada etapa do upload
- **Erros:** Informações específicas sobre falhas
- **Timer:** Tempo total de processamento

## 🎯 **VANTAGENS DO SISTEMA SSH COM CHAVES**

1. **Segurança Máxima:** Autenticação por chave SSH
2. **Fallback Automático:** Se chave falhar, usa senha
3. **Conectividade Robusta:** Testa TCP e SSH automaticamente
4. **Detecção Inteligente:** Identifica imagens na coluna H corretamente
5. **Interface Moderna:** Frontend com barra de progresso e timer
6. **Debug Completo:** Logs detalhados para troubleshooting
7. **Upload Confiável:** SSH com timeout e retry automático
8. **Tratamento de Erros:** Mensagens claras sobre problemas

## 🔗 **URLS DO SISTEMA**

- **Frontend:** `https://moribrasil.pythonanywhere.com/`
- **Health Check:** `https://moribrasil.pythonanywhere.com/health`
- **Upload API:** `https://moribrasil.pythonanywhere.com/upload`

## 📞 **SUPORTE**

Para problemas ou dúvidas:
1. Verifique os logs de debug no sistema
2. Teste a conectividade SSH manualmente
3. Confirme que a chave SSH está configurada no servidor
4. Confirme que o arquivo Excel tem imagens na coluna H
5. Verifique as configurações de rede/firewall

## 🔧 **TESTE MANUAL DE CONECTIVIDADE**

Para testar SSH manualmente no PythonAnywhere:

```python
import paramiko
import socket

# Teste TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(10)
result = sock.connect_ex(("46.202.90.62", 65002))
sock.close()
print(f"TCP conectado: {result == 0}")

# Teste SSH com chave
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("46.202.90.62", 65002, "u715606397", key_filename="~/.ssh/id_ed25519", timeout=10)
    sftp = ssh.open_sftp()
    sftp.close()
    ssh.close()
    print("SSH com chave funcionando!")
except Exception as e:
    print(f"SSH com chave falhou: {e}")
    
    # Teste SSH com senha
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect("46.202.90.62", 65002, "u715606397", "]X9CC>t~ihWhdzNq", timeout=10)
        sftp = ssh.open_sftp()
        sftp.close()
        ssh.close()
        print("SSH com senha funcionando!")
    except Exception as e2:
        print(f"SSH com senha também falhou: {e2}")
```

## 🔐 **SEGURANÇA**

- **Chave Privada:** Mantida segura no PythonAnywhere
- **Chave Pública:** Adicionada ao servidor SSH
- **Fallback:** Senha como backup se chave falhar
- **Permissões:** Arquivos SSH com permissões corretas
- **Timeout:** Conexões com timeout para evitar travamentos
