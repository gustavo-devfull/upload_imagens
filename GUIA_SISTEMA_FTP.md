# 🚀 GUIA COMPLETO: SISTEMA EXCEL → FTP

## 📋 VISÃO GERAL

Este sistema permite extrair imagens de arquivos Excel e enviá-las diretamente para um servidor FTP, mantendo a associação com as REFs e posições das células.

## 🔧 CONFIGURAÇÃO INICIAL

### 1. Configurar Dados FTP

Execute o configurador para testar e configurar sua conexão FTP:

```bash
python configurador_ftp.py
```

Ou teste diretamente:

```bash
python configurador_ftp.py test seu-servidor.com usuario senha /uploads/
```

### 2. Editar Configuração FTP

No arquivo `sistema_flask_ftp.py`, edite a seção `FTP_CONFIG`:

```python
FTP_CONFIG = {
    'host': 'seu-servidor-ftp.com',
    'user': 'seu-usuario',
    'password': 'sua-senha',
    'directory': '/uploads/'
}
```

## 🚀 COMO USAR

### 1. Iniciar o Sistema

```bash
source venv/bin/activate
python sistema_flask_ftp.py
```

### 2. Acessar Interface Web

Abra seu navegador em: **http://localhost:8086**

### 3. Processar Arquivo Excel

1. **Clique em "📁 Selecionar Arquivo"**
2. **Escolha um arquivo .xlsx** (ex: `produtos_novos.xlsx`)
3. **Clique em "🚀 Processar e Enviar para FTP"**
4. **Aguarde o processamento**

## 📊 O QUE ACONTECE

### 1. Extração de Imagens
- ✅ Detecta imagens na coluna H
- ✅ Obtém REFs da coluna A
- ✅ Extrai dados das imagens do arquivo Excel

### 2. Upload para FTP
- ✅ Conecta ao servidor FTP
- ✅ Envia cada imagem com nome único
- ✅ Mantém associação REF → Imagem

### 3. Resultado
- ✅ Mostra estatísticas do upload
- ✅ Lista arquivos enviados com sucesso
- ✅ Indica falhas (se houver)

## 📁 ESTRUTURA DOS ARQUIVOS ENVIADOS

### Nomenclatura
```
{REF}_{nome_original}.jpg
```

### Exemplos
```
40_image1.jpg    # REF: 40, Posição: H4
43_image2.jpg    # REF: 43, Posição: H5
45_image3.jpg    # REF: 45, Posição: H6
47_image4.jpg    # REF: 47, Posição: H7
```

## 🔍 ARQUIVOS DO SISTEMA

### Principais
- **`sistema_flask_ftp.py`** - Sistema principal Flask + FTP
- **`sistema_excel_para_ftp.py`** - Script standalone para uso direto
- **`configurador_ftp.py`** - Configurador e testador FTP

### Dependências
- **`detector_integrado.py`** - Detector de imagens (já existente)
- **`detector_imagens_melhorado.py`** - Detector melhorado (já existente)

## 📊 EXEMPLO DE USO

### Input (Excel)
```
Coluna A (REF) | Coluna H (Imagem)
40            | [imagem1.jpg]
43            | [imagem2.jpg]
45            | [imagem3.jpg]
47            | [imagem4.jpg]
```

### Output (FTP)
```
/uploads/
├── 40_image1.jpg (349 KB)
├── 43_image2.jpg (169 KB)
├── 45_image3.jpg (45 KB)
└── 47_image4.jpg (169 KB)
```

## 🛠️ USO PROGRAMÁTICO

### Script Standalone

```python
from sistema_excel_para_ftp import SistemaExcelParaFTP

# Configurar sistema
sistema = SistemaExcelParaFTP(
    ftp_host="seu-servidor.com",
    ftp_user="usuario",
    ftp_pass="senha",
    ftp_dir="/uploads/"
)

# Processar arquivo
resultado = sistema.processar_arquivo_completo("produtos_novos.xlsx")

if resultado['success']:
    print(f"✅ {resultado['upload_stats']['successful_uploads']} imagens enviadas!")
else:
    print(f"❌ Erro: {resultado['error']}")
```

## 🔧 ENDPOINTS DA API

### Upload
```
POST /upload
Content-Type: multipart/form-data
Body: file (arquivo .xlsx)
```

### Health Check
```
GET /health
```

### Configuração
```
GET /config
```

## 📈 MONITORAMENTO

### Logs do Sistema
- ✅ Conexão FTP
- ✅ Extração de imagens
- ✅ Upload de arquivos
- ✅ Estatísticas finais

### Interface Web
- ✅ Status em tempo real
- ✅ Estatísticas visuais
- ✅ Lista de arquivos enviados
- ✅ Indicação de erros

## 🚨 SOLUÇÃO DE PROBLEMAS

### Erro de Conexão FTP
1. Verifique host, usuário e senha
2. Teste com `configurador_ftp.py`
3. Verifique firewall/proxy

### Nenhuma Imagem Encontrada
1. Verifique se há imagens na coluna H
2. Confirme se há REFs na coluna A
3. Teste com arquivo conhecido (`produtos_novos.xlsx`)

### Upload Falha
1. Verifique permissões do diretório FTP
2. Confirme espaço em disco
3. Verifique logs do servidor FTP

## 📞 SUPORTE

Para problemas ou dúvidas:
1. Verifique os logs do sistema
2. Teste conexão FTP com configurador
3. Confirme configurações

## 🎯 RESUMO

✅ **Sistema completo funcionando**
✅ **Interface web amigável**
✅ **Upload direto para FTP**
✅ **Associação REF → Imagem**
✅ **Monitoramento em tempo real**
✅ **Configuração fácil**

**Pronto para usar! Configure o FTP e comece a processar seus arquivos Excel!** 🚀

