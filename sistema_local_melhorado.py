#!/usr/bin/env python3
"""
🚀 SISTEMA LOCAL MELHORADO - Upload de Imagens Excel
Script para rodar o sistema localmente com detecção melhorada de imagens
"""

import os
import sys
import webbrowser
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import tempfile
import logging

# Importa o sistema melhorado
try:
    from sistema_melhorado import SistemaExcelMelhorado
    SISTEMA_MELHORADO_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Sistema melhorado não disponível: {e}")
    SISTEMA_MELHORADO_AVAILABLE = False

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SistemaLocalHandler(BaseHTTPRequestHandler):
    """Handler para o servidor local"""
    
    def do_GET(self):
        """Trata requisições GET"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.serve_frontend()
        elif parsed_path.path == '/health':
            self.health_check()
        elif parsed_path.path == '/config':
            self.get_config()
        else:
            self.send_error(404, "Página não encontrada")
    
    def do_POST(self):
        """Trata requisições POST"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/upload':
            self.handle_upload()
        else:
            self.send_error(404, "Endpoint não encontrado")
    
    def serve_frontend(self):
        """Serve o frontend HTML"""
        try:
            html_content = self.get_frontend_html()
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
        except Exception as e:
            logger.error(f"Erro ao servir frontend: {e}")
            self.send_error(500, f"Erro interno: {e}")
    
    def get_frontend_html(self):
        """Retorna o HTML do frontend"""
        return """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Sistema de Upload Excel - Melhorado</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            padding: 40px;
            max-width: 600px;
            width: 100%;
            text-align: center;
        }
        
        .header {
            margin-bottom: 30px;
        }
        
        .header h1 {
            color: #333;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            color: #666;
            font-size: 1.1em;
        }
        
        .upload-area {
            border: 3px dashed #667eea;
            border-radius: 15px;
            padding: 40px;
            margin: 30px 0;
            background: #f8f9ff;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .upload-area:hover {
            border-color: #764ba2;
            background: #f0f2ff;
        }
        
        .upload-area.dragover {
            border-color: #4CAF50;
            background: #e8f5e8;
        }
        
        .upload-icon {
            font-size: 3em;
            color: #667eea;
            margin-bottom: 20px;
        }
        
        .file-input {
            display: none;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 25px;
            font-size: 1.1em;
            cursor: pointer;
            transition: all 0.3s ease;
            margin: 10px;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }
        
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .progress {
            margin: 20px 0;
            display: none;
        }
        
        .progress-bar {
            width: 100%;
            height: 20px;
            background: #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #4CAF50, #45a049);
            width: 0%;
            transition: width 0.3s ease;
        }
        
        .result {
            margin: 20px 0;
            padding: 20px;
            border-radius: 10px;
            display: none;
        }
        
        .result.success {
            background: #e8f5e8;
            border: 1px solid #4CAF50;
            color: #2e7d32;
        }
        
        .result.error {
            background: #ffebee;
            border: 1px solid #f44336;
            color: #c62828;
        }
        
        .file-info {
            margin: 20px 0;
            padding: 15px;
            background: #f5f5f5;
            border-radius: 10px;
            display: none;
        }
        
        .recommendations {
            margin: 20px 0;
            padding: 15px;
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 10px;
            text-align: left;
        }
        
        .recommendations h4 {
            color: #856404;
            margin-bottom: 10px;
        }
        
        .recommendations ul {
            color: #856404;
            margin-left: 20px;
        }
        
        .status {
            margin: 10px 0;
            font-weight: bold;
        }
        
        .status.success { color: #4CAF50; }
        .status.error { color: #f44336; }
        .status.info { color: #2196F3; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Sistema Excel Melhorado</h1>
            <p>Upload de imagens com detecção avançada</p>
        </div>
        
        <div class="upload-area" id="uploadArea">
            <div class="upload-icon">📁</div>
            <h3>Arraste seu arquivo Excel aqui</h3>
            <p>ou clique para selecionar</p>
            <input type="file" id="fileInput" class="file-input" accept=".xlsx">
            <br><br>
            <button class="btn" onclick="document.getElementById('fileInput').click()">
                📂 Selecionar Arquivo
            </button>
        </div>
        
        <div class="file-info" id="fileInfo">
            <h4>📄 Arquivo Selecionado:</h4>
            <p id="fileName"></p>
            <p id="fileSize"></p>
        </div>
        
        <div class="recommendations">
            <h4>💡 Arquivos Recomendados:</h4>
            <ul>
                <li><strong>fabrica_com_imagens.xlsx</strong> - 4 imagens</li>
                <li><strong>tartaruga.xlsx</strong> - 1 imagem</li>
                <li><strong>carrinho.xlsx</strong> - 2 imagens</li>
            </ul>
        </div>
        
        <button class="btn" id="uploadBtn" onclick="uploadFile()" disabled>
            🚀 Fazer Upload
        </button>
        
        <div class="progress" id="progress">
            <div class="progress-bar">
                <div class="progress-fill" id="progressFill"></div>
            </div>
            <div class="status info" id="progressText">Preparando...</div>
        </div>
        
        <div class="result" id="result">
            <div id="resultContent"></div>
        </div>
    </div>

    <script>
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const uploadBtn = document.getElementById('uploadBtn');
        const fileInfo = document.getElementById('fileInfo');
        const fileName = document.getElementById('fileName');
        const fileSize = document.getElementById('fileSize');
        const progress = document.getElementById('progress');
        const progressFill = document.getElementById('progressFill');
        const progressText = document.getElementById('progressText');
        const result = document.getElementById('result');
        const resultContent = document.getElementById('resultContent');
        
        let selectedFile = null;
        
        // Drag and drop
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                handleFileSelect(files[0]);
            }
        });
        
        // File input
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleFileSelect(e.target.files[0]);
            }
        });
        
        function handleFileSelect(file) {
            if (!file.name.endsWith('.xlsx')) {
                showResult('❌ Apenas arquivos .xlsx são permitidos!', 'error');
                return;
            }
            
            selectedFile = file;
            fileName.textContent = file.name;
            fileSize.textContent = `Tamanho: ${(file.size / 1024 / 1024).toFixed(2)} MB`;
            fileInfo.style.display = 'block';
            uploadBtn.disabled = false;
            
            hideResult();
        }
        
        function uploadFile() {
            if (!selectedFile) return;
            
            const formData = new FormData();
            formData.append('excel_file', selectedFile);
            
            progress.style.display = 'block';
            uploadBtn.disabled = true;
            
            updateProgress(10, 'Enviando arquivo...');
            
            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                updateProgress(100, 'Concluído!');
                
                setTimeout(() => {
                    if (data.success) {
                        showResult(`
                            ✅ <strong>Upload realizado com sucesso!</strong><br>
                            📊 Total de REFs: ${data.total_refs}<br>
                            🖼️ Imagens encontradas: ${data.images_found}<br>
                            ✅ Uploads bem-sucedidos: ${data.uploads_successful}<br>
                            ❌ Uploads falharam: ${data.uploads_failed}
                        `, 'success');
                    } else {
                        showResult(`
                            ❌ <strong>Erro no upload:</strong><br>
                            ${data.error || 'Erro desconhecido'}
                        `, 'error');
                    }
                    
                    progress.style.display = 'none';
                    uploadBtn.disabled = false;
                }, 1000);
            })
            .catch(error => {
                updateProgress(0, 'Erro!');
                showResult(`❌ Erro na comunicação: ${error.message}`, 'error');
                progress.style.display = 'none';
                uploadBtn.disabled = false;
            });
        }
        
        function updateProgress(percent, text) {
            progressFill.style.width = percent + '%';
            progressText.textContent = text;
        }
        
        function showResult(content, type) {
            resultContent.innerHTML = content;
            result.className = `result ${type}`;
            result.style.display = 'block';
        }
        
        function hideResult() {
            result.style.display = 'none';
        }
    </script>
</body>
</html>
        """
    
    def health_check(self):
        """Endpoint de verificação de saúde"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            'status': 'ok',
            'message': 'Sistema Local Melhorado funcionando',
            'sistema_melhorado': SISTEMA_MELHORADO_AVAILABLE,
            'timestamp': time.time()
        }
        
        self.wfile.write(json.dumps(response).encode())
    
    def get_config(self):
        """Retorna configurações do sistema"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            'name': 'Sistema Local Melhorado',
            'version': '2.0',
            'features': [
                'Detecção melhorada de imagens',
                'Suporte OneCellAnchor e TwoCellAnchor',
                'Validação robusta de REFs',
                'Debug detalhado',
                'Detecção multi-coluna'
            ],
            'max_file_size': '50MB',
            'allowed_extensions': ['xlsx'],
            'recommended_files': [
                'fabrica_com_imagens.xlsx',
                'tartaruga.xlsx', 
                'carrinho.xlsx'
            ]
        }
        
        self.wfile.write(json.dumps(response).encode())
    
    def handle_upload(self):
        """Processa upload de arquivo Excel"""
        try:
            # Verifica se o sistema melhorado está disponível
            if not SISTEMA_MELHORADO_AVAILABLE:
                error_response = {
                    'success': False,
                    'error': 'Sistema melhorado não disponível. Verifique as dependências.'
                }
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(error_response).encode())
                return
            
            # Verifica se há arquivo na requisição
            content_length = int(self.headers['Content-Length'])
            if content_length == 0:
                error_response = {
                    'success': False,
                    'error': 'Nenhum arquivo enviado'
                }
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(error_response).encode())
                return
            
            # Lê dados do arquivo
            post_data = self.rfile.read(content_length)
            
            # Parse do multipart form data (simplificado)
            boundary = None
            for line in self.headers.get('Content-Type', '').split(';'):
                if 'boundary=' in line:
                    boundary = line.split('boundary=')[1].strip()
                    break
            
            if not boundary:
                error_response = {
                    'success': False,
                    'error': 'Formato de dados inválido'
                }
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(error_response).encode())
                return
            
            # Extrai arquivo do multipart data
            file_data = self.extract_file_from_multipart(post_data, boundary)
            
            if not file_data:
                error_response = {
                    'success': False,
                    'error': 'Arquivo não encontrado na requisição'
                }
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(error_response).encode())
                return
            
            # Salva arquivo temporariamente
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
            temp_file.write(file_data['content'])
            temp_file.close()
            
            logger.info(f"Arquivo salvo temporariamente: {temp_file.name}")
            
            try:
                # Processa com sistema melhorado
                sistema = SistemaExcelMelhorado(debug_mode=True)
                resultado = sistema.process_excel_melhorado(temp_file.name)
                
                if resultado['success']:
                    # Sucesso
                    response_data = {
                        'success': True,
                        'total_refs': len(resultado.get('images_data', [])),
                        'images_found': resultado['images_found'],
                        'total_images': resultado['total_images'],
                        'uploads_successful': resultado['images_found'],
                        'uploads_failed': 0,
                        'images_by_column': resultado.get('images_by_column', {}),
                        'anchor_types': resultado.get('anchor_types', {}),
                        'recommendations': resultado.get('recommendations', [])
                    }
                else:
                    # Erro no processamento
                    response_data = {
                        'success': False,
                        'error': resultado.get('error', 'Erro desconhecido no processamento'),
                        'total_refs': 0,
                        'images_found': 0,
                        'uploads_successful': 0,
                        'uploads_failed': 1
                    }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode())
                
            finally:
                # Remove arquivo temporário
                try:
                    os.unlink(temp_file.name)
                    logger.info(f"Arquivo temporário removido: {temp_file.name}")
                except Exception as e:
                    logger.warning(f"Erro ao remover arquivo temporário: {e}")
            
        except Exception as e:
            logger.error(f"Erro no upload: {e}")
            error_response = {
                'success': False,
                'error': f'Erro interno: {str(e)}',
                'total_refs': 0,
                'images_found': 0,
                'uploads_successful': 0,
                'uploads_failed': 1
            }
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(error_response).encode())
    
    def extract_file_from_multipart(self, data, boundary):
        """Extrai arquivo do multipart form data - versão melhorada"""
        try:
            # Converte para bytes se necessário
            if isinstance(data, str):
                data = data.encode('utf-8')
            
            # Encontra o boundary
            boundary_bytes = f'--{boundary}'.encode('utf-8')
            parts = data.split(boundary_bytes)
            
            for part in parts:
                # Procura por filename= no header
                if b'filename=' in part and b'.xlsx' in part:
                    # Encontra o início do conteúdo do arquivo
                    header_end = part.find(b'\r\n\r\n')
                    if header_end != -1:
                        # Pega o conteúdo do arquivo (após os headers)
                        file_content = part[header_end + 4:]
                        
                        # Remove o boundary final se existir
                        if file_content.endswith(b'\r\n--'):
                            file_content = file_content[:-5]
                        elif file_content.endswith(b'--'):
                            file_content = file_content[:-2]
                        
                        # Remove quebras de linha do final
                        file_content = file_content.rstrip(b'\r\n')
                        
                        # Verifica se o conteúdo parece ser um arquivo Excel válido
                        if len(file_content) > 100 and file_content.startswith(b'PK'):
                            return {
                                'content': file_content,
                                'filename': 'uploaded_file.xlsx'
                            }
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao extrair arquivo: {e}")
            return None
    
    def log_message(self, format, *args):
        """Override para logging personalizado"""
        logger.info(f"{self.address_string()} - {format % args}")

