# 🚀 Sistema SSH Porta 65002 - Guia de Deploy PythonAnywhere

## 📋 **CARACTERÍSTICAS DO SISTEMA**

- ✅ **SSH específico na porta 65002**
- ✅ **Teste automático de conectividade SSH**
- ✅ **Detecção inteligente de imagens na coluna H**
- ✅ **Upload robusto com tratamento de erros**
- ✅ **Interface web moderna com barra de progresso**
- ✅ **Debug detalhado para troubleshooting**
- ✅ **Timer de processamento**

## 🔧 **CONFIGURAÇÃO SSH**

**Host:** 46.202.90.62  
**Porta:** 65002  
**Usuário:** u715606397  
**Senha:** ]X9CC>t~ihWhdzNq  

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
# Sistema SSH Porta 65002
wget -O sistema_ssh_65002.py "https://raw.githubusercontent.com/gustavo-devfull/upload_imagens/main/sistema_ssh_65002.py"

# WSGI
wget -O wsgi.py "https://raw.githubusercontent.com/gustavo-devfull/upload_imagens/main/wsgi.py"
```

### **4. Configurar Web App**
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
- Testa conectividade TCP e SSH na porta 65002
- Exibe configurações SSH na interface

### **3. Teste o Upload**
- Selecione um arquivo Excel (.xlsx)
- O sistema detecta imagens na coluna H
- Faz upload automático via SSH
- Mostra barra de progresso e timer

## 🔍 **TROUBLESHOOTING**

### **Problema: "Sem conexão SSH"**
- **Causa:** SSH na porta 65002 não está acessível
- **Solução:** Verificar configurações de firewall/rede

### **Problema: "Arquivo sem imagens"**
- **Causa:** Arquivo Excel não tem imagens na coluna H
- **Solução:** Usar arquivo com imagens inseridas na coluna H

### **Problema: "Erro no upload"**
- **Causa:** Problema de permissões ou conectividade
- **Solução:** Verificar logs de debug no sistema

## 📊 **LOGS E DEBUG**

O sistema fornece logs detalhados:

- **Conectividade SSH:** Testa TCP e SSH automaticamente
- **Processamento Excel:** Mostra REFs e imagens encontradas
- **Upload:** Detalha cada etapa do upload
- **Erros:** Informações específicas sobre falhas
- **Timer:** Tempo total de processamento

## 🎯 **VANTAGENS DO SISTEMA SSH**

1. **SSH Específico:** Configurado especificamente para porta 65002
2. **Conectividade Robusta:** Testa TCP e SSH automaticamente
3. **Detecção Inteligente:** Identifica imagens na coluna H corretamente
4. **Interface Moderna:** Frontend com barra de progresso e timer
5. **Debug Completo:** Logs detalhados para troubleshooting
6. **Upload Confiável:** SSH com timeout e retry automático
7. **Tratamento de Erros:** Mensagens claras sobre problemas

## 🔗 **URLS DO SISTEMA**

- **Frontend:** `https://moribrasil.pythonanywhere.com/`
- **Health Check:** `https://moribrasil.pythonanywhere.com/health`
- **Upload API:** `https://moribrasil.pythonanywhere.com/upload`

## 📞 **SUPORTE**

Para problemas ou dúvidas:
1. Verifique os logs de debug no sistema
2. Teste a conectividade SSH manualmente
3. Confirme que o arquivo Excel tem imagens na coluna H
4. Verifique as configurações de rede/firewall
5. Confirme que a porta 65002 está acessível

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

# Teste SSH
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("46.202.90.62", 65002, "u715606397", "]X9CC>t~ihWhdzNq", timeout=10)
    sftp = ssh.open_sftp()
    sftp.close()
    ssh.close()
    print("SSH funcionando!")
except Exception as e:
    print(f"SSH falhou: {e}")
```
