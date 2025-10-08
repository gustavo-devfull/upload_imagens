# 🚀 Sistema Upload Excel - Railway

Sistema para upload de imagens de planilhas Excel com detecção automática e upload para FTP.

## 📋 Funcionalidades

- ✅ **Detecção de imagens** na coluna H das planilhas Excel
- ✅ **Upload automático** para servidor FTP
- ✅ **Validação de arquivos** com sugestões
- ✅ **Logs detalhados** para debug
- ✅ **Interface responsiva** com barra de progresso
- ✅ **Deploy no Railway** otimizado

## 🔧 Tecnologias

- **Backend:** Python Flask
- **Processamento:** openpyxl
- **Upload:** ftplib
- **Deploy:** Railway
- **Frontend:** HTML/CSS/JavaScript

## 📊 Arquivos Suportados

- **Formato:** .xlsx (Excel)
- **Imagens:** Coluna H (PHOTO)
- **REFs:** Coluna A
- **Início:** Linha 4

## 🚀 Deploy no Railway

### 1. Conectar Repositório
1. Acesse [railway.app](https://railway.app)
2. Faça login na sua conta
3. Clique em "New Project"
4. Selecione "Deploy from GitHub repo"
5. Conecte o repositório: `gustavo-devfull/upload_imagens`

### 2. Configuração Automática
O Railway detectará automaticamente:
- ✅ **Python 3.11.9** (runtime.txt)
- ✅ **Dependências** (requirements_simples.txt)
- ✅ **Comando de start** (Procfile)
- ✅ **Health check** (/health)

### 3. Variáveis de Ambiente
O Railway configurará automaticamente:
- `PORT` - Porta do servidor (automática)
- `PYTHONUNBUFFERED=1` - Logs em tempo real

### 4. URLs após Deploy
- **Frontend:** `https://seu-app.railway.app/`
- **Health Check:** `https://seu-app.railway.app/health`
- **Config:** `https://seu-app.railway.app/config`
- **Upload API:** `https://seu-app.railway.app/upload`

## 📁 Estrutura do Projeto

```
├── sistema_flask_debug.py    # Sistema principal Flask
├── requirements_simples.txt  # Dependências Python
├── Procfile                  # Comando de start
├── runtime.txt              # Versão Python
├── railway.json             # Configuração Railway
├── tartaruga.xlsx           # Arquivo de teste (1 imagem)
├── carrinho.xlsx            # Arquivo de teste (2 imagens)
└── README_RAILWAY.md        # Este arquivo
```

## 🧪 Teste

### Arquivos de Teste
- **tartaruga.xlsx** - 1 REF, 1 imagem ✅
- **carrinho.xlsx** - 2 REFs, 2 imagens ✅
- **cotacao.xlsx** - 4 REFs, 0 imagens ❌

### Como Testar
1. Acesse a URL do seu app Railway
2. Selecione um arquivo Excel (.xlsx)
3. Clique em "Fazer Upload"
4. Verifique as informações de debug
5. Confirme o upload no FTP

## 🔍 Debug

O sistema inclui logs detalhados:
- Total de imagens encontradas
- Posição de cada imagem (linha/coluna)
- REFs processadas
- Processo de upload FTP
- Erros detalhados

## 📊 Configuração FTP

```python
FTP_HOST = "46.202.90.62"
FTP_USER = "u715606397.ideolog.ia.br"
FTP_PASS = "]X9CC>t~ihWhdzNq"
FTP_DIR = "public_html/images/products"
```

## 🚨 Troubleshooting

### Problemas Comuns
1. **Imagens não detectadas:** Verifique se estão na coluna H
2. **Upload falha:** Verifique conexão FTP
3. **Arquivo inválido:** Use apenas .xlsx com imagens

### Logs
- Acesse o dashboard do Railway
- Verifique os logs em tempo real
- Use as informações de debug no frontend

## 📈 Monitoramento

- **Health Check:** `/health`
- **Configuração:** `/config`
- **Logs:** Dashboard Railway
- **Métricas:** CPU, memória, requests

## 🎯 Próximos Passos

1. ✅ Deploy no Railway
2. 🔄 Teste com arquivos de exemplo
3. 📊 Verifique logs de debug
4. 🚀 Sistema pronto para produção

---

**Sistema otimizado para Railway com logs detalhados e interface responsiva!** 🚀