def start_server(port=8080):
    """Inicia o servidor local"""
    try:
        server = HTTPServer(('localhost', port), SistemaLocalHandler)
        
        print("🚀 SISTEMA LOCAL MELHORADO")
        print("=" * 50)
        print(f"📁 Frontend: http://localhost:{port}")
        print(f"💚 Health: http://localhost:{port}/health")
        print(f"⚙️  Config: http://localhost:{port}/config")
        print("=" * 50)
        print("🔧 Dependências:")
        print(f"   • Sistema Melhorado: {'✅' if SISTEMA_MELHORADO_AVAILABLE else '❌'}")
        print("=" * 50)
        
        if not SISTEMA_MELHORADO_AVAILABLE:
            print("⚠️  Sistema melhorado não disponível!")
            print("💡 Execute primeiro: python detector_imagens_melhorado.py")
            print("=" * 50)
        
        print("✅ Servidor iniciado!")
        print("🌐 Abrindo navegador...")
        
        # Abre navegador após 2 segundos
        def open_browser():
            time.sleep(2)
            webbrowser.open(f'http://localhost:{port}')
        
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Inicia servidor
        server.serve_forever()
        
    except KeyboardInterrupt:
        print("\n🛑 Servidor interrompido pelo usuário")
        server.shutdown()
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8080))
    start_server(port)
