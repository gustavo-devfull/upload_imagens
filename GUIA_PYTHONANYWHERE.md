# 🚀 Sistema Upload Excel - Deploy PythonAnywhere

Sistema para upload de imagens de planilhas Excel com detecção automática e upload para FTP, otimizado para PythonAnywhere.

## 📋 Funcionalidades

- ✅ **Detecção de imagens** na coluna H das planilhas Excel
- ✅ **Upload automático** para servidor FTP
- ✅ **Validação de arquivos** com sugestões
- ✅ **Interface responsiva** com feedback visual
- ✅ **Deploy no PythonAnywhere** otimizado
- ✅ **Logs detalhados** para debug

## 🔧 Tecnologias

- **Backend:** Python Flask
- **Processamento:** openpyxl
- **Upload:** ftplib
- **Deploy:** PythonAnywhere
- **Frontend:** HTML/CSS/JavaScript

## 📊 Arquivos Suportados

- **Formato:** .xlsx (Excel)
- **Imagens:** Coluna H (PHOTO)
- **REFs:** Coluna A
- **Início:** Linha 4

## 🚀 Deploy no PythonAnywhere

### 1. Preparação

**1.1 Criar Conta PythonAnywhere:**
- Acesse [pythonanywhere.com](https://pythonanywhere.com)
- Crie uma conta gratuita ou paga
- Acesse o dashboard

**1.2 Preparar Arquivos:**
- `sistema_pythonanywhere.py` - Sistema principal
- `wsgi.py` - Configuração WSGI
- `install_pythonanywhere.sh` - Script de instalação

### 2. Instalação

**2.1 Via Console PythonAnywhere:**
```bash
# Execute no console do PythonAnywhere
bash install_pythonanywhere.sh
```

**2.2 Instalação Manual:**
```bash
# Instalar dependências
pip3.10 install --user flask openpyxl

# Criar diretório
mkdir -p ~/sistema_upload_excel
cd ~/sistema_upload_excel

# Baixar arquivos (substitua pelo seu repositório)
wget https://raw.githubusercontent.com/gustavo-devfull/upload_imagens/main/sistema_pythonanywhere.py
wget https://raw.githubusercontent.com/gustavo-devfull/upload_imagens/main/wsgi.py

# Configurar permissões
chmod +x wsgi.py
```

### 3. Configuração Web App

**3.1 Criar Web App:**
1. No dashboard PythonAnywhere, vá em **"Web"**
2. Clique em **"Add a new web app"**
3. Escolha **"Manual configuration"**
4. Selecione **Python 3.10**

**3.2 Configurar WSGI:**
1. Clique em **"WSGI configuration file"**
2. Substitua o conteúdo por:
```python
#!/usr/bin/env python3
import sys
import os

path = '/home/seu_usuario/sistema_upload_excel'
if path not in sys.path:
    sys.path.append(path)

from sistema_pythonanywhere import app

if __name__ == "__main__":
    app.run()
```

**3.3 Configurar Source Code:**
1. Vá em **"Source code"**
2. Configure o diretório: `/home/seu_usuario/sistema_upload_excel`

### 4. Configuração de Domínio

**4.1 Domínio Padrão:**
- `https://seu_usuario.pythonanywhere.com/`

**4.2 Domínio Personalizado (Pago):**
- Configure DNS para apontar para PythonAnywhere
- Adicione domínio nas configurações

### 5. URLs do Sistema

Após deploy bem-sucedido:
- **Frontend:** `https://seu_usuario.pythonanywhere.com/`
- **Health Check:** `https://seu_usuario.pythonanywhere.com/health`
- **Upload API:** `https://seu_usuario.pythonanywhere.com/upload`

## 🧪 Teste

### Arquivos de Teste
- **tartaruga.xlsx** - 1 REF, 1 imagem ✅
- **carrinho.xlsx** - 2 REFs, 2 imagens ✅
- **cotacao.xlsx** - 4 REFs, 0 imagens ❌

### Como Testar
1. Acesse a URL do seu app PythonAnywhere
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
4. **Erro WSGI:** Verifique path e permissões

### Logs
- Acesse o console do PythonAnywhere
- Verifique logs em tempo real
- Use as informações de debug no frontend

## 📈 Monitoramento

- **Health Check:** `/health`
- **Logs:** Console PythonAnywhere
- **Métricas:** Dashboard PythonAnywhere
- **Uptime:** Monitoramento automático

## 🎯 Vantagens PythonAnywhere

- ✅ **Simplicidade:** Deploy fácil e rápido
- ✅ **Confiabilidade:** Servidor estável
- ✅ **Suporte:** Documentação completa
- ✅ **Escalabilidade:** Planos flexíveis
- ✅ **Domínio:** Personalizado disponível

## 🔄 Atualizações

Para atualizar o sistema:
1. Faça upload da nova versão
2. Reinicie o web app
3. Teste as funcionalidades

---

**Sistema otimizado para PythonAnywhere com interface responsiva e logs detalhados!** 🚀
