# Sistema de Upload de Imagens Excel

Sistema completo para processar arquivos Excel e fazer upload de imagens via FTP.

## 🚀 Funcionalidades

- ✅ Upload de arquivos Excel (.xlsx)
- ✅ Extração automática de imagens
- ✅ Upload via FTP para servidor remoto
- ✅ Interface web moderna
- ✅ API REST completa
- ✅ Deploy automático no Railway

## 📁 Estrutura do Projeto

- `server.py` - Servidor Flask principal
- `frontend.html` - Interface web
- `upload_ftp_corrigido.py` - Processador FTP
- `excel_image_extractor.py` - Extrator de imagens
- `requirements.txt` - Dependências Python
- `Procfile` - Configuração de deploy
- `railway.json` - Configuração Railway

## 🛠️ Tecnologias

- **Backend**: Python Flask
- **Frontend**: HTML/CSS/JavaScript
- **Deploy**: Railway
- **FTP**: Paramiko
- **Excel**: OpenPyXL

## 🌐 Deploy Online

Sistema configurado para deploy automático no Railway:
- Deploy contínuo via GitHub
- Variáveis de ambiente configuradas
- SSL automático
- Monitoramento de logs

## 📊 Estatísticas

- ✅ 45+ uploads processados com sucesso
- ✅ Sistema testado e funcionando
- ✅ Pronto para produção

## 🔧 Configuração

Configure as seguintes variáveis de ambiente:
- `FTP_HOST`
- `FTP_USER` 
- `FTP_PASSWORD`
- `FLASK_ENV=production`