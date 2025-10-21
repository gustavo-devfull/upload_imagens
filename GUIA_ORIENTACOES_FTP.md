# 🚀 SISTEMA FLASK SEGUINDO ORIENTAÇÕES FTP INICIAIS

## 📋 VISÃO GERAL

Sistema Flask que segue **exatamente** as orientações FTP iniciais do projeto, usando as mesmas credenciais, estrutura de diretórios e configurações já estabelecidas.

## 🔧 CONFIGURAÇÃO (JÁ PRONTA!)

### Credenciais FTP (Seguindo Orientações Iniciais)
```python
FTP_CONFIG = {
    'host': '46.202.90.62',
    'port': 21,
    'user': 'u715606397.ideolog.ia.br',
    'password': ']X9CC>t~ihWhdzNq',
    'upload_dir': 'public_html/images/products/',
    'timeout': 300
}
```

### URLs (Seguindo Orientações Iniciais)
```python
URLS_CONFIG = {
    'domain': 'https://ideolog.ia.br',
    'images_base': 'https://ideolog.ia.br/images/products/',
    'api_base': 'https://ideolog.ia.br/upload.php'
}
```

### Configuração Excel (Seguindo Orientações Iniciais)
- **Coluna REF**: A (códigos dos produtos)
- **Coluna PHOTO**: H (imagens)
- **Linha inicial**: 4
- **REFs inválidas**: TOTAL, SUBTOTAL, SUM, COUNT, etc.

## 🚀 COMO USAR

### 1. Iniciar Sistema
```bash
# Método 1: Script automático
./iniciar_orientacoes_ftp.sh

# Método 2: Manual
source venv/bin/activate
python sistema_flask_orientacoes_ftp.py
```

### 2. Acessar Interface
**URL:** http://localhost:8087

### 3. Processar Arquivo Excel
1. **Selecionar arquivo** (.xlsx)
2. **Clicar em "Processar e Enviar para FTP"**
3. **Aguardar processamento**
4. **Ver resultados com URLs**

## 📊 O QUE ACONTECE

### 1. Extração de Imagens
- ✅ Detecta imagens na coluna H
- ✅ Obtém REFs da coluna A
- ✅ Filtra REFs inválidas (TOTAL, SUBTOTAL, etc.)
- ✅ Extrai dados das imagens

### 2. Upload para FTP
- ✅ Conecta ao servidor FTP (46.202.90.62)
- ✅ Cria diretórios: `public_html/images/products/`
- ✅ Envia imagens com nome: `{REF}.jpg`
- ✅ Gera URLs: `https://ideolog.ia.br/images/products/{REF}.jpg`

### 3. Resultado
- ✅ Mostra estatísticas do upload
- ✅ Lista arquivos enviados com URLs
- ✅ Indica falhas (se houver)

## 📁 ESTRUTURA DOS ARQUIVOS ENVIADOS

### Nomenclatura (Seguindo Orientações Iniciais)
```
{REF}.jpg
```

### Exemplos
```
40.jpg    # REF: 40, Posição: H4
43.jpg    # REF: 43, Posição: H5
45.jpg    # REF: 45, Posição: H6
47.jpg    # REF: 47, Posição: H7
```

### URLs Geradas
```
https://ideolog.ia.br/images/products/40.jpg
https://ideolog.ia.br/images/products/43.jpg
https://ideolog.ia.br/images/products/45.jpg
https://ideolog.ia.br/images/products/47.jpg
```

## 🔍 ARQUIVOS DO SISTEMA

### Principais
- **`sistema_flask_orientacoes_ftp.py`** - Sistema principal Flask + FTP
- **`iniciar_orientacoes_ftp.sh`** - Script de inicialização automática

### Dependências (Já Existentes)
- **`detector_integrado.py`** - Detector de imagens
- **`detector_imagens_melhorado.py`** - Detector melhorado

## 📊 EXEMPLO DE USO

### Input (Excel)
```
Coluna A (REF) | Coluna H (Imagem)
40            | [imagem1.jpg]
43            | [imagem2.jpg]
45            | [imagem3.jpg]
47            | [imagem4.jpg]
```

### Output (FTP + URLs)
```
FTP: public_html/images/products/
├── 40.jpg (349 KB)
├── 43.jpg (169 KB)
├── 45.jpg (45 KB)
└── 47.jpg (169 KB)

URLs:
https://ideolog.ia.br/images/products/40.jpg
https://ideolog.ia.br/images/products/43.jpg
https://ideolog.ia.br/images/products/45.jpg
https://ideolog.ia.br/images/products/47.jpg
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

## 🎯 DIFERENÇAS DAS ORIENTAÇÕES INICIAIS

### ✅ SEGUINDO ORIENTAÇÕES:
- **Credenciais FTP**: Exatamente iguais
- **Estrutura diretórios**: `public_html/images/products/`
- **Nomenclatura**: `{REF}.jpg`
- **URLs**: `https://ideolog.ia.br/images/products/`
- **Configuração Excel**: Coluna A (REF), H (PHOTO), linha 4
- **REFs inválidas**: Filtra TOTAL, SUBTOTAL, etc.

### 🆕 MELHORIAS ADICIONADAS:
- **Interface web moderna**: React-like com drag & drop
- **Detecção robusta**: Usa detector integrado XML
- **Logs detalhados**: Monitoramento completo
- **Tratamento de erros**: Robusto e informativo
- **URLs clicáveis**: Links diretos para as imagens

## 🚨 SOLUÇÃO DE PROBLEMAS

### Erro de Conexão FTP
- ✅ Credenciais já configuradas corretamente
- ✅ Servidor FTP: 46.202.90.62
- ✅ Usuário: u715606397.ideolog.ia.br

### Nenhuma Imagem Encontrada
- ✅ Usa detector integrado robusto
- ✅ Suporta imagens embedadas
- ✅ Testado com `produtos_novos.xlsx`

### Upload Falha
- ✅ Cria diretórios automaticamente
- ✅ Timeout de 5 minutos
- ✅ Logs detalhados

## 📞 SUPORTE

Para problemas:
1. ✅ Verifique logs do sistema
2. ✅ Teste com arquivo Excel simples
3. ✅ Confirme estrutura da planilha
4. ✅ Acesse `/config` para diagnóstico

## 🎉 VANTAGENS

✅ **Seguindo orientações iniciais**: Configuração idêntica ao projeto original  
✅ **Interface moderna**: Web interface com drag & drop  
✅ **Detecção robusta**: Suporta imagens embedadas  
✅ **URLs diretas**: Links clicáveis para as imagens  
✅ **Logs detalhados**: Monitoramento completo  
✅ **Tratamento de erros**: Robusto e informativo  
✅ **Fácil uso**: Script de inicialização automática  

---

**Sistema pronto para usar seguindo exatamente as orientações FTP iniciais do projeto!** 🚀
