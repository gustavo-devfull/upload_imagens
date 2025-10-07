#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema Híbrido: Frontend Online + Processamento Local + Upload FTP
Solução para quando o servidor PHP não está funcionando
"""

import os
import json
import tempfile
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import time
from upload_ftp_corrigido import FTPImageExtractorCorrigido

class HybridUploadHandler(BaseHTTPRequestHandler):
    """Handler para o servidor híbrido"""
    
    def do_GET(self):
        """Serve o frontend"""
        if self.path == '/':
            self.serve_frontend()
        elif self.path == '/config':
            self.serve_config()
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
    <title>Sistema de Upload de Imagens Excel - Híbrido</title>
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

        .progress-container {
            display: none;
            margin: 30px 0;
            background: #f8f9fa;
            border-radius: 15px;
            padding: 20px;
            border: 1px solid #e9ecef;
        }

        .progress-bar {
            width: 100%;
            height: 25px;
            background: #e9ecef;
            border-radius: 15px;
            overflow: hidden;
            margin-bottom: 15px;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(135deg, #28a745 0%, #20c997 50%, #17a2b8 100%);
            width: 0%;
            transition: width 0.5s ease;
            position: relative;
            border-radius: 15px;
        }

        .progress-fill::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.3) 50%, transparent 70%);
            animation: shimmer 2s infinite;
        }

        @keyframes shimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }

        .progress-text {
            text-align: center;
            color: #495057;
            font-size: 1rem;
            font-weight: 500;
            margin-bottom: 10px;
        }

        .progress-details {
            display: flex;
            justify-content: space-between;
            font-size: 0.8rem;
            color: #6c757d;
        }

        .progress-step {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }

        .progress-step-icon {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: #e9ecef;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 10px;
            font-size: 0.7rem;
        }

        .progress-step.active .progress-step-icon {
            background: #28a745;
            color: white;
        }

        .progress-step.completed .progress-step-icon {
            background: #28a745;
            color: white;
        }

        .progress-steps {
            margin: 15px 0;
        }

        .progress-step {
            display: flex;
            align-items: center;
            margin-bottom: 8px;
            font-size: 0.9rem;
            color: #6c757d;
            transition: color 0.3s ease;
        }

        .progress-step.active {
            color: #28a745;
            font-weight: 500;
        }

        .progress-step.completed {
            color: #28a745;
        }

        .progress-step-icon {
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: #e9ecef;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 12px;
            font-size: 0.8rem;
            font-weight: bold;
            transition: all 0.3s ease;
            border: 2px solid #e9ecef;
        }

        .progress-step.active .progress-step-icon {
            background: #28a745;
            color: white;
            border-color: #28a745;
            transform: scale(1.1);
        }

        .progress-step.completed .progress-step-icon {
            background: #28a745;
            color: white;
            border-color: #28a745;
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
            <p>Sistema Híbrido - Frontend Online + Processamento Local + Upload FTP</p>
        </div>

        <div class="content">
            <div class="status-box">
                <h3>✅ Sistema Híbrido Funcionando</h3>
                <p>Este sistema combina frontend web com processamento local para máxima compatibilidade.</p>
                <p><strong>Modo:</strong> Híbrido (Frontend Web + Processamento Local)</p>
                <p><strong>Upload:</strong> Via FTP para https://ideolog.ia.br/images/products/</p>
            </div>

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
                <div id="progressText" class="progress-text">Preparando upload...</div>
                <div class="progress-bar">
                    <div id="progressFill" class="progress-fill"></div>
                </div>
                <div id="progressSteps" class="progress-steps">
                    <div class="progress-step" id="step1">
                        <div class="progress-step-icon">1</div>
                        <span>Enviando arquivo</span>
                    </div>
                    <div class="progress-step" id="step2">
                        <div class="progress-step-icon">2</div>
                        <span>Analisando planilha</span>
                    </div>
                    <div class="progress-step" id="step3">
                        <div class="progress-step-icon">3</div>
                        <span>Extraindo imagens</span>
                    </div>
                    <div class="progress-step" id="step4">
                        <div class="progress-step-icon">4</div>
                        <span>Upload FTP</span>
                    </div>
                    <div class="progress-step" id="step5">
                        <div class="progress-step-icon">5</div>
                        <span>Finalizando</span>
                    </div>
                </div>
                <div id="progressDetails" class="progress-details">
                    <span id="progressStatus">Aguardando...</span>
                    <span id="progressTime">00:00</span>
                </div>
            </div>

            <div id="results" class="results">
                <h3>📊 Resultados do Processamento</h3>
                <div id="resultsContent"></div>
            </div>
        </div>
    </div>

    <script>
        let selectedFile = null;

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

            // Barra de progresso avançada
            let progress = 0;
            let currentStep = 0;
            let startTime = Date.now();
            
            const steps = [
                { text: 'Enviando arquivo...', progress: 20, stepId: 'step1' },
                { text: 'Analisando planilha...', progress: 40, stepId: 'step2' },
                { text: 'Extraindo imagens...', progress: 60, stepId: 'step3' },
                { text: 'Fazendo upload FTP...', progress: 80, stepId: 'step4' },
                { text: 'Finalizando...', progress: 100, stepId: 'step5' }
            ];
            
            // Cronômetro
            const timerInterval = setInterval(() => {
                const elapsed = Math.floor((Date.now() - startTime) / 1000);
                const minutes = Math.floor(elapsed / 60).toString().padStart(2, '0');
                const seconds = (elapsed % 60).toString().padStart(2, '0');
                document.getElementById('progressTime').textContent = `${minutes}:${seconds}`;
            }, 1000);
            
            // Progresso dos passos
            const progressInterval = setInterval(() => {
                if (currentStep < steps.length) {
                    const step = steps[currentStep];
                    
                    // Atualiza barra de progresso
                    progress = step.progress;
                    document.getElementById('progressFill').style.width = progress + '%';
                    document.getElementById('progressText').textContent = step.text;
                    
                    // Atualiza passo atual
                    const stepElement = document.getElementById(step.stepId);
                    stepElement.classList.add('active');
                    
                    // Marca passos anteriores como completos
                    for (let i = 0; i < currentStep; i++) {
                        const prevStep = document.getElementById(steps[i].stepId);
                        prevStep.classList.remove('active');
                        prevStep.classList.add('completed');
                    }
                    
                    // Atualiza status
                    document.getElementById('progressStatus').textContent = step.text;
                    
                    currentStep++;
                } else {
                    clearInterval(progressInterval);
                }
            }, 400);

            fetch('/upload', {
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                clearInterval(progressInterval);
                clearInterval(timerInterval);
                
                // Marca todos os passos como completos
                steps.forEach(step => {
                    const stepElement = document.getElementById(step.stepId);
                    stepElement.classList.remove('active');
                    stepElement.classList.add('completed');
                });
                
                // Atualiza progresso final com informações detalhadas
                document.getElementById('progressFill').style.width = '100%';
                if (data.uploads_successful > 0) {
                    document.getElementById('progressText').textContent = `✅ Upload concluído! ${data.uploads_successful} imagem(ns) enviada(s)`;
                    document.getElementById('progressStatus').textContent = `✅ ${data.uploads_successful} imagem(ns) enviada(s) com sucesso`;
                } else if (data.error) {
                    document.getElementById('progressText').textContent = `❌ ${data.error}`;
                    document.getElementById('progressStatus').textContent = `❌ Erro: ${data.error}`;
                } else {
                    document.getElementById('progressText').textContent = '⚠️ Nenhuma imagem foi enviada';
                    document.getElementById('progressStatus').textContent = '⚠️ Nenhuma imagem foi enviada';
                }
                
                setTimeout(() => {
                    showResults(data);
                }, 1500);
            })
            .catch(error => {
                clearInterval(progressInterval);
                clearInterval(timerInterval);
                
                document.getElementById('progressText').textContent = `❌ Erro no upload: ${error.message}`;
                document.getElementById('progressStatus').textContent = `❌ Erro: ${error.message}`;
                
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
                        <div class="stat-number">${data.total_refs}</div>
                        <div class="stat-label">REFs Processadas</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${data.images_found}</div>
                        <div class="stat-label">Imagens Encontradas</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${data.uploads_successful}</div>
                        <div class="stat-label">Uploads Bem-sucedidos</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${data.uploads_failed}</div>
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
                html += `<div class="warning-box"><h3>⚠️ Arquivo sem imagens</h3><p>${data.error}</p>`;
                if (data.suggestion) {
                    html += `<p><strong>💡 Sugestão:</strong> ${data.suggestion}</p>`;
                }
                html += `</div>`;
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
            'message': 'Sistema Híbrido Funcionando',
            'mode': 'hybrid',
            'ftp_host': '46.202.90.62',
            'base_url': 'https://ideolog.ia.br/images/products/',
            'max_file_size': '50MB'
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(config).encode())
    
    def handle_upload(self):
        """Processa uploads de arquivos Excel"""
        try:
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
            
            # Verifica se o arquivo tem imagens
            if stats['images_found'] == 0:
                error_response = {
                    'error': f'Arquivo {filename} não contém imagens na coluna H. Use um arquivo que tenha imagens inseridas.',
                    'total_refs': stats['total_refs'],
                    'images_found': stats['images_found'],
                    'uploads_successful': 0,
                    'uploads_failed': stats['total_refs'],
                    'suggestion': 'Arquivos recomendados: tartaruga.xlsx ou carrinho.xlsx'
                }
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(error_response).encode())
                os.remove(temp_path)
                return
            
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
            error_response = {'error': str(e)}
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(error_response).encode())

def start_hybrid_server():
    """Inicia o servidor híbrido"""
    port = 8081  # Porta diferente para evitar conflito
    
    print("🚀 Iniciando Sistema Híbrido...")
    print("=" * 50)
    print(f"📁 Frontend: http://localhost:{port}")
    print(f"🔧 API: http://localhost:{port}/upload")
    print(f"⚙️  Config: http://localhost:{port}/config")
    print("=" * 50)
    
    server = HTTPServer(('localhost', port), HybridUploadHandler)
    
    # Abre navegador automaticamente
    def open_browser():
        time.sleep(2)
        webbrowser.open(f'http://localhost:{port}')
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Sistema híbrido encerrado.")
        server.shutdown()

if __name__ == "__main__":
    start_hybrid_server()
