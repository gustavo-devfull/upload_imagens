# 🚀 Sistema de Upload de Imagens Excel

Sistema completo para extrair imagens de planilhas Excel e fazer upload para servidor FTP, com interface web moderna e API REST.

## ✨ Funcionalidades

- 📊 **Upload de arquivos Excel** (.xlsx)
- 🖼️ **Extração automática de imagens** da coluna H
- 🌐 **Interface web moderna** com React
- 🔧 **API REST completa** para integração
- 📡 **Upload FTP automático** para servidor remoto
- 🛡️ **Tratamento de erros** robusto
- 📝 **Logging detalhado** para debug

## 🎯 Versões Disponíveis

### 🌐 Versão Online (Render)
- **URL:** https://upload-imagens.onrender.com
- **Status:** ✅ Funcionando
- **Versão:** Simplificada (sem dependências complexas)
- **Funcionalidades:** Upload, análise e processamento básico

### 💻 Versão Local Completa
- **Arquivo:** `server.py`
- **Funcionalidades:** Sistema completo com FTP
- **Dependências:** Flask, openpyxl, Pillow, paramiko

### 🔧 Versão Simplificada (Render)
- **Arquivo:** `app_simple_render.py`
- **Funcionalidades:** Processamento básico sem FTP
- **Dependências:** Flask, openpyxl apenas

## 📋 Estrutura do Projeto

```
upload/
├── 🌐 Frontend
│   ├── frontend.html          # Interface web React
│   └── index.html            # Página inicial
├── 🚀 Backend
│   ├── server.py             # Sistema completo local
│   ├── app_simple_render.py  # Versão simplificada Render
│   ├── wsgi.py               # Entry point WSGI
│   └── upload_ftp_corrigido.py # Módulo FTP
├── ⚙️ Configuração
│   ├── requirements.txt      # Dependências Python
│   ├── Procfile             # Comando de start Render
│   ├── render.yaml          # Configuração Render
│   └── runtime.txt          # Versão Python
├── 🧪 Testes
│   ├── test_tartaruga.py    # Análise de arquivos Excel
│   └── iniciar_sistema.py   # Script de inicialização
└── 📚 Documentação
    ├── README.md            # Este arquivo
    ├── RENDER_DEPLOY_GUIDE.md # Guia de deploy
    └── DEPLOY_GUIDE.md      # Guia geral
```

## 🚀 Como Usar

### 🌐 Versão Online (Recomendado)
1. **Acesse:** https://upload-imagens.onrender.com
2. **Faça upload** do arquivo Excel (.xlsx)
3. **Aguarde processamento** automático
4. **Visualize resultados** na interface

### 💻 Versão Local
1. **Clone o repositório:**
   ```bash
   git clone https://github.com/gustavo-devfull/upload_imagens.git
   cd upload_imagens
   ```

2. **Instale dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o sistema:**
   ```bash
   python server.py
   ```

4. **Acesse:** http://localhost:8080

## 🔧 Configuração

### 📡 Variáveis de Ambiente
```bash
FTP_HOST=46.202.90.62
FTP_USER=u715606397.ideolog.ia.br
FTP_PASSWORD=]X9CC>t~ihWhdzNq
FLASK_ENV=production
```

### 📊 Formato do Excel
- **Coluna A:** REF (referência do produto) - **SJ0001, SJ0002, etc.**
- **Coluna H:** Imagens embutidas diretamente nas células
- **Início:** Linha 4 (linhas 1-3 são cabeçalhos)
- **Detecção:** Automática de REFs válidos (contém letras)

## 🛠️ API Endpoints

### 📡 Endpoints Principais
- **`GET /`** - Interface web
- **`GET /health`** - Status do servidor
- **`GET /config`** - Configurações do sistema
- **`POST /upload`** - Upload de arquivos Excel

### 📊 Exemplo de Resposta
```json
{
  "success": true,
  "total_refs": 2,
  "images_found": 1,
  "uploads_successful": 1,
  "uploads_failed": 0,
  "errors": [],
  "images": [
    {
      "name": "Imagem processada",
      "url": "https://ideolog.ia.br/images/products/"
    }
  ]
}
```

## 🔍 Debugging

### 🧪 Análise de Arquivos Excel
```bash
python test_tartaruga.py
```

### 📝 Logs Detalhados
O sistema gera logs detalhados para debug:
- Total de imagens na planilha
- Posição de cada imagem
- Processamento linha por linha
- Status de cada REF processada

## 🚀 Deploy

### 🌐 Render (Atual)
- **Status:** ✅ Deploy automático ativo
- **URL:** https://upload-imagens.onrender.com
- **Branch:** main
- **Build:** Automático via GitHub

### 🚂 Railway (Alternativo)
- Configuração disponível em `railway.json`
- Comandos em `Procfile`

## 📊 Status do Sistema

### ✅ Funcionando
- ✅ Upload de arquivos Excel
- ✅ Detecção de imagens inseridas
- ✅ Processamento básico
- ✅ Interface web
- ✅ API REST
- ✅ Health checks

### ⚠️ Limitado (Versão Online)
- ⚠️ Upload FTP (versão simplificada)
- ⚠️ Processamento de imagens (sem Pillow)

### 🔧 Em Desenvolvimento
- 🔧 Upload FTP completo
- 🔧 Processamento avançado de imagens
- 🔧 Interface melhorada

## 🤝 Contribuição

1. **Fork** o repositório
2. **Crie** uma branch para sua feature
3. **Commit** suas mudanças
4. **Push** para a branch
5. **Abra** um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

**Gustavo Santos**
- GitHub: [@gustavo-devfull](https://github.com/gustavo-devfull)
- Projeto: Sistema de Upload de Imagens Excel

## 📞 Suporte

Para suporte ou dúvidas:
- **Issues:** [GitHub Issues](https://github.com/gustavo-devfull/upload_imagens/issues)
- **Email:** [Seu email]
- **Documentação:** Veja os arquivos `.md` no projeto

---

**🎉 Sistema funcionando online em:** https://upload-imagens.onrender.com