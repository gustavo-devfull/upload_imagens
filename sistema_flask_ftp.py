#!/usr/bin/env python3
"""
🚀 SISTEMA FLASK COM UPLOAD DIRETO PARA FTP
Sistema Flask que extrai imagens do Excel e salva diretamente no FTP
"""

import os
import sys
import tempfile
import logging
import ftplib
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime

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

# Configurações FTP (configure aqui seus dados)
FTP_CONFIG = {
    'host': 'seu-servidor-ftp.com',
    'user': 'seu-usuario',
    'password': 'sua-senha',
    'directory': '/uploads/'
}

def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class FTPUploader:
    def __init__(self, config):
        self.config = config
        self.connection = None
    
    def conectar(self):
        """Conecta ao servidor FTP"""
        try:
            logger.info(f"🔗 Conectando ao FTP: {self.config['host']}")
            self.connection = ftplib.FTP()
            self.connection.connect(self.config['host'], 21)
            self.connection.login(self.config['user'], self.config['password'])
            self.connection.cwd(self.config['directory'])
            logger.info("✅ Conectado ao FTP com sucesso!")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao conectar FTP: {e}")
            return False
    
    def desconectar(self):
        """Desconecta do servidor FTP"""
        if self.connection:
            try:
                self.connection.quit()
                logger.info("🔌 Desconectado do FTP")
            except Exception as e:
                logger.warning(f"⚠️ Erro ao desconectar FTP: {e}")
    
    def upload_imagem(self, image_data: bytes, filename: str) -> bool:
        """Faz upload de uma imagem para o FTP"""
        try:
            if not self.connection:
                logger.error("❌ Não conectado ao FTP!")
                return False
            
            logger.info(f"📤 Upload: {filename}")
            
            # Criar arquivo temporário
            temp_path = f"/tmp/{filename}"
            with open(temp_path, 'wb') as f:
                f.write(image_data)
            
            # Fazer upload para FTP
            with open(temp_path, 'rb') as f:
                self.connection.storbinary(f'STOR {filename}', f)
            
            # Remover arquivo temporário
            os.remove(temp_path)
            
            logger.info(f"   ✅ Upload bem-sucedido: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"   ❌ Erro no upload {filename}: {e}")
            return False

def extrair_imagens_do_excel(file_path: str) -> list:
    """Extrai imagens de um arquivo Excel"""
    import zipfile
    
    logger.info(f"🔍 Extraindo imagens de: {file_path}")
    images_extracted = []
    
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            # Listar arquivos de mídia
            media_files = [name for name in zf.namelist() if name.startswith('xl/media/') and name.endswith(('.jpg', '.jpeg', '.png'))]
            logger.info(f"🖼️ Arquivos de mídia encontrados: {len(media_files)}")
            
            # Obter posições das imagens
            positions = []
            if DETECTOR_INTEGRADO_AVAILABLE:
                try:
                    detector = DetectorImagensIntegrado(debug_mode=False)
                    positions = detector.detectar_imagens(file_path, target_columns=['H'], start_row=4, ref_column='A')
                except Exception as e:
                    logger.warning(f"Erro ao obter posições: {e}")
            
            # Extrair imagens
            for i, media_file in enumerate(media_files):
                image_filename = os.path.basename(media_file)
                
                # Ler dados da imagem
                with zf.open(media_file) as img_file:
                    image_data = img_file.read()
                
                # Obter informações da posição se disponível
                position_info = {}
                if i < len(positions):
                    pos = positions[i]
                    position_info = {
                        'ref': pos['ref'],
                        'position': f"{pos['col']}{pos['row']}",
                        'col': pos['col'],
                        'row': pos['row']
                    }
                
                # Criar nome único para o arquivo
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                if position_info.get('ref'):
                    output_filename = f"{position_info['ref']}_{image_filename}"
                else:
                    output_filename = f"imagem_{i+1}_{timestamp}_{image_filename}"
                
                image_info = {
                    'original_filename': image_filename,
                    'ftp_filename': output_filename,
                    'image_data': image_data,
                    'file_size': len(image_data),
                    'index': i + 1,
                    **position_info
                }
                
                images_extracted.append(image_info)
                
                logger.info(f"   ✅ Imagem {i+1} extraída:")
                logger.info(f"      📁 Arquivo: {output_filename}")
                logger.info(f"      📏 Tamanho: {len(image_data):,} bytes")
                if position_info.get('position'):
                    logger.info(f"      📍 Posição: {position_info['position']}")
                    logger.info(f"      🔢 REF: {position_info['ref']}")
            
            logger.info(f"🎉 {len(images_extracted)} imagens extraídas!")
            return images_extracted
            
    except Exception as e:
        logger.error(f"❌ Erro na extração: {e}")
        return []

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
    <title>🚀 Sistema Excel → FTP</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f0f0f0;
            margin: 0;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }
        
        .upload-section {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .btn {
            background: #007bff;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 5px;
            cursor: pointer;
            margin: 10px;
            font-size: 16px;
        }
        
        .btn:hover {
            background: #0056b3;
        }
        
        .btn:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        
        .btn-success {
            background: #28a745;
        }
        
        .btn-success:hover {
            background: #1e7e34;
        }
        
        .file-info {
            background: #e9ecef;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
            text-align: center;
        }
        
        .loading {
            text-align: center;
            margin: 20px 0;
            color: #007bff;
            font-size: 18px;
            display: none;
        }
        
        .results {
            margin-top: 30px;
            padding: 20px;
            border-radius: 5px;
            background: #f8f9fa;
            border: 2px solid #007bff;
            min-height: 100px;
        }
        
        .success {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        
        .error {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
            padding: 15px;
            border-radius: 5px;
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
            border-radius: 5px;
            text-align: center;
            border: 1px solid #dee2e6;
        }
        
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #007bff;
            margin-bottom: 5px;
        }
        
        .stat-label {
            color: #666;
            font-size: 14px;
        }
        
        .uploaded-files {
            background: white;
            border-radius: 5px;
            padding: 15px;
            margin-top: 15px;
        }
        
        .file-item {
            padding: 8px 12px;
            margin: 5px 0;
            background: #f8f9fa;
            border-radius: 3px;
            font-size: 14px;
        }
        
        .file-item.success {
            background: #d4edda;
            color: #155724;
        }
        
        .file-item.error {
            background: #f8d7da;
            color: #721c24;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Sistema Excel → FTP</h1>
        
        <div class="upload-section">
            <input type="file" id="fileInput" accept=".xlsx" style="display: none;">
            <button class="btn" onclick="selectFile()">📁 Selecionar Arquivo</button>
            <button class="btn btn-success" id="processBtn" onclick="processFile()" disabled>🚀 Processar e Enviar para FTP</button>
        </div>
        
        <div id="fileInfo" class="file-info" style="display: none;"></div>
        
        <div class="loading" id="loading">
            ⏳ Processando arquivo e enviando para FTP...
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
            console.log('🚀 Iniciando processamento:', file.name);
            
            const formData = new FormData();
            formData.append('file', file);
            
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');
            
            // Mostrar loading
            loading.style.display = 'block';
            results.innerHTML = '';
            
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
                displayError('Erro no processamento: ' + error.message);
            }
        }

        function displayResults(data) {
            console.log('🎨 Exibindo resultados:', data);
            
            const results = document.getElementById('results');
            
            let html = '';
            
            if (data.success) {
                console.log('✅ Processamento bem-sucedido');
                html += '<div class="success">✅ Arquivo processado e imagens enviadas para FTP com sucesso!</div>';
                
                html += '<div class="stats">';
                html += `<div class="stat-item"><div class="stat-value">${data.stats.total_images || 0}</div><div class="stat-label">🖼️ Imagens extraídas</div></div>`;
                html += `<div class="stat-item"><div class="stat-value">${data.stats.successful_uploads || 0}</div><div class="stat-label">✅ Uploads bem-sucedidos</div></div>`;
                html += `<div class="stat-item"><div class="stat-value">${data.stats.failed_uploads || 0}</div><div class="stat-label">❌ Uploads falharam</div></div>`;
                html += `<div class="stat-item"><div class="stat-value">${(data.stats.total_size / 1024).toFixed(1)} KB</div><div class="stat-label">📏 Total enviado</div></div>`;
                html += '</div>';
                
                if (data.uploaded_files && data.uploaded_files.length > 0) {
                    html += '<div class="uploaded-files">';
                    html += '<div style="font-weight: bold; margin-bottom: 10px;">📁 Arquivos enviados para FTP:</div>';
                    
                    data.uploaded_files.forEach(file => {
                        html += `<div class="file-item success">✅ ${file.filename} (${(file.size / 1024).toFixed(1)} KB) - REF: ${file.ref} - Pos: ${file.position}</div>`;
                    });
                    
                    html += '</div>';
                }
                
                if (data.failed_files && data.failed_files.length > 0) {
                    html += '<div class="uploaded-files">';
                    html += '<div style="font-weight: bold; margin-bottom: 10px;">❌ Arquivos com falha:</div>';
                    
                    data.failed_files.forEach(file => {
                        html += `<div class="file-item error">❌ ${file.filename} - Erro: ${file.error}</div>`;
                    });
                    
                    html += '</div>';
                }
                
            } else {
                console.log('❌ Processamento falhou:', data.error);
                html += '<div class="error">❌ Erro no processamento: ' + (data.error || 'Erro desconhecido') + '</div>';
            }
            
            console.log('📝 HTML gerado:', html);
            results.innerHTML = html;
            console.log('✅ Resultados exibidos na tela');
        }

        function displayError(message) {
            console.log('❌ Exibindo erro:', message);
            const results = document.getElementById('results');
            results.innerHTML = '<div class="error">❌ ' + message + '</div>';
        }
    </script>
