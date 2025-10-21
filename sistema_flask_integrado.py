#!/usr/bin/env python3
"""
🚀 SISTEMA FLASK COM DETECTOR INTEGRADO
Sistema Flask que usa o detector corrigido para imagens embedadas
"""

import os
import sys
import tempfile
import logging
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

# Importa o detector integrado
try:
    from detector_integrado import DetectorImagensIntegrado
    DETECTOR_INTEGRADO_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Detector integrado não disponível: {e}")
    DETECTOR_INTEGRADO_AVAILABLE = False

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
    return '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Sistema de Upload Excel - Detector Integrado</title>
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
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .title {
            color: #333;
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
        }
        
        .subtitle {
            color: #666;
            font-size: 1.1em;
            margin-bottom: 20px;
        }
        
        .upload-section {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .upload-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 50px;
            font-size: 1.2em;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 10px;
        }
        
        .upload-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }
        
        .process-btn {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 50px;
            font-size: 1.2em;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            margin-left: 15px;
        }
        
        .process-btn:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }
        
        .process-btn:disabled {
            background: #6c757d;
            cursor: not-allowed;
            opacity: 0.6;
        }
        
        .file-input {
            display: none;
        }
        
        .results {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 25px;
            margin-top: 20px;
            display: none;
        }
        
        .results.show {
            display: block;
        }
        
        .success {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        
        .error {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .stat-item {
            background: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }
        
        .stat-label {
            color: #666;
            font-size: 0.9em;
        }
        
        .debug-info {
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
        }
        
        .debug-title {
            font-weight: bold;
            margin-bottom: 10px;
            color: #333;
        }
        
        .recommendations {
            margin-top: 15px;
        }
        
        .recommendation {
            margin: 8px 0;
            padding: 8px 12px;
            border-radius: 5px;
            font-size: 0.9em;
        }
        
        .recommendation.error {
            background: #f8d7da;
            color: #721c24;
        }
        
        .recommendation.info {
            background: #d1ecf1;
            color: #0c5460;
        }
        
        .loading {
            display: none;
            text-align: center;
            margin: 20px 0;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .footer {
            text-align: center;
            margin-top: 30px;
            color: #666;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">🚀 Sistema Excel</h1>
            <p class="subtitle">Detector Integrado de Imagens Embedadas</p>
        </div>
        
        <div class="upload-section">
            <input type="file" id="fileInput" class="file-input" accept=".xlsx">
            <button class="upload-btn" onclick="document.getElementById('fileInput').click()">
                📁 Selecionar Arquivo
            </button>
            <button class="process-btn" id="processBtn" onclick="processFile()" disabled>
                🚀 Processar Arquivo
            </button>
        </div>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Processando arquivo...</p>
        </div>
        
        <div class="results" id="results">
            <!-- Resultados serão inseridos aqui -->
        </div>
        
        <div class="footer">
            <p>💡 Sistema com detecção avançada de imagens embedadas</p>
        </div>
    </div>

    <script>
        let selectedFile = null;
        
        document.getElementById('fileInput').addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                selectedFile = file;
                document.getElementById('processBtn').disabled = false;
                document.getElementById('processBtn').innerHTML = `🚀 Processar: ${file.name}`;
            }
        });

        function processFile() {
            if (selectedFile) {
                uploadFile(selectedFile);
            }
        }

        async function uploadFile(file) {
            const formData = new FormData();
            formData.append('file', file);
            
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');
            
            loading.style.display = 'block';
            results.style.display = 'none';
            
            try {
                console.log('🚀 Iniciando upload do arquivo:', file.name);
                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });
                
                console.log('📡 Resposta recebida:', response.status);
                const data = await response.json();
                console.log('📊 Dados recebidos:', data);
                
                loading.style.display = 'none';
                displayResults(data);
                
            } catch (error) {
                console.error('❌ Erro no upload:', error);
                loading.style.display = 'none';
                displayError('Erro no upload: ' + error.message);
            }
        }

        function displayResults(data) {
            console.log('🎨 Exibindo resultados:', data);
            const results = document.getElementById('results');
            results.className = 'results show';
            
            let html = '';
            
            if (data.success) {
                console.log('✅ Upload bem-sucedido, gerando HTML...');
                html += '<div class="success">✅ Upload realizado com sucesso!</div>';
                
                html += '<div class="stats">';
                html += `<div class="stat-item"><div class="stat-value">${data.stats.total_refs || 0}</div><div class="stat-label">📊 Total de REFs</div></div>`;
                html += `<div class="stat-item"><div class="stat-value">${data.stats.images_found || 0}</div><div class="stat-label">🖼️ Imagens encontradas</div></div>`;
                html += `<div class="stat-item"><div class="stat-value">${data.stats.successful_uploads || 0}</div><div class="stat-label">✅ Uploads bem-sucedidos</div></div>`;
                html += `<div class="stat-item"><div class="stat-value">${data.stats.failed_uploads || 0}</div><div class="stat-label">❌ Uploads falharam</div></div>`;
                html += `<div class="stat-item"><div class="stat-value">${data.stats.total_images || 0}</div><div class="stat-label">📝 Total de imagens</div></div>`;
                html += `<div class="stat-item"><div class="stat-value">${JSON.stringify(data.stats.images_by_column || {})}</div><div class="stat-label">📁 Colunas com imagens</div></div>`;
                html += `<div class="stat-item"><div class="stat-value">${JSON.stringify(data.stats.anchor_types || {})}</div><div class="stat-label">🔗 Tipos de anchor</div></div>`;
                html += '</div>';
                
                if (data.debug_info && data.debug_info.length > 0) {
                    html += '<div class="debug-info">';
                    html += '<div class="debug-title">🔍 Debug Info:</div>';
                    html += '<div class="recommendations">';
                    
                    data.debug_info.forEach(info => {
                        if (info.includes('❌')) {
                            html += `<div class="recommendation error">${info}</div>`;
                        } else if (info.includes('💡')) {
                            html += `<div class="recommendation info">${info}</div>`;
                        } else {
                            html += `<div class="recommendation">${info}</div>`;
                        }
                    });
                    
                    html += '</div>';
                    html += '</div>';
                }
                
            } else {
                console.log('❌ Upload falhou:', data.error);
                html += '<div class="error">❌ Erro no upload: ' + (data.error || 'Erro desconhecido') + '</div>';
            }
            
            console.log('📝 HTML gerado:', html);
            results.innerHTML = html;
            console.log('✅ Resultados exibidos na tela');
        }

        function displayError(message) {
            const results = document.getElementById('results');
            results.className = 'results show';
            results.innerHTML = '<div class="error">❌ ' + message + '</div>';
        }
    </script>
