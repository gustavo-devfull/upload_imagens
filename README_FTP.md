# 🖼️ Sistema de Upload de Imagens Excel - Versão FTP

Sistema completo para extrair imagens de planilhas Excel e fazer upload para servidor FTP, rodando diretamente no servidor web.

## 🚀 Características

- **Frontend React**: Interface moderna e responsiva
- **Backend PHP**: Processamento no servidor FTP
- **Upload FTP**: Integração nativa com servidor FTP
- **Filtros Inteligentes**: Ignora REFs inválidas automaticamente
- **Progress Bar**: Acompanhamento visual em tempo real
- **URLs Diretas**: Links diretos para as imagens processadas

## 📋 Pré-requisitos

- Servidor web com PHP 7.4+
- Extensão FTP habilitada no PHP
- Acesso FTP ao servidor
- Navegador moderno

## 🛠️ Instalação Automática

### Método 1: Script Python (Recomendado)
```bash
python3 instalar_ftp.py
```

### Método 2: Upload Manual
1. Faça upload dos arquivos para `public_html/`:
   - `index.html`
   - `upload.php`
   - `config.php`

2. Configure as credenciais FTP no `upload.php`

3. Acesse: `https://seudominio.com/`

## 📁 Arquivos do Sistema

```
public_html/
├── index.html              # Interface React
├── upload.php              # Processador de uploads
├── config.php              # Configurações do sistema
└── images/products/        # Diretório das imagens (criado automaticamente)
```

## ⚙️ Configuração

### Credenciais FTP (upload.php)
```php
define('FTP_HOST', '46.202.90.62');
define('FTP_PORT', 21);
define('FTP_USER', 'u715606397.ideolog.ia.br');
define('FTP_PASS', ']X9CC>t~ihWhdzNq');
```

### Configurações da Planilha
- **Coluna REF**: A (códigos dos produtos)
- **Coluna PHOTO**: H (imagens)
- **Linha inicial**: 4
- **Formato**: .xlsx

## 🌐 Uso do Sistema

1. **Acesse**: `https://ideolog.ia.br/`
2. **Arraste** arquivo Excel (.xlsx) para a área de upload
3. **Clique** em "Fazer Upload"
4. **Acompanhe** o progresso em tempo real
5. **Veja** os resultados com URLs das imagens
6. **Copie** as URLs para usar em outros sistemas

## 🔧 API Endpoints

- `GET /` - Interface principal
- `POST /upload.php` - Upload de arquivo Excel
- `GET /config.php` - Configurações e status do sistema

## 📊 Exemplo de Resposta

```json
{
  "total_refs": 3,
  "images_found": 3,
  "uploads_successful": 3,
  "uploads_failed": 0,
  "images": [
    {
      "name": "CHDJ25001.jpg",
      "url": "https://ideolog.ia.br/images/products/CHDJ25001.jpg"
    }
  ],
  "errors": []
}
```

## 🎨 URLs Geradas

```
https://ideolog.ia.br/images/products/CHDJ25001.jpg
https://ideolog.ia.br/images/products/T608.jpg
https://ideolog.ia.br/images/products/106-6S.jpg
```

## 🚨 Solução de Problemas

### Erro: "Conexão FTP falhou"
- Verifique credenciais FTP no `upload.php`
- Teste conexão: `https://ideolog.ia.br/config.php`

### Erro: "Arquivo muito grande"
- Limite: 50MB por arquivo
- Ajuste `upload_max_filesize` no PHP

### Erro: "Extensão não permitida"
- Apenas arquivos .xlsx são aceitos
- Verifique extensão do arquivo

### Erro: "Diretório não encontrado"
- Sistema cria diretórios automaticamente
- Verifique permissões FTP

## 🔒 Segurança

- Validação de extensões de arquivo
- Limite de tamanho de arquivo
- Sanitização de nomes de arquivo
- Headers CORS configurados
- Logs de erro detalhados

## 📈 Performance

- **Upload**: ~2-5 segundos por imagem
- **Processamento**: ~1-3 segundos por REF
- **Limite**: 50MB por arquivo
- **Timeout**: 5 minutos por upload

## 🧪 Teste do Sistema

### Health Check
```bash
curl https://ideolog.ia.br/config.php
```

### Teste de Upload
```bash
curl -X POST -F "excel_file=@arquivo.xlsx" https://ideolog.ia.br/upload.php
```

## 🔄 Atualizações

Para atualizar o sistema:

1. Faça backup dos arquivos atuais
2. Faça upload das novas versões
3. Teste o sistema
4. Verifique logs de erro

## 📱 Responsividade

- **Desktop**: Interface completa
- **Tablet**: Layout adaptado
- **Mobile**: Interface otimizada
- **Touch**: Suporte a drag & drop

## 🎯 Funcionalidades Avançadas

- **Drag & Drop**: Arraste arquivos diretamente
- **Progress Bar**: Acompanhamento visual
- **Copy to Clipboard**: Copie URLs com um clique
- **Error Handling**: Tratamento robusto de erros
- **Auto-refresh**: Interface atualiza automaticamente
- **CORS**: Suporte a requisições cross-origin

## 🆘 Suporte

Para problemas:

1. Verifique logs de erro do PHP
2. Teste com arquivo Excel simples
3. Verifique conectividade FTP
4. Confirme estrutura da planilha
5. Acesse `/config.php` para diagnóstico

## 🎉 Vantagens da Versão FTP

✅ **Sem dependências externas**: Roda no servidor web  
✅ **Instalação simples**: Apenas upload de arquivos  
✅ **Manutenção fácil**: Arquivos PHP padrão  
✅ **Escalabilidade**: Suporta múltiplos usuários  
✅ **Segurança**: Processamento no servidor  
✅ **Performance**: Sem latência de rede  

---

**Desenvolvido para funcionar diretamente no servidor FTP** 🚀