</body>
</html>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    """Processa upload de arquivo Excel e envia imagens para FTP"""
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
            # 1. Extrair imagens do Excel
            images = extrair_imagens_do_excel(temp_path)
            
            if not images:
                return jsonify({
                    'success': False,
                    'error': 'Nenhuma imagem encontrada no arquivo'
                }), 400
            
            # 2. Conectar ao FTP e fazer upload
            ftp_uploader = FTPUploader(FTP_CONFIG)
            
            if not ftp_uploader.conectar():
                return jsonify({
                    'success': False,
                    'error': 'Falha na conexão com FTP'
                }), 500
            
            # 3. Fazer upload das imagens
            stats = {
                'total_images': len(images),
                'successful_uploads': 0,
                'failed_uploads': 0,
                'total_size': 0,
                'uploaded_files': [],
                'failed_files': []
            }
            
            for img in images:
                success = ftp_uploader.upload_imagem(img['image_data'], img['ftp_filename'])
                
                if success:
                    stats['successful_uploads'] += 1
                    stats['total_size'] += img['file_size']
                    stats['uploaded_files'].append({
                        'filename': img['ftp_filename'],
                        'size': img['file_size'],
                        'ref': img.get('ref', 'N/A'),
                        'position': img.get('position', 'N/A')
                    })
                else:
                    stats['failed_uploads'] += 1
                    stats['failed_files'].append({
                        'filename': img['ftp_filename'],
                        'error': 'Erro no upload FTP'
                    })
            
            ftp_uploader.desconectar()
            
            # 4. Retornar resultado
            return jsonify({
                'success': stats['successful_uploads'] > 0,
                'stats': stats,
                'message': f"Processadas {stats['total_images']} imagens. {stats['successful_uploads']} enviadas com sucesso para FTP."
            })
                
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
        'ftp_config': {
            'host': FTP_CONFIG['host'],
            'directory': FTP_CONFIG['directory']
        },
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
        'ftp_config': FTP_CONFIG,
        'python_version': sys.version,
        'working_directory': os.getcwd()
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8086))  # Porta diferente para evitar conflito
    debug = os.getenv('FLASK_ENV') != 'production'

    print("🚀 SISTEMA FLASK COM UPLOAD DIRETO PARA FTP")
    print("=" * 60)
    print(f"📁 Frontend: http://localhost:{port}")
    print(f"💚 Health: http://localhost:{port}/health")
    print(f"⚙️  Config: http://localhost:{port}/config")
    print("=" * 60)
    print("🔧 Dependências:")
    print(f"   • Detector Integrado: {'✅' if DETECTOR_INTEGRADO_AVAILABLE else '❌'}")
    print("=" * 60)
    print("🌐 Configuração FTP:")
    print(f"   • Host: {FTP_CONFIG['host']}")
    print(f"   • Usuário: {FTP_CONFIG['user']}")
    print(f"   • Diretório: {FTP_CONFIG['directory']}")
    print("=" * 60)

    if not DETECTOR_INTEGRADO_AVAILABLE:
        logger.error("❌ Detector integrado não disponível.")
        sys.exit(1)

    try:
        logger.info(f"✅ Servidor Flask iniciado!")
        print(f"✅ Servidor Flask iniciado!")
        print(f"🌐 Acesse: http://localhost:{port}")
        print("⚠️  IMPORTANTE: Configure os dados FTP no arquivo antes de usar!")
        app.run(host='0.0.0.0', port=port, debug=debug)
    except Exception as e:
        logger.error(f"❌ Erro ao iniciar servidor Flask: {e}")
        print(f"❌ Erro ao iniciar servidor Flask: {e}")
        sys.exit(1)
