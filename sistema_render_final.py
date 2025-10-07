#!/usr/bin/env python3
"""
Sistema de Upload de Imagens Excel - Versão Final para Render
Detecta imagens em planilhas Excel e faz upload para FTP
"""

import os
import sys
import json
import tempfile
import traceback
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import time
import cgi
import io

# Imports condicionais para evitar erros de deploy
try:
    import openpyxl
    OPENPYXL_AVAILABLE = True
except ImportError:
    OPENPYXL_AVAILABLE = False
    print("⚠️ openpyxl não disponível")

try:
    import ftplib
    FTP_AVAILABLE = True
except ImportError:
    FTP_AVAILABLE = False
    print("⚠️ ftplib não disponível")

# Configurações FTP
FTP_HOST = "46.202.90.62"
FTP_USER = "u715606397.ideolog.ia.br"
FTP_PASS = "]X9CC>t~ihWhdzNq"
FTP_DIR = "public_html/images/products"

class RenderUploadHandler(BaseHTTPRequestHandler):
    """Handler otimizado para Render"""
    
    def log_message(self, format, *args):
        """Suprime logs desnecessários"""
        pass
    
    def do_GET(self):
        """Serve páginas"""
        if self.path == '/':
            self.serve_frontend()
        elif self.path == '/health':
            self.serve_health()
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
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_cors_headers()
        self.end_headers()
    
    def send_cors_headers(self):
        """Envia headers CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Type', 'application/json')
    
    def serve_health(self):
        """Health check para Render"""
        health = {
            "status": "ok",
            "message": "Sistema Render Final funcionando",
            "dependencies": {
                "ftp": FTP_AVAILABLE,
                "openpyxl": OPENPYXL_AVAILABLE,
                "pil": False
            },
            "timestamp": time.time()
        }
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(health).encode())
    
    def serve_config(self):
        """Configurações do sistema"""
        config = {
            "ftp_host": FTP_HOST,
            "ftp_user": FTP_USER,
            "ftp_dir": FTP_DIR,
            "max_file_size": "10MB",
            "supported_formats": [".xlsx"],
            "features": [
                "Detecção de imagens",
                "Upload FTP automático",
                "Validação de arquivos",
                "Barra de progresso avançada"
            ]
        }
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(config).encode())
    
    def serve_frontend(self):
        """Serve o frontend HTML otimizado"""
        html_content = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Sistema Upload Excel - Render Final</title>
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
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .upload-area {
            padding: 40px;
            text-align: center;
        }
        
        .file-input-wrapper {
            position: relative;
            display: inline-block;
            margin: 20px 0;
        }
        
        .file-input {
            display: none;
        }
        
        .file-input-label {
            display: inline-block;
            padding: 15px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 50px;
            cursor: pointer;
            font-size: 1.1em;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .file-input-label:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
        }
        
        .file-name {
            margin: 15px 0;
            font-size: 1.1em;
            color: #333;
            font-weight: 500;
        }
        
        .buttons {
            margin: 30px 0;
        }
        
        .btn {
            padding: 12px 25px;
            margin: 0 10px;
            border: none;
            border-radius: 25px;
            font-size: 1em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .btn-primary:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
        }
        
        .btn-secondary {
            background: #f8f9fa;
            color: #6c757d;
            border: 2px solid #dee2e6;
        }
        
        .btn-secondary:hover:not(:disabled) {
            background: #e9ecef;
            border-color: #adb5bd;
        }
        
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none !important;
        }
        
        /* Barra de Progresso Avançada */
        .progress-container {
            margin: 30px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 15px;
            display: none;
        }
        
        .progress-text {
            text-align: center;
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 15px;
            color: #333;
        }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background: #e9ecef;
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 20px;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            width: 0%;
            transition: width 0.3s ease;
            border-radius: 10px;
            position: relative;
        }
        
        .progress-fill::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            animation: shimmer 2s infinite;
        }
        
        @keyframes shimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        
        .progress-steps {
            display: flex;
            justify-content: space-between;
            margin-bottom: 15px;
        }
        
        .progress-step {
            display: flex;
            flex-direction: column;
            align-items: center;
            flex: 1;
            position: relative;
        }
        
        .progress-step-icon {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: #e9ecef;
            color: #6c757d;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-bottom: 8px;
            transition: all 0.3s ease;
        }
        
        .progress-step.active .progress-step-icon {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            transform: scale(1.1);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .progress-step.completed .progress-step-icon {
            background: #28a745;
            color: white;
        }
        
        .progress-step span {
            font-size: 0.9em;
            color: #6c757d;
            text-align: center;
        }
        
        .progress-step.active span {
            color: #333;
            font-weight: bold;
        }
        
        .progress-step.completed span {
            color: #28a745;
            font-weight: bold;
        }
        
        .progress-details {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.9em;
            color: #6c757d;
        }
        
        .results {
            margin: 30px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 15px;
            display: none;
        }
        
        .success-box {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        
        .error-box {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        
        .warning-box {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .stat-item {
            background: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }
        
        .stat-label {
            color: #6c757d;
            font-size: 0.9em;
        }
        
        .footer {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #6c757d;
            border-top: 1px solid #dee2e6;
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
                font-size: 2em;
            }
            
            .upload-area {
                padding: 20px;
            }
            
            .progress-steps {
                flex-direction: column;
                gap: 15px;
            }
            
            .progress-step {
                flex-direction: row;
                text-align: left;
            }
            
            .progress-step-icon {
                margin-right: 15px;
                margin-bottom: 0;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Sistema Upload Excel</h1>
            <p>Versão Final para Render - Upload de Imagens Automático</p>
        </div>
        
        <div class="upload-area">
            <h2>📁 Selecione seu arquivo Excel</h2>
            <p>Arquivos suportados: .xlsx com imagens na coluna H</p>
            
            <div class="file-input-wrapper">
                <input type="file" id="excelFile" class="file-input" accept=".xlsx" />
                <label for="excelFile" class="file-input-label">
                    📂 Escolher Arquivo Excel
                </label>
            </div>
            
            <div id="fileName" class="file-name"></div>
            
            <div class="buttons">
                <button id="uploadBtn" class="btn btn-primary" onclick="uploadFile()" disabled>
                    🚀 Fazer Upload
                </button>
                <button id="resetBtn" class="btn btn-secondary" onclick="resetForm()" disabled>
                    🔄 Resetar
                </button>
            </div>
            
            <!-- Barra de Progresso Avançada -->
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
            
            <!-- Resultados -->
            <div id="results" class="results"></div>
        </div>
        
        <div class="footer">
            <p>🔧 Sistema Final para Render | 🚀 Upload Automático | 📊 Detecção Inteligente</p>
        </div>
    </div>

    <script>
        let selectedFile = null;
        
        document.getElementById('excelFile').addEventListener('change', handleFileSelect);
        
        function handleFileSelect(event) {
            const file = event.target.files[0];
            if (file) {
                selectedFile = file;
                document.getElementById('fileName').textContent = `📄 ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)`;
                document.getElementById('uploadBtn').disabled = false;
                document.getElementById('resetBtn').disabled = false;
            }
        }
        
        function uploadFile() {
            if (!selectedFile) {
                alert('Por favor, selecione um arquivo Excel.');
                return;
            }
            
            const formData = new FormData();
            formData.append('excel_file', selectedFile);
            
            // Desabilita botões
            document.getElementById('uploadBtn').disabled = true;
            document.getElementById('resetBtn').disabled = true;
            
            // Mostra barra de progresso
            document.getElementById('progressContainer').style.display = 'block';
            document.getElementById('results').style.display = 'none';
            
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
            
            // Upload com timeout aumentado
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 120000); // 2 minutos
            
            fetch('/upload', {
                method: 'POST',
                body: formData,
                signal: controller.signal
            })
            .then(response => {
                clearTimeout(timeoutId);
                return response.json();
            })
            .then(data => {
                clearInterval(progressInterval);
                clearInterval(timerInterval);
                
                // Marca todos os passos como completos
                steps.forEach(step => {
                    const stepElement = document.getElementById(step.stepId);
                    stepElement.classList.remove('active');
                    stepElement.classList.add('completed');
                });
                
                // Atualiza progresso final
                document.getElementById('progressFill').style.width = '100%';
                if (data.success && data.uploads_successful > 0) {
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
                clearTimeout(timeoutId);
                
                document.getElementById('progressText').textContent = `❌ Erro no upload: ${error.message}`;
                document.getElementById('progressStatus').textContent = `❌ Erro: ${error.message}`;
                
                alert('Erro no upload: ' + error.message);
                document.getElementById('uploadBtn').disabled = false;
                document.getElementById('resetBtn').disabled = false;
            });
        }
        
        function showResults(data) {
            const resultsDiv = document.getElementById('results');
            resultsDiv.style.display = 'block';
            
            let html = '';
            
            if (data.success && data.uploads_successful > 0) {
                html += `<div class="success-box">
                    <h3>✅ Upload Concluído com Sucesso!</h3>
                    <p>${data.uploads_successful} imagem(ns) processada(s) e enviada(s) para o FTP.</p>
                </div>`;
                
                html += `<div class="stats">
                    <div class="stat-item">
                        <div class="stat-number">${data.total_refs}</div>
                        <div class="stat-label">REFs Processadas</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">${data.images_found}</div>
                        <div class="stat-label">Imagens Encontradas</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">${data.uploads_successful}</div>
                        <div class="stat-label">Uploads Bem-sucedidos</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">${data.uploads_failed}</div>
                        <div class="stat-label">Uploads Falharam</div>
                    </div>
                </div>`;
                
            } else if (data.error) {
                html += `<div class="warning-box">
                    <h3>⚠️ Arquivo sem imagens</h3>
                    <p>${data.error}</p>`;
                if (data.suggestion) {
                    html += `<p><strong>💡 Sugestão:</strong> ${data.suggestion}</p>`;
                }
                html += `</div>`;
                
                html += `<div class="stats">
                    <div class="stat-item">
                        <div class="stat-number">${data.total_refs || 0}</div>
                        <div class="stat-label">REFs Processadas</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">${data.images_found || 0}</div>
                        <div class="stat-label">Imagens Encontradas</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">${data.uploads_successful || 0}</div>
                        <div class="stat-label">Uploads Bem-sucedidos</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">${data.uploads_failed || 0}</div>
                        <div class="stat-label">Uploads Falharam</div>
                    </div>
                </div>`;
            } else {
                html += `<div class="error-box">
                    <h3>❌ Erro no Processamento</h3>
                    <p>Não foi possível processar o arquivo. Verifique se é um arquivo Excel válido.</p>
                </div>`;
            }
            
            resultsDiv.innerHTML = html;
            
            // Reabilita botões
            document.getElementById('uploadBtn').disabled = false;
            document.getElementById('resetBtn').disabled = false;
        }
        
        function resetForm() {
            document.getElementById('excelFile').value = '';
            document.getElementById('fileName').textContent = '';
            document.getElementById('progressContainer').style.display = 'none';
            document.getElementById('results').style.display = 'none';
            document.getElementById('uploadBtn').disabled = true;
            document.getElementById('resetBtn').disabled = true;
            selectedFile = null;
            
            // Reset progress steps
            document.querySelectorAll('.progress-step').forEach(step => {
                step.classList.remove('active', 'completed');
            });
        }
    </script>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def handle_upload(self):
        """Processa uploads usando cgi.FieldStorage"""
        try:
            # Headers CORS
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            
            if not FTP_AVAILABLE or not OPENPYXL_AVAILABLE:
                error_response = {
                    'error': 'Dependências não disponíveis no ambiente de deploy',
                    'total_refs': 0,
                    'images_found': 0,
                    'uploads_successful': 0,
                    'uploads_failed': 1
                }
                self.end_headers()
                self.wfile.write(json.dumps(error_response).encode())
                return
            
            # Usa cgi.FieldStorage para parsing mais robusto
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
            
            # Verifica se o arquivo foi enviado
            if 'excel_file' not in form:
                error_response = {
                    'error': 'Arquivo não encontrado no formulário',
                    'total_refs': 0,
                    'images_found': 0,
                    'uploads_successful': 0,
                    'uploads_failed': 1
                }
                self.end_headers()
                self.wfile.write(json.dumps(error_response).encode())
                return
            
            file_item = form['excel_file']
            
            if not file_item.filename:
                error_response = {
                    'error': 'Nome do arquivo não encontrado',
                    'total_refs': 0,
                    'images_found': 0,
                    'uploads_successful': 0,
                    'uploads_failed': 1
                }
                self.end_headers()
                self.wfile.write(json.dumps(error_response).encode())
                return
            
            # Salva arquivo temporariamente
            temp_path = os.path.join(tempfile.gettempdir(), file_item.filename)
            with open(temp_path, 'wb') as f:
                f.write(file_item.file.read())
            
            # Processamento completo
            stats = self.process_excel_render(temp_path)
            
            # Verifica se o arquivo tem imagens
            if stats['images_found'] == 0:
                error_response = {
                    'error': f'Arquivo {file_item.filename} não contém imagens na coluna H. Use um arquivo que tenha imagens inseridas.',
                    'total_refs': stats['total_refs'],
                    'images_found': stats['images_found'],
                    'uploads_successful': 0,
                    'uploads_failed': stats['total_refs'],
                    'suggestion': 'Arquivos recomendados: tartaruga.xlsx ou carrinho.xlsx'
                }
                self.end_headers()
                self.wfile.write(json.dumps(error_response).encode())
                os.remove(temp_path)
                return
            
            # Remove arquivo temporário
            os.remove(temp_path)
            
            # Envia resposta
            self.end_headers()
            self.wfile.write(json.dumps(stats).encode())
            
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
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(error_response).encode())
    
    def process_excel_render(self, file_path):
        """Processamento completo do Excel para Render"""
        try:
            workbook = openpyxl.load_workbook(file_path)
            worksheet = workbook.active
            
            # Processa REFs
            refs = self.get_ref_column_data(worksheet, start_row=4)
            
            # Processa imagens
            images = self.extract_images_from_worksheet(worksheet, start_row=4, photo_column='H')
            
            # Faz upload das imagens
            uploads_successful = 0
            uploads_failed = 0
            errors = []
            
            for image_data in images:
                try:
                    if self.upload_image_to_ftp(image_data['image'], image_data['ref']):
                        uploads_successful += 1
                    else:
                        uploads_failed += 1
                        errors.append(f"Falha no upload da imagem para REF: {image_data['ref']}")
                except Exception as e:
                    uploads_failed += 1
                    errors.append(f"Erro no upload da imagem para REF {image_data['ref']}: {str(e)}")
            
            return {
                'success': True,
                'total_refs': len(refs),
                'images_found': len(images),
                'uploads_successful': uploads_successful,
                'uploads_failed': uploads_failed,
                'errors': errors,
                'message': 'Processamento Render Final concluído com detecção de imagens'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'total_refs': 0,
                'images_found': 0,
                'uploads_successful': 0,
                'uploads_failed': 1
            }
    
    def get_ref_column_data(self, worksheet, start_row=4):
        """Extrai dados da coluna REF"""
        refs = []
        try:
            for row in range(start_row, worksheet.max_row + 1):
                cell_value = worksheet[f'A{row}'].value
                if cell_value and str(cell_value).strip() and str(cell_value).upper() not in ['TOTAL', 'SUBTOTAL', '']:
                    refs.append(str(cell_value).strip())
        except Exception as e:
            print(f"Erro ao ler REFs: {e}")
        return refs
    
    def extract_images_from_worksheet(self, worksheet, start_row=4, photo_column='H'):
        """Extrai imagens da planilha"""
        images = []
        try:
            for image in worksheet._images:
                # Verifica se a imagem está na coluna correta e linha válida
                if hasattr(image, 'anchor') and image.anchor:
                    anchor = image.anchor
                    if hasattr(anchor, '_from') and anchor._from:
                        col_idx = anchor._from.col
                        row_idx = anchor._from.row + 1  # openpyxl usa índice 0-based
                        
                        # Converte índice da coluna para letra
                        col_letter = openpyxl.utils.get_column_letter(col_idx + 1)
                        
                        if col_letter == photo_column and row_idx >= start_row:
                            # Busca REF correspondente
                            ref_cell = worksheet[f'A{row_idx}']
                            if ref_cell.value:
                                ref_value = str(ref_cell.value).strip()
                                if ref_value and ref_value.upper() not in ['TOTAL', 'SUBTOTAL', '']:
                                    images.append({
                                        'image': image,
                                        'ref': ref_value,
                                        'row': row_idx,
                                        'col': col_letter
                                    })
        except Exception as e:
            print(f"Erro ao extrair imagens: {e}")
        return images
    
    def upload_image_to_ftp(self, image, ref_value):
        """Faz upload da imagem para FTP"""
        try:
            # Salva imagem temporariamente
            temp_image_path = self.save_image_to_temp(image, ref_value)
            
            # Conecta ao FTP
            ftp = ftplib.FTP()
            ftp.connect(FTP_HOST, 21, timeout=300)
            ftp.login(FTP_USER, FTP_PASS)
            
            # Cria diretórios se necessário
            try:
                ftp.cwd('public_html')
            except:
                ftp.mkd('public_html')
                ftp.cwd('public_html')
            
            try:
                ftp.cwd('images')
            except:
                ftp.mkd('images')
                ftp.cwd('images')
            
            try:
                ftp.cwd('products')
            except:
                ftp.mkd('products')
                ftp.cwd('products')
            
            # Upload do arquivo
            with open(temp_image_path, 'rb') as file:
                ftp.storbinary(f'STOR {ref_value}.jpg', file)
            
            ftp.quit()
            
            # Remove arquivo temporário
            os.remove(temp_image_path)
            
            return True
            
        except Exception as e:
            print(f"Erro no upload FTP: {e}")
            return False
    
    def save_image_to_temp(self, image, ref_value):
        """Salva imagem temporariamente"""
        try:
            # Sanitiza nome do arquivo
            safe_ref = "".join(c for c in ref_value if c.isalnum() or c in ('-', '_')).rstrip()
            if not safe_ref:
                safe_ref = f"image_{int(time.time())}"
            
            temp_path = os.path.join(tempfile.gettempdir(), f"{safe_ref}.jpg")
            
            # Tenta diferentes métodos para extrair dados da imagem
            image_data = None
            
            # Método 1: _data() (mais comum)
            if hasattr(image, '_data') and callable(image._data):
                try:
                    image_data = image._data()
                except:
                    pass
            
            # Método 2: ref (BytesIO)
            if not image_data and hasattr(image, 'ref'):
                try:
                    image_data = image.ref.read()
                except:
                    pass
            
            # Método 3: data
            if not image_data and hasattr(image, 'data'):
                try:
                    image_data = image.data
                except:
                    pass
            
            # Método 4: image.save() como último recurso
            if not image_data:
                try:
                    image.save(temp_path)
                    return temp_path
                except:
                    pass
            
            # Salva dados extraídos
            if image_data:
                with open(temp_path, 'wb') as f:
                    f.write(image_data)
                return temp_path
            
            raise Exception("Não foi possível extrair dados da imagem")
            
        except Exception as e:
            print(f"Erro ao salvar imagem: {e}")
            raise

def start_render_server():
    """Inicia o servidor Render final"""
    port = int(os.getenv('PORT', 8080))
    
    print("🚀 Iniciando Sistema Render Final...")
    print("=" * 50)
    print(f"📁 Frontend: http://localhost:{port}")
    print(f"🔧 API: http://localhost:{port}/upload")
    print(f"⚙️  Config: http://localhost:{port}/config")
    print(f"💚 Health: http://localhost:{port}/health")
    print("=" * 50)
    print("🔧 Dependências:")
    print(f"   • FTP: {'✅' if FTP_AVAILABLE else '❌'}")
    print(f"   • openpyxl: {'✅' if OPENPYXL_AVAILABLE else '❌'}")
    print(f"   • PIL: ❌ (não usado nesta versão)")
    print("=" * 50)
    
    try:
        server = HTTPServer(('0.0.0.0', port), RenderUploadHandler)
        print(f"✅ Servidor iniciado na porta {port}")
        print("🔄 Aguardando conexões...")
        server.serve_forever()
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_render_server()
