# 🚀 GUIA DE DEPLOY NO RENDER

## 📋 **PASSOS PARA DEPLOY NO RENDER**

### **1. 🌐 ACESSAR RENDER**
1. Acesse: https://render.com
2. Faça login com sua conta GitHub
3. Clique em **"New +"** → **"Web Service"**

### **2. 🔗 CONECTAR REPOSITÓRIO**
1. **Connect a repository:** Selecione `gustavo-devfull/upload_imagens`
2. **Name:** `upload-imagens` (ou qualquer nome que preferir)
3. **Region:** Escolha a região mais próxima (US East ou US West)

### **3. ⚙️ CONFIGURAR BUILD E DEPLOY**
1. **Build Command:** `pip install -r requirements.txt`
2. **Start Command:** `python app.py`
3. **Python Version:** Deixe automático (detectará Python 3.x)

### **4. 🔧 CONFIGURAR VARIÁVEIS DE AMBIENTE**
No painel do Render, vá em **Environment** e adicione:

```
FTP_HOST=46.202.90.62
FTP_USER=u715606397.ideolog.ia.br
FTP_PASSWORD=]X9CC>t~ihWhdzNq
FLASK_ENV=production
```

### **5. 🚀 FAZER DEPLOY**
1. Clique em **"Create Web Service"**
2. Render fará o build automaticamente
3. Acompanhe os logs em tempo real
4. Aguarde o deploy completar

### **6. ✅ RESULTADO**
Sua aplicação ficará disponível em uma URL como:
`https://upload-imagens.onrender.com`

## 📊 **VANTAGENS DO RENDER**

- ✅ **Interface mais simples** que Railway
- ✅ **Deploy automático** via GitHub
- ✅ **SSL automático** incluído
- ✅ **Logs em tempo real**
- ✅ **Suporte nativo** a Python/Flask
- ✅ **Plano gratuito** robusto

## 🔧 **ARQUIVOS PREPARADOS**

- ✅ `app.py` - Servidor Flask minimal
- ✅ `requirements.txt` - Apenas Flask
- ✅ `render.yaml` - Configuração Render
- ✅ `README.md` - Documentação

## 🧪 **TESTAR APÓS DEPLOY**

1. **Health Check:** `https://sua-url.onrender.com/health`
2. **Página inicial:** `https://sua-url.onrender.com/`
3. **Configurações:** `https://sua-url.onrender.com/config`

## 🆘 **SUPORTE**

Se tiver problemas:
1. Verifique os logs no painel do Render
2. Confirme as variáveis de ambiente
3. Teste localmente primeiro
4. Verifique se o repositório está atualizado
