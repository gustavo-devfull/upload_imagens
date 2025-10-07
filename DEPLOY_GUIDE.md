# 🚀 GUIA DE DEPLOY ONLINE - Sistema Excel Upload

## 📋 **ARQUIVOS PREPARADOS PARA DEPLOY**

✅ **requirements.txt** - Dependências Python
✅ **Procfile** - Comando de inicialização (Heroku/Railway)
✅ **runtime.txt** - Versão do Python
✅ **railway.json** - Configuração Railway
✅ **render.yaml** - Configuração Render
✅ **server.py** - Atualizado com variáveis de ambiente

## 🌟 **PLATAFORMAS RECOMENDADAS**

### **1. RAILWAY (MAIS FÁCIL)**
1. Acesse: https://railway.app
2. Faça login com GitHub
3. Clique em "New Project" → "Deploy from GitHub repo"
4. Selecione seu repositório
5. Configure as variáveis de ambiente:
   - `FTP_HOST` = 46.202.90.62
   - `FTP_USER` = u715606397.ideolog.ia.br
   - `FTP_PASSWORD` = ]X9CC>t~ihWhdzNq
   - `FLASK_ENV` = production
6. Deploy automático! 🎉

### **2. RENDER**
1. Acesse: https://render.com
2. Faça login com GitHub
3. Clique em "New" → "Web Service"
4. Conecte seu repositório
5. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn server:app --bind 0.0.0.0:$PORT`
6. Adicione as variáveis de ambiente (mesmas do Railway)
7. Deploy! 🚀

### **3. PYTHONANYWHERE**
1. Acesse: https://pythonanywhere.com
2. Crie conta gratuita
3. Vá em "Web" → "Add a new web app"
4. Escolha "Flask" e Python 3.11
5. Faça upload dos arquivos via Files
6. Configure as variáveis de ambiente
7. Reload da aplicação

## 🔧 **VARIÁVEIS DE AMBIENTE NECESSÁRIAS**

```
FTP_HOST=46.202.90.62
FTP_USER=u715606397.ideolog.ia.br
FTP_PASSWORD=]X9CC>t~ihWhdzNq
FLASK_ENV=production
```

## 📁 **ARQUIVOS QUE DEVEM ESTAR NO REPOSITÓRIO**

- ✅ server.py
- ✅ frontend.html
- ✅ upload_ftp_corrigido.py
- ✅ excel_image_extractor.py
- ✅ requirements.txt
- ✅ Procfile
- ✅ runtime.txt
- ✅ railway.json (opcional)
- ✅ render.yaml (opcional)

## 🎯 **PRÓXIMOS PASSOS**

1. **Criar repositório GitHub** com todos os arquivos
2. **Escolher plataforma** (Railway recomendado)
3. **Configurar variáveis de ambiente**
4. **Fazer deploy**
5. **Testar a aplicação online**

## 💡 **DICAS IMPORTANTES**

- 🔒 **Nunca commite senhas** no código (use variáveis de ambiente)
- 📊 **Monitore logs** para debug
- 🔄 **Deploy automático** funciona com push no GitHub
- 💾 **Backup** das configurações FTP
- 🌐 **URL será gerada** automaticamente pela plataforma

## 🆘 **SUPORTE**

Se tiver problemas:
1. Verifique logs da plataforma
2. Confirme variáveis de ambiente
3. Teste localmente primeiro
4. Verifique dependências no requirements.txt
