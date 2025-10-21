#!/usr/bin/env python3
"""
🚀 SISTEMA FLASK SIMPLES E ROBUSTO
Sistema Flask com frontend simplificado para garantir funcionamento
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
    """Serve o frontend HTML simplificado"""
    try:
        html_content = get_simple_frontend_html()
        return html_content
    except Exception as e:
        logger.error(f"Erro ao servir frontend: {e}")
        return jsonify({'error': f'Erro interno: {e}'}), 500

def get_simple_frontend_html():
    """Retorna o HTML do frontend simplificado"""
    return '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Sistema Excel - Detector Integrado</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            padding: 30px;
            max-width: 800px;
            width: 100%;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .title {
            color: #333;
            font-size: 2em;
            margin-bottom: 10px;
        }
        
        .subtitle {
            color: #666;
            font-size: 1em;
        }
        
        .upload-section {
            text-align: center;
            margin-bottom: 30px;
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
            margin: 10px;
            transition: all 0.3s ease;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .btn:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        
        .btn-success {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        }
        
        .loading {
            display: none;
            text-align: center;
            margin: 20px 0;
            color: #667eea;
            font-size: 1.1em;
        }
        
        .results {
            display: none;
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
        }
        
        .results.show {
            display: block;
        }
        
        .success {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        
        .error {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .stat-item {
            background: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .stat-value {
            font-size: 1.8em;
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
            border-radius: 8px;
            padding: 15px;
            margin-top: 15px;
        }
        
        .debug-title {
            font-weight: bold;
            margin-bottom: 10px;
            color: #333;
        }
        
        .recommendation {
            margin: 5px 0;
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
        
        .file-info {
            background: #e9ecef;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            font-size: 0.9em;
            color: #495057;
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
            <button class="btn" onclick="selectFile()">📁 Selecionar Arquivo</button>
            <button class="btn btn-success" id="processBtn" onclick="processFile()" disabled>🚀 Processar</button>
        </div>
        
        <div id="fileInfo" class="file-info" style="display: none;"></div>
        
        <div class="loading" id="loading">
            <p>⏳ Processando arquivo...</p>
        </div>
        
        <div class="results" id="results">
            <!-- Resultados serão inseridos aqui -->
        </div>
    </div>

    <script>
        let selectedFile = null;
        
        function selectFile() {
            document.getElementById('fileInput').click();
        }
        
        document.getElementById('fileInput').addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                selectedFile = file;
                document.getElementById('processBtn').disabled = false;
                document.getElementById('fileInfo').style.display = 'block';
                document.getElementById('fileInfo').innerHTML = `📄 Arquivo selecionado: <strong>${file.name}</strong> (${(file.size / 1024 / 1024).toFixed(2)} MB)`;
            }
        });

        function processFile() {
            if (!selectedFile) {
                alert('Por favor, selecione um arquivo primeiro.');
                return;
            }
            
            uploadFile(selectedFile);
        }

        async function uploadFile(file) {
            console.log('🚀 Iniciando upload:', file.name);
            
            const formData = new FormData();
            formData.append('file', file);
            
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');
            
            // Mostrar loading
            loading.style.display = 'block';
            results.style.display = 'none';
            results.className = 'results';
            
            try {
                console.log('📡 Enviando requisição...');
                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });
                
                console.log('📡 Resposta recebida:', response.status);
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                
                const data = await response.json();
                console.log('📊 Dados recebidos:', data);
                
                // Esconder loading
                loading.style.display = 'none';
                
                // Mostrar resultados
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
                console.log('✅ Upload bem-sucedido');
                html += '<div class="success">✅ Upload realizado com sucesso!</div>';
                
                html += '<div class="stats">';
                html += `<div class="stat-item"><div class="stat-value">${data.stats.total_refs || 0}</div><div class="stat-label">📊 Total de REFs</div></div>`;
                html += `<div class="stat-item"><div class="stat-value">${data.stats.images_found || 0}</div><div class="stat-label">🖼️ Imagens encontradas</div></div>`;
                html += `<div class="stat-item"><div class="stat-value">${data.stats.successful_uploads || 0}</div><div class="stat-label">✅ Uploads bem-sucedidos</div></div>`;
                html += `<div class="stat-item"><div class="stat-value">${data.stats.failed_uploads || 0}</div><div class="stat-label">❌ Uploads falharam</div></div>`;
                html += '</div>';
                
                if (data.debug_info && data.debug_info.length > 0) {
                    html += '<div class="debug-info">';
                    html += '<div class="debug-title">🔍 Informações Detalhadas:</div>';
                    
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
            console.log('❌ Exibindo erro:', message);
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
    port = int(os.getenv('PORT', 8083))  # Porta diferente para evitar conflito
    debug = os.getenv('FLASK_ENV') != 'production'

    print("🚀 SISTEMA FLASK SIMPLES E ROBUSTO")
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

