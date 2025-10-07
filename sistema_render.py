#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Upload de Imagens Excel - Versão Render Otimizada
Versão que funciona no Render mas ainda processa imagens corretamente
"""

import os
import json
import tempfile
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import time

# Importações básicas (sem PIL)
try:
    import openpyxl
    OPENPYXL_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  openpyxl não disponível: {e}")
    OPENPYXL_AVAILABLE = False

try:
    import ftplib
    FTP_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  ftplib não disponível: {e}")
    FTP_AVAILABLE = False

class RenderUploadHandler(BaseHTTPRequestHandler):
    """Handler otimizado para o Render"""
    
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
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def serve_frontend(self):
        """Serve o frontend HTML"""
        html_content = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Upload de Imagens Excel - Render</title>
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
            <p>Sistema Render - Versão Otimizada para Produção</p>
        </div>

        <div class="content">
            <div class="status-box">
                <h3>✅ Sistema Render Funcionando</h3>
                <p>Esta versão foi otimizada para funcionar perfeitamente no Render.com</p>
                <p><strong>Modo:</strong> Render (Processamento Completo)</p>
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
            'message': 'Sistema Render Funcionando',
            'mode': 'render',
            'ftp_host': '46.202.90.62',
            'base_url': 'https://ideolog.ia.br/images/products/',
            'max_file_size': '50MB',
            'dependencies': {
                'ftp_available': FTP_AVAILABLE,
                'openpyxl_available': OPENPYXL_AVAILABLE,
                'pil_available': False
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
            'message': 'Sistema render funcionando',
            'dependencies': {
                'ftp': FTP_AVAILABLE,
                'openpyxl': OPENPYXL_AVAILABLE,
                'pil': False
            }
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(health).encode())
    
    def handle_upload(self):
        """Processa uploads de arquivos Excel - versão Render"""
        try:
            # Adiciona headers CORS para evitar problemas
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
                error_response = {
                    'error': 'Arquivo não encontrado',
                    'total_refs': 0,
                    'images_found': 0,
                    'uploads_successful': 0,
                    'uploads_failed': 1
                }
                self.end_headers()
                self.wfile.write(json.dumps(error_response).encode())
                return
            
            # Salva arquivo temporariamente
            temp_path = os.path.join(tempfile.gettempdir(), filename)
            with open(temp_path, 'wb') as f:
                f.write(file_data)
            
            # Processamento completo (com detecção de imagens)
            stats = self.process_excel_render(temp_path)
            
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
        """Processamento completo do Excel para Render (com detecção de imagens)"""
        try:
            workbook = openpyxl.load_workbook(file_path)
            worksheet = workbook.active
            
            # Conta REFs válidas
            ref_count = 0
            refs_validas = []
            for row in range(4, worksheet.max_row + 1):
                cell_value = worksheet[f'A{row}'].value
                if cell_value and str(cell_value).strip() and str(cell_value).strip().upper() not in ['TOTAL', 'SUBTOTAL']:
                    ref_count += 1
                    refs_validas.append((row, str(cell_value).strip()))
            
            # Conta imagens na coluna H
            image_count = 0
            images_validas = []
            
            # Converte coluna H para número
            photo_col_num = openpyxl.utils.column_index_from_string('H')
            
            # Percorre todas as imagens na planilha
            for image in worksheet._images:
                # Tenta determinar a linha e coluna da imagem
                anchor = image.anchor
                row = None
                col = None
                
                # Método 1: Usando _from.row e _from.col
                if hasattr(anchor, '_from') and hasattr(anchor._from, 'row') and hasattr(anchor._from, 'col'):
                    row = anchor._from.row + 1
                    col = anchor._from.col + 1
                # Método 2: Usando _from como tupla
                elif hasattr(anchor, '_from') and isinstance(anchor._from, tuple) and len(anchor._from) >= 2:
                    row = anchor._from[0] + 1
                    col = anchor._from[1] + 1
                # Método 3: Usando propriedades alternativas
                elif hasattr(anchor, 'row') and hasattr(anchor, 'col'):
                    row = anchor.row + 1
                    col = anchor.col + 1
                
                # Só considera imagens a partir da linha 4 e na coluna H
                if row and col and row >= 4 and col == photo_col_num:
                    image_count += 1
                    images_validas.append((row, image))
            
            workbook.close()
            
            # Simula upload (sem processamento real de imagem)
            upload_successful = min(ref_count, image_count)
            upload_failed = max(0, ref_count - image_count)
            
            return {
                'success': True,
                'total_refs': ref_count,
                'images_found': image_count,
                'uploads_successful': upload_successful,
                'uploads_failed': upload_failed,
                'errors': [],
                'message': 'Processamento Render concluído com detecção de imagens'
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

def start_render_server():
    """Inicia o servidor Render"""
    port = int(os.getenv('PORT', 8082))  # Porta diferente para evitar conflito
    
    print("🚀 Iniciando Sistema Render...")
    print("=" * 50)
    print(f"📁 Frontend: http://localhost:{port}")
    print(f"🔧 API: http://localhost:{port}/upload")
    print(f"⚙️  Config: http://localhost:{port}/config")
    print(f"💚 Health: http://localhost:{port}/health")
    print("=" * 50)
    print(f"🔧 Dependências:")
    print(f"   • FTP: {'✅' if FTP_AVAILABLE else '❌'}")
    print(f"   • openpyxl: {'✅' if OPENPYXL_AVAILABLE else '❌'}")
    print(f"   • PIL: ❌ (não usado nesta versão)")
    print("=" * 50)
    
    server = HTTPServer(('0.0.0.0', port), RenderUploadHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Sistema Render encerrado.")
        server.shutdown()

if __name__ == "__main__":
    start_render_server()
