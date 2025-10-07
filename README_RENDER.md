# 🚀 Sistema de Upload de Imagens Excel - Deploy Render

## 📋 Descrição
Sistema profissional para extrair imagens de planilhas Excel e fazer upload via FTP com barra de progresso avançada.

## ✨ Funcionalidades
- ✅ **Barra de progresso avançada** com 5 passos visuais
- ✅ **Cronômetro em tempo real** (MM:SS)
- ✅ **Detecção automática** de arquivos sem imagens
- ✅ **Upload FTP** para servidor remoto
- ✅ **Interface responsiva** e moderna
- ✅ **Validação inteligente** de arquivos

## 🎯 Deploy no Render.com

### 1. Conectar Repositório
1. Acesse [Render.com](https://render.com)
2. Conecte seu repositório GitHub
3. Selecione este projeto

### 2. Configuração Automática
O arquivo `render.yaml` já está configurado:
```yaml
services:
  - type: web
    name: sistema-upload-excel-render
    env: python
    pythonVersion: 3.11.9
    buildCommand: pip install --upgrade pip && pip install -r requirements_simples.txt
    startCommand: python sistema_simples.py
    envVars:
      - key: PORT
        value: 8080
      - key: PYTHONUNBUFFERED
        value: 1
    healthCheckPath: /health
    plan: starter
```

### 3. Deploy
1. Clique em "Deploy"
2. Aguarde o build (2-3 minutos)
3. Acesse a URL fornecida

## 📊 Arquivos de Deploy

| Arquivo | Descrição |
|---------|-----------|
| `sistema_simples.py` | Sistema principal (sem PIL) |
| `requirements_simples.txt` | Dependências mínimas |
| `render.yaml` | Configuração do Render |
| `Procfile` | Compatibilidade Heroku |
| `runtime.txt` | Versão Python |

## 🔧 Dependências Simplificadas
```
Flask==3.0.0
Werkzeug==3.0.1
openpyxl==3.1.2
requests==2.31.0
```

## 🎨 Interface
- **Barra de progresso** com animação shimmer
- **5 passos visuais** numerados
- **Cronômetro** em tempo real
- **Status detalhado** de cada etapa
- **Design responsivo** para mobile

## 📱 Como Usar
1. **Acesse** a URL do Render
2. **Selecione** arquivo Excel (.xlsx)
3. **Observe** a barra de progresso
4. **Aguarde** o processamento
5. **Veja** os resultados

## 🎯 Arquivos Recomendados
- ✅ `tartaruga.xlsx` (1 imagem)
- ✅ `carrinho.xlsx` (2 imagens)
- ❌ `cotacao.xlsx` (sem imagens)

## 🌐 URLs das Imagens
Após o upload, as imagens ficam disponíveis em:
```
https://ideolog.ia.br/images/products/[REF].jpg
```

## 🔍 Health Check
O sistema possui endpoint de health check:
```
GET /health
```

## 📈 Monitoramento
- **Logs em tempo real** no Render
- **Métricas de performance**
- **Status de saúde** automático

## 🚀 Vantagens do Deploy
- ✅ **Sem configuração** de servidor
- ✅ **Escalabilidade** automática
- ✅ **SSL** incluído
- ✅ **CDN** global
- ✅ **Backup** automático

## 🎊 Resultado Final
Sistema profissional funcionando na nuvem com:
- Interface moderna e responsiva
- Barra de progresso avançada
- Upload FTP automático
- Validação inteligente de arquivos
- Monitoramento completo
