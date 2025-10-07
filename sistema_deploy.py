#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Upload de Imagens Excel - Versão para Deploy
Sistema híbrido otimizado para Render.com e outros serviços de deploy
"""

import os
import json
import tempfile
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import time

# Importações opcionais com fallback
try:
    from upload_ftp_corrigido import FTPImageExtractorCorrigido
    FTP_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Módulo FTP não disponível: {e}")
    FTP_AVAILABLE = False

try:
    import openpyxl
    OPENPYXL_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  openpyxl não disponível: {e}")
    OPENPYXL_AVAILABLE = False

try:
    from PIL import Image as PILImage
    PIL_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  PIL não disponível: {e}")
    PIL_AVAILABLE = False

class DeployUploadHandler(BaseHTTPRequestHandler):
    """Handler para o servidor de deploy"""
    
    def do_GET(self):
        """Serve o frontend"""
        if self.path == '/':
            self.serve_frontend()
        elif self.path == '/config':
            self.serve_config()
        elif self.path == '/health':
            self.serve_health()
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Processa uploads"""
        if self.path == '/upload':
            self.handle_upload()
        else:
            self.send_error(404)
    
    def serve_frontend(self):
        """Serve o frontend HTML"""
        html_content = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Upload de Imagens Excel - Deploy</title>
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
            padding: 20px;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            font-weight: 300;
        }

        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }

        .content {
            padding: 40px;
        }

        .status-box {
            background: #e8f5e8;
            border: 1px solid #c8e6c9;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }

        .status-box h3 {
            color: #2e7d32;
            margin-bottom: 10px;
        }

        .warning-box {
            background: #fff3e0;
            border: 1px solid #ffcc02;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }

        .warning-box h3 {
            color: #f57c00;
            margin-bottom: 10px;
        }

        .upload-area {
            border: 3px dashed #667eea;
            border-radius: 15px;
            padding: 40px;
            text-align: center;
            margin-bottom: 30px;
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .upload-area:hover {
            border-color: #764ba2;
            background: #f8f9ff;
        }

        .upload-icon {
            font-size: 4rem;
            color: #667eea;
            margin-bottom: 20px;
        }

        .upload-text {
            font-size: 1.2rem;
            color: #333;
            margin-bottom: 10px;
        }

        .upload-subtext {
            color: #666;
            font-size: 0.9rem;
        }

        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 50px;
            font-size: 1.1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            margin: 10px;
            text-decoration: none;
            display: inline-block;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }

        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .info-box {
            background: #e3f2fd;
            border: 1px solid #bbdefb;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }

        .info-box h3 {
            color: #1976d2;
            margin-bottom: 10px;
        }

        .progress-container {
            display: none;
            margin: 30px 0;
        }

        .progress-bar {
            width: 100%;
            height: 20px;
            background: #e9ecef;
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 10px;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            width: 0%;
            transition: width 0.3s ease;
        }

        .progress-text {
            text-align: center;
            color: #666;
            font-size: 0.9rem;
        }

        .results {
            display: none;
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 15px;
        }

        .results h3 {
            margin-bottom: 20px;
            color: #333;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }

        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }

        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }

        .stat-label {
            color: #666;
            font-size: 0.9rem;
        }

        .image-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px;
            background: white;
            border-radius: 10px;
            margin-bottom: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }

        .image-info {
            flex: 1;
            margin-left: 15px;
        }

        .image-name {
            font-weight: 600;
            color: #333;
            margin-bottom: 5px;
        }

        .image-url {
            font-size: 0.8rem;
            color: #666;
            word-break: break-all;
        }

        .copy-btn {
            background: #28a745;
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.8rem;
            cursor: pointer;
        }

        @media (max-width: 768px) {
            .container {
                margin: 10px;
                border-radius: 15px;
            }
            
            .header {
                padding: 20px;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .content {
                padding: 20px;
            }
            
            .upload-area {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🖼️ Sistema de Upload de Imagens Excel</h1>
            <p>Sistema Deploy - Versão Otimizada para Serviços Cloud</p>
        </div>

        <div class="content">
            <div class="status-box">
                <h3>✅ Sistema Deploy Funcionando</h3>
                <p>Este sistema foi otimizado para funcionar em serviços de deploy como Render.com</p>
                <p><strong>Modo:</strong> Deploy (Frontend Web + Processamento Otimizado)</p>
                <p><strong>Upload:</strong> Via FTP para https://ideolog.ia.br/images/products/</p>
            </div>

            <div id="dependenciesStatus"></div>

            <div class="info-box">
                <h3>📋 Informações Importantes</h3>
                <ul>
                    <li><strong>Coluna REF:</strong> A (códigos dos produtos)</li>
                    <li><strong>Coluna PHOTO:</strong> H (imagens)</li>
                    <li><strong>Linha inicial:</strong> 4</li>
                    <li><strong>Formato:</strong> Apenas arquivos .xlsx</li>
                    <li><strong>Limite:</strong> 50MB por arquivo</li>
                </ul>
            </div>

            <div class="upload-area" onclick="document.getElementById('fileInput').click()">
                <div class="upload-icon">📁</div>
                <div class="upload-text">Clique para selecionar arquivo Excel</div>
                <div class="upload-subtext">Apenas arquivos .xlsx são aceitos</div>
            </div>

            <input type="file" id="fileInput" accept=".xlsx" style="display: none;" onchange="handleFileSelect(this.files[0])">

            <div style="text-align: center;">
                <button class="btn" onclick="uploadFile()" id="uploadBtn" disabled>
                    🚀 Fazer Upload
                </button>
                <button class="btn" onclick="resetForm()" id="resetBtn" disabled>
                    🔄 Limpar
                </button>
            </div>

            <div id="progressContainer" class="progress-container">
                <div class="progress-bar">
                    <div id="progressFill" class="progress-fill"></div>
                </div>
                <div id="progressText" class="progress-text"></div>
            </div>

            <div id="results" class="results">
                <h3>📊 Resultados do Processamento</h3>
                <div id="resultsContent"></div>
            </div>
        </div>
    </div>

    <script>
        let selectedFile = null;

        // Verifica status das dependências
        fetch('/config')
            .then(response => response.json())
            .then(data => {
                const statusDiv = document.getElementById('dependenciesStatus');
                let html = '';
                
                if (data.dependencies) {
                    if (data.dependencies.ftp_available) {
                        html += '<div class="status-box"><h3>✅ FTP Disponível</h3><p>Sistema de upload FTP funcionando</p></div>';
                    } else {
                        html += '<div class="warning-box"><h3>⚠️ FTP Indisponível</h3><p>Sistema de upload FTP não está disponível</p></div>';
                    }
                    
                    if (data.dependencies.openpyxl_available) {
                        html += '<div class="status-box"><h3>✅ Excel Disponível</h3><p>Processamento de arquivos Excel funcionando</p></div>';
                    } else {
                        html += '<div class="warning-box"><h3>⚠️ Excel Indisponível</h3><p>Processamento de Excel não está disponível</p></div>';
                    }
                }
                
                statusDiv.innerHTML = html;
            });

        function handleFileSelect(file) {
            if (file && file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') {
                selectedFile = file;
                document.getElementById('uploadBtn').disabled = false;
                document.getElementById('resetBtn').disabled = false;
                document.querySelector('.upload-text').textContent = file.name;
                document.querySelector('.upload-area').style.borderColor = '#28a745';
                document.querySelector('.upload-area').style.backgroundColor = '#f8fff8';
            } else {
                alert('Por favor, selecione um arquivo Excel (.xlsx) válido.');
            }
        }

        function uploadFile() {
            if (!selectedFile) {
                alert('Por favor, selecione um arquivo Excel.');
                return;
            }

            const formData = new FormData();
            formData.append('excel_file', selectedFile);

            // Mostra progresso
            document.getElementById('progressContainer').style.display = 'block';
            document.getElementById('uploadBtn').disabled = true;
            document.getElementById('resetBtn').disabled = true;

            // Simula progresso
            let progress = 0;
            const progressInterval = setInterval(() => {
                progress += 10;
                document.getElementById('progressFill').style.width = progress + '%';
                
                if (progress < 30) {
                    document.getElementById('progressText').textContent = 'Enviando arquivo...';
                } else if (progress < 60) {
                    document.getElementById('progressText').textContent = 'Processando imagens...';
                } else if (progress < 90) {
                    document.getElementById('progressText').textContent = 'Fazendo upload FTP...';
                } else {
                    document.getElementById('progressText').textContent = 'Finalizando...';
                }
            }, 200);

            fetch('/upload', {
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                clearInterval(progressInterval);
                document.getElementById('progressFill').style.width = '100%';
                document.getElementById('progressText').textContent = 'Upload concluído!';
                
                setTimeout(() => {
                    showResults(data);
                }, 500);
            })
            .catch(error => {
                clearInterval(progressInterval);
                alert('Erro no upload: ' + error.message);
                document.getElementById('uploadBtn').disabled = false;
                document.getElementById('resetBtn').disabled = false;
            });
        }

        function showResults(data) {
            const resultsDiv = document.getElementById('results');
            const contentDiv = document.getElementById('resultsContent');
            
            let html = `
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number">${data.total_refs || 0}</div>
                        <div class="stat-label">REFs Processadas</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${data.images_found || 0}</div>
                        <div class="stat-label">Imagens Encontradas</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${data.uploads_successful || 0}</div>
                        <div class="stat-label">Uploads Bem-sucedidos</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${data.uploads_failed || 0}</div>
                        <div class="stat-label">Uploads Falharam</div>
                    </div>
                </div>
            `;

            if (data.images && data.images.length > 0) {
                html += '<h4 style="margin-bottom: 15px; color: #333;">🖼️ Imagens Processadas</h4>';
                data.images.forEach(image => {
                    html += `
                        <div class="image-item">
                            <div class="image-info">
                                <div class="image-name">${image.name}</div>
                                <div class="image-url">${image.url}</div>
                            </div>
                            <button onclick="copyToClipboard('${image.url}')" class="copy-btn">
                                📋 Copiar URL
                            </button>
                        </div>
                    `;
                });
            }

            if (data.error) {
                html += `<div class="warning-box"><h3>⚠️ Erro</h3><p>${data.error}</p></div>`;
            }

            contentDiv.innerHTML = html;
            resultsDiv.style.display = 'block';
            
            document.getElementById('uploadBtn').disabled = false;
            document.getElementById('resetBtn').disabled = false;
        }

        function resetForm() {
            selectedFile = null;
            document.getElementById('fileInput').value = '';
            document.getElementById('uploadBtn').disabled = true;
            document.getElementById('resetBtn').disabled = true;
            document.querySelector('.upload-text').textContent = 'Clique para selecionar arquivo Excel';
            document.querySelector('.upload-area').style.borderColor = '#667eea';
            document.querySelector('.upload-area').style.backgroundColor = 'transparent';
            document.getElementById('progressContainer').style.display = 'none';
            document.getElementById('results').style.display = 'none';
        }

        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(() => {
                alert('URL copiada para a área de transferência!');
            }).catch(() => {
                // Fallback para navegadores mais antigos
                const textArea = document.createElement('textarea');
                textArea.value = text;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                alert('URL copiada para a área de transferência!');
            });
        }
    </script>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode())
    
    def serve_config(self):
        """Serve configurações do sistema"""
        config = {
            'status': 'ok',
            'message': 'Sistema Deploy Funcionando',
            'mode': 'deploy',
            'ftp_host': '46.202.90.62',
            'base_url': 'https://ideolog.ia.br/images/products/',
            'max_file_size': '50MB',
            'dependencies': {
                'ftp_available': FTP_AVAILABLE,
                'openpyxl_available': OPENPYXL_AVAILABLE,
                'pil_available': PIL_AVAILABLE
            }
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(config).encode())
    
    def serve_health(self):
        """Serve health check"""
        health = {
            'status': 'ok',
            'message': 'Sistema funcionando',
            'dependencies': {
                'ftp': FTP_AVAILABLE,
                'openpyxl': OPENPYXL_AVAILABLE,
                'pil': PIL_AVAILABLE
            }
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(health).encode())
    
    def handle_upload(self):
        """Processa uploads de arquivos Excel"""
        try:
            if not FTP_AVAILABLE:
                error_response = {
                    'error': 'Sistema FTP não disponível no ambiente de deploy',
                    'total_refs': 0,
                    'images_found': 0,
                    'uploads_successful': 0,
                    'uploads_failed': 1
                }
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(error_response).encode())
                return
            
            # Lê o arquivo enviado
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Parse do FormData
            boundary = self.headers['Content-Type'].split('boundary=')[1]
            parts = post_data.split(f'--{boundary}'.encode())
            
            file_data = None
            filename = None
            
            for part in parts:
                if b'Content-Disposition: form-data' in part:
                    if b'filename=' in part:
                        # Extrai nome do arquivo
                        filename_start = part.find(b'filename="') + 11
                        filename_end = part.find(b'"', filename_start)
                        filename = part[filename_start:filename_end].decode()
                        
                        # Extrai dados do arquivo
                        file_start = part.find(b'\r\n\r\n') + 4
                        file_data = part[file_start:-2]  # Remove \r\n no final
                        break
            
            if not file_data or not filename:
                self.send_error(400, 'Arquivo não encontrado')
                return
            
            # Salva arquivo temporariamente
            temp_path = os.path.join(tempfile.gettempdir(), filename)
            with open(temp_path, 'wb') as f:
                f.write(file_data)
            
            # Processa com o sistema FTP corrigido
            extractor = FTPImageExtractorCorrigido(
                "46.202.90.62", 
                "u715606397.ideolog.ia.br", 
                "]X9CC>t~ihWhdzNq"
            )
            
            stats = extractor.process_excel_file(temp_path, start_row=4, photo_column='H')
            
            # Prepara resposta
            response_data = {
                'success': True,
                'total_refs': stats['total_refs'],
                'images_found': stats['images_found'],
                'uploads_successful': stats['uploads_successful'],
                'uploads_failed': stats['uploads_failed'],
                'errors': stats['errors'],
                'images': []
            }
            
            # Adiciona informações das imagens processadas
            if stats['uploads_successful'] > 0:
                response_data['images'] = [
                    {
                        'name': 'Imagem processada',
                        'url': 'https://ideolog.ia.br/images/products/'
                    }
                ]
            
            # Remove arquivo temporário
            os.remove(temp_path)
            
            # Envia resposta
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            error_response = {
                'error': str(e),
                'total_refs': 0,
                'images_found': 0,
                'uploads_successful': 0,
                'uploads_failed': 1
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(error_response).encode())

def start_deploy_server():
    """Inicia o servidor de deploy"""
    port = int(os.getenv('PORT', 8080))
    
    print("🚀 Iniciando Sistema de Deploy...")
    print("=" * 50)
    print(f"📁 Frontend: http://localhost:{port}")
    print(f"🔧 API: http://localhost:{port}/upload")
    print(f"⚙️  Config: http://localhost:{port}/config")
    print(f"💚 Health: http://localhost:{port}/health")
    print("=" * 50)
    print(f"🔧 Dependências:")
    print(f"   • FTP: {'✅' if FTP_AVAILABLE else '❌'}")
    print(f"   • openpyxl: {'✅' if OPENPYXL_AVAILABLE else '❌'}")
    print(f"   • PIL: {'✅' if PIL_AVAILABLE else '❌'}")
    print("=" * 50)
    
    server = HTTPServer(('0.0.0.0', port), DeployUploadHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Sistema de deploy encerrado.")
        server.shutdown()

if __name__ == "__main__":
    start_deploy_server()