</body>
</html>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    """Processa upload de arquivo Excel"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'Nenhum arquivo selecionado'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Tipo de arquivo não permitido. Use apenas .xlsx'}), 400
        
        # Salvar arquivo temporariamente
        filename = secure_filename(file.filename)
        temp_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(temp_path)
        
        logger.info(f"Arquivo salvo temporariamente: {temp_path}")
        
        try:
            # Processar arquivo com detector integrado
            if DETECTOR_INTEGRADO_AVAILABLE:
                detector = DetectorImagensIntegrado(debug_mode=True)
                images = detector.detectar_imagens(temp_path, target_columns=['H'], start_row=4, ref_column='A')
                
                # Calcular estatísticas
                stats = {
                    'total_refs': len(set(img['ref'] for img in images)),
                    'images_found': len(images),
                    'successful_uploads': len(images),
                    'failed_uploads': 0,
                    'total_images': len(images),
                    'images_by_column': {},
                    'anchor_types': {}
                }
                
                # Agrupar por coluna
                for img in images:
                    col = img['col']
                    stats['images_by_column'][col] = stats['images_by_column'].get(col, 0) + 1
                    
                    anchor_type = img.get('anchor_type', 'Unknown')
                    stats['anchor_types'][anchor_type] = stats['anchor_types'].get(anchor_type, 0) + 1
                
                # Preparar debug info
                debug_info = []
                if len(images) == 0:
                    debug_info.append("❌ Arquivo não contém imagens. Insira imagens nas células.")
                    debug_info.append("💡 Considere mover imagens para a coluna H.")
                else:
                    debug_info.append(f"✅ {len(images)} imagens detectadas com sucesso!")
                    debug_info.append(f"📊 REFs encontradas: {', '.join(set(img['ref'] for img in images))}")
                    positions = [f"{img['col']}{img['row']}" for img in images]
                    debug_info.append(f"📍 Posições: {', '.join(positions)}")
                
                # Adicionar informações do detector
                debug_info.extend(detector.debug_info[-5:])  # Últimas 5 mensagens de debug
                
                return jsonify({
                    'success': True,
                    'stats': stats,
                    'images': images,
                    'debug_info': debug_info
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Detector integrado não disponível'
                }), 500
                
        except Exception as e:
            logger.error(f"Erro no processamento: {e}")
            return jsonify({
                'success': False,
                'error': f'Erro no processamento: {str(e)}'
            }), 500
        
        finally:
            # Remover arquivo temporário
            try:
                os.remove(temp_path)
                logger.info(f"Arquivo temporário removido: {temp_path}")
            except Exception as e:
                logger.warning(f"Erro ao remover arquivo temporário: {e}")
    
    except Exception as e:
        logger.error(f"Erro no upload: {e}")
        return jsonify({'success': False, 'error': f'Erro interno: {str(e)}'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'detector_integrado': DETECTOR_INTEGRADO_AVAILABLE,
        'timestamp': str(os.popen('date').read().strip())
    })

@app.route('/config')
def config():
    """Configuração do sistema"""
    return jsonify({
        'max_file_size': '50MB',
        'allowed_extensions': list(ALLOWED_EXTENSIONS),
        'upload_folder': UPLOAD_FOLDER,
        'detector_integrado': DETECTOR_INTEGRADO_AVAILABLE,
        'python_version': sys.version,
        'working_directory': os.getcwd()
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8082))  # Porta diferente para evitar conflito
    debug = os.getenv('FLASK_ENV') != 'production'

    print("🚀 SISTEMA FLASK COM DETECTOR INTEGRADO")
    print("=" * 50)
    print(f"📁 Frontend: http://localhost:{port}")
    print(f"💚 Health: http://localhost:{port}/health")
    print(f"⚙️  Config: http://localhost:{port}/config")
    print("=" * 50)
    print("🔧 Dependências:")
    print(f"   • Detector Integrado: {'✅' if DETECTOR_INTEGRADO_AVAILABLE else '❌'}")
    print("=" * 50)

    if not DETECTOR_INTEGRADO_AVAILABLE:
        logger.error("❌ Detector integrado não disponível.")
        sys.exit(1)

    try:
        logger.info(f"✅ Servidor Flask iniciado!")
        print(f"✅ Servidor Flask iniciado!")
        print(f"🌐 Acesse: http://localhost:{port}")
        app.run(host='0.0.0.0', port=port, debug=debug)
    except Exception as e:
        logger.error(f"❌ Erro ao iniciar servidor Flask: {e}")
        print(f"❌ Erro ao iniciar servidor Flask: {e}")
        sys.exit(1)
