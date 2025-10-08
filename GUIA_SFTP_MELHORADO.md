# 🚀 Sistema SFTP Melhorado - Guia de Deploy PythonAnywhere

## 📋 **CARACTERÍSTICAS DO SISTEMA**

- ✅ **Teste automático de conectividade SFTP**
- ✅ **Múltiplas portas SFTP testadas automaticamente**
- ✅ **Detecção inteligente de imagens na coluna H**
- ✅ **Upload robusto com tratamento de erros**
- ✅ **Interface web moderna e responsiva**
- ✅ **Debug detalhado para troubleshooting**

## 🔧 **CONFIGURAÇÕES SFTP TESTADAS**

O sistema testa automaticamente estas configurações:

1. **46.202.90.62:22** (SFTP padrão)
2. **46.202.90.62:65002** (Porta alternativa)
3. **46.202.90.62:2222** (Porta comum)
4. **46.202.90.62:8022** (Porta alternativa)

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
# Sistema SFTP Melhorado
wget -O sistema_sftp_melhorado.py "https://raw.githubusercontent.com/seu_usuario/sistema_upload_excel/main/sistema_sftp_melhorado.py"

# WSGI
wget -O wsgi.py "https://raw.githubusercontent.com/seu_usuario/sistema_upload_excel/main/wsgi.py"
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
- O sistema mostra automaticamente o status da conexão SFTP
- Testa todas as portas configuradas
- Exibe qual configuração está funcionando

### **3. Teste o Upload**
- Selecione um arquivo Excel (.xlsx)
- O sistema detecta imagens na coluna H
- Faz upload automático via SFTP

## 🔍 **TROUBLESHOOTING**

### **Problema: "Sem conexão SFTP"**
- **Causa:** Nenhuma das portas SFTP está acessível
- **Solução:** Verificar configurações de firewall/rede

### **Problema: "Arquivo sem imagens"**
- **Causa:** Arquivo Excel não tem imagens na coluna H
- **Solução:** Usar arquivo com imagens inseridas na coluna H

### **Problema: "Erro no upload"**
- **Causa:** Problema de permissões ou conectividade
- **Solução:** Verificar logs de debug no sistema

## 📊 **LOGS E DEBUG**

O sistema fornece logs detalhados:

- **Conectividade SFTP:** Testa cada porta automaticamente
- **Processamento Excel:** Mostra REFs e imagens encontradas
- **Upload:** Detalha cada etapa do upload
- **Erros:** Informações específicas sobre falhas

## 🎯 **VANTAGENS DO SISTEMA MELHORADO**

1. **Conectividade Robusta:** Testa múltiplas portas automaticamente
2. **Detecção Inteligente:** Identifica imagens na coluna H corretamente
3. **Interface Moderna:** Frontend responsivo e intuitivo
4. **Debug Completo:** Logs detalhados para troubleshooting
5. **Tratamento de Erros:** Mensagens claras sobre problemas
6. **Upload Confiável:** SFTP com timeout e retry automático

## 🔗 **URLS DO SISTEMA**

- **Frontend:** `https://moribrasil.pythonanywhere.com/`
- **Health Check:** `https://moribrasil.pythonanywhere.com/health`
- **Upload API:** `https://moribrasil.pythonanywhere.com/upload`

## 📞 **SUPORTE**

Para problemas ou dúvidas:
1. Verifique os logs de debug no sistema
2. Teste a conectividade SFTP manualmente
3. Confirme que o arquivo Excel tem imagens na coluna H
4. Verifique as configurações de rede/firewall
