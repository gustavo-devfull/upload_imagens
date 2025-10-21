#!/usr/bin/env python3
"""
🚀 SISTEMA LOCAL FLASK MELHORADO - Upload de Imagens Excel
Versão Flask mais robusta para uploads
"""

import os
import sys
import tempfile
import logging
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

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

# Configuração Flask
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Diretório para uploads temporários
UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'xlsx'}

def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def serve_frontend():
    """Serve o frontend HTML"""
    try:
        html_content = get_frontend_html()
        return html_content
    except Exception as e:
        logger.error(f"Erro ao servir frontend: {e}")
        return jsonify({'error': f'Erro interno: {e}'}), 500

def get_frontend_html():
    """Retorna o HTML do frontend"""
    return """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Sistema Excel Melhorado - Flask</title>
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
        
        .debug-info {
            margin: 20px 0;
            padding: 15px;
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 10px;
            text-align: left;
            font-family: monospace;
            font-size: 0.9em;
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Sistema Excel Melhorado</h1>
            <p>Upload de imagens com detecção avançada (Flask)</p>
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
        
        <div class="debug-info" id="debugInfo">
            <h4>🔍 Debug Info:</h4>
            <pre id="debugContent"></pre>
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
        const debugInfo = document.getElementById('debugInfo');
        const debugContent = document.getElementById('debugContent');
        
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
            hideDebug();
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
                            ❌ Uploads falharam: ${data.uploads_failed}<br>
                            📈 Total de imagens: ${data.total_images}<br>
                            📋 Colunas com imagens: ${JSON.stringify(data.images_by_column || {})}<br>
                            🔗 Tipos de anchor: ${JSON.stringify(data.anchor_types || {})}
                        `, 'success');
                        
                        if (data.recommendations && data.recommendations.length > 0) {
                            showDebug('Recomendações: ' + data.recommendations.join(', '));
                        }
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
        
        function showDebug(content) {
            debugContent.textContent = content;
            debugInfo.style.display = 'block';
        }
        
        function hideDebug() {
            debugInfo.style.display = 'none';
        }
    </script>
</body>
</html>
    """

@app.route('/upload', methods=['POST'])
def upload_file():
    """Processa upload de arquivo Excel"""
    try:
        # Verifica se o sistema melhorado está disponível
        if not SISTEMA_MELHORADO_AVAILABLE:
            return jsonify({
                'success': False,
                'error': 'Sistema melhorado não disponível. Verifique as dependências.'
            }), 500
        
        # Verifica se há arquivo na requisição
        if 'excel_file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'Nenhum arquivo enviado'
            }), 400
        
        file = request.files['excel_file']
        
        # Verifica se arquivo foi selecionado
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'Nenhum arquivo selecionado'
            }), 400
        
        # Verifica se arquivo é permitido
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Apenas arquivos .xlsx são permitidos'
            }), 400
        
        # Salva arquivo temporariamente
        filename = secure_filename(file.filename)
        temp_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(temp_path)
        
        logger.info(f"Arquivo salvo temporariamente: {temp_path}")
        
        try:
            # Processa com sistema melhorado
            sistema = SistemaExcelMelhorado(debug_mode=True)
            resultado = sistema.process_excel_melhorado(temp_path)
            
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
            
            return jsonify(response_data)
            
        finally:
            # Remove arquivo temporário
            try:
                os.unlink(temp_path)
                logger.info(f"Arquivo temporário removido: {temp_path}")
            except Exception as e:
                logger.warning(f"Erro ao remover arquivo temporário: {e}")
    
    except Exception as e:
        logger.error(f"Erro no upload: {e}")
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}',
            'total_refs': 0,
            'images_found': 0,
            'uploads_successful': 0,
            'uploads_failed': 1
        }), 500

@app.route('/health')
def health_check():
    """Endpoint de verificação de saúde"""
    return jsonify({
        'status': 'ok',
        'message': 'Sistema Flask Melhorado funcionando',
        'sistema_melhorado': SISTEMA_MELHORADO_AVAILABLE
    })

@app.route('/config')
def get_config():
    """Retorna configurações do sistema"""
    return jsonify({
        'name': 'Sistema Flask Melhorado',
        'version': '2.0',
        'features': [
            'Detecção melhorada de imagens',
            'Suporte OneCellAnchor e TwoCellAnchor',
            'Validação robusta de REFs',
            'Debug detalhado',
            'Detecção multi-coluna',
            'Upload robusto com Flask'
        ],
        'max_file_size': '50MB',
        'allowed_extensions': ['xlsx'],
        'recommended_files': [
            'fabrica_com_imagens.xlsx',
            'tartaruga.xlsx', 
            'carrinho.xlsx'
        ]
    })

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8080))
    
    print("🚀 SISTEMA FLASK MELHORADO")
    print("=" * 50)
    print(f"📁 Frontend: http://localhost:{port}")
    print(f"💚 Health: http://localhost:{port}/health")
    print(f"⚙️  Config: http://localhost:{port}/config")
    print("=" * 50)
    print("🔧 Dependências:")
    print(f"   • Sistema Melhorado: {'✅' if SISTEMA_MELHORADO_AVAILABLE else '❌'}")
    print(f"   • Flask: ✅")
    print("=" * 50)
    
    if not SISTEMA_MELHORADO_AVAILABLE:
        print("⚠️  Sistema melhorado não disponível!")
        print("💡 Execute primeiro: python detector_imagens_melhorado.py")
        print("=" * 50)
    
    print("✅ Servidor Flask iniciado!")
    print("🌐 Acesse: http://localhost:8080")
    
    # Inicia servidor Flask
    app.run(host='0.0.0.0', port=port, debug=True)
