#!/usr/bin/env python3
"""
🚀 SISTEMA FLASK SEGUINDO ORIENTAÇÕES FTP INICIAIS
Sistema que segue exatamente as configurações FTP já estabelecidas no projeto
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

# CONFIGURAÇÕES FTP SEGUINDO ORIENTAÇÕES INICIAIS DO PROJETO
FTP_CONFIG = {
    'host': '46.202.90.62',
    'port': 21,
    'user': 'u715606397.ideolog.ia.br',
    'password': ']X9CC>t~ihWhdzNq',
    'upload_dir': 'public_html/images/products/',
    'timeout': 300
}

# URLs seguindo orientações iniciais
URLS_CONFIG = {
    'domain': 'https://ideolog.ia.br',
    'images_base': 'https://ideolog.ia.br/images/products/',
    'api_base': 'https://ideolog.ia.br/upload.php'
}

# REFs inválidas seguindo orientações iniciais
INVALID_REFS = {
    'TOTAL', 'SUBTOTAL', 'SUM', 'COUNT', 'AVERAGE', 'MAX', 'MIN',
    'TOTAIS', 'SUBTOTAIS', 'SOMA', 'CONTAGEM', 'MÉDIA', 'MÁXIMO', 'MÍNIMO',
    'TOTAL GERAL', 'TOTAL PARCIAL', 'RESUMO', 'SUMMARY'
}

def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class FTPUploaderOrientacoes:
    def __init__(self, config):
        self.config = config
        self.connection = None
    
    def conectar(self):
        """Conecta ao servidor FTP seguindo orientações iniciais"""
        try:
            logger.info(f"🔗 Conectando ao FTP: {self.config['host']}")
            self.connection = ftplib.FTP()
            self.connection.connect(self.config['host'], self.config['port'])
            self.connection.login(self.config['user'], self.config['password'])
            
            # Criar diretórios seguindo estrutura inicial
            self._criar_diretorios()
            
            logger.info("✅ Conectado ao FTP com sucesso!")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao conectar FTP: {e}")
            return False
    
    def _criar_diretorios(self):
        """Cria diretórios seguindo estrutura inicial do projeto"""
        try:
            # Criar public_html se não existir
            try:
                self.connection.mkd('public_html')
                logger.debug("Diretório 'public_html' criado")
            except:
                logger.debug("Diretório 'public_html' já existe")
            
            # Criar images dentro de public_html
            try:
                self.connection.cwd('public_html')
                self.connection.mkd('images')
                logger.debug("Diretório 'images' criado")
            except:
                logger.debug("Diretório 'images' já existe")
            
            # Criar products dentro de images
            try:
                self.connection.cwd('images')
                self.connection.mkd('products')
                logger.debug("Diretório 'products' criado")
            except:
                logger.debug("Diretório 'products' já existe")
            
            # Volta para raiz
            self.connection.cwd('/')
            
        except Exception as e:
            logger.warning(f"Erro ao criar diretórios: {e}")
    
    def desconectar(self):
        """Desconecta do servidor FTP"""
        if self.connection:
            try:
                self.connection.quit()
                logger.info("🔌 Desconectado do FTP")
            except Exception as e:
                logger.warning(f"⚠️ Erro ao desconectar FTP: {e}")
    
    def upload_imagem(self, image_data: bytes, filename: str) -> bool:
        """Faz upload de uma imagem para o FTP seguindo orientações iniciais"""
        try:
            if not self.connection:
                logger.error("❌ Não conectado ao FTP!")
                return False
            
            logger.info(f"📤 Upload: {filename}")
            
            # Criar arquivo temporário
            temp_path = f"/tmp/{filename}"
            with open(temp_path, 'wb') as f:
                f.write(image_data)
            
            # Garantir que estamos no diretório correto
            try:
                self.connection.cwd('/')
                logger.debug("Voltou para diretório raiz")
            except Exception as e:
                logger.warning(f"Erro ao voltar para raiz: {e}")
            
            # Caminho completo seguindo estrutura inicial
            remote_path = f"public_html/images/products/{filename}"
            
            logger.debug(f"Fazendo upload para: {remote_path}")
            
            # Fazer upload para FTP
            with open(temp_path, 'rb') as f:
                self.connection.storbinary(f'STOR {remote_path}', f)
            
            # Verificar se o arquivo foi criado
            try:
                self.connection.cwd('public_html/images/products')
                files_after = self.connection.nlst()
                if filename in files_after:
                    logger.info(f"   ✅ Upload confirmado: {filename} encontrado no servidor")
                else:
                    logger.warning(f"   ⚠️ Upload não confirmado: {filename} não encontrado no servidor")
                
                # Volta para raiz
                self.connection.cwd('/')
            except Exception as e:
                logger.warning(f"Erro ao verificar upload: {e}")
            
            # Remover arquivo temporário
            os.remove(temp_path)
            
            logger.info(f"   ✅ Upload bem-sucedido: {remote_path}")
            logger.info(f"   🌐 Disponível em: {URLS_CONFIG['images_base']}{filename}")
            return True
            
        except Exception as e:
            logger.error(f"   ❌ Erro no upload {filename}: {e}")
            import traceback
            traceback.print_exc()
            return False

def extrair_imagens_do_excel(file_path: str) -> list:
    """Extrai imagens de um arquivo Excel seguindo orientações iniciais"""
    import zipfile
    
    logger.info(f"🔍 Extraindo imagens de: {file_path}")
    images_extracted = []
    
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            # Listar arquivos de mídia
            media_files = [name for name in zf.namelist() if name.startswith('xl/media/') and name.endswith(('.jpg', '.jpeg', '.png'))]
            logger.info(f"🖼️ Arquivos de mídia encontrados: {len(media_files)}")
            
            # Obter posições das imagens usando detector integrado
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
                
                # Criar nome seguindo orientações iniciais: REF.jpg
                if position_info.get('ref'):
                    output_filename = f"{position_info['ref']}.jpg"
                else:
                    # Fallback se não tiver REF
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_filename = f"imagem_{i+1}_{timestamp}.jpg"
                
                image_info = {
                    'original_filename': image_filename,
                    'ftp_filename': output_filename,
                    'image_data': image_data,  # Mantém para upload FTP
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
    """Serve o frontend HTML seguindo orientações iniciais"""
    try:
        html_content = get_frontend_html()
        return html_content
    except Exception as e:
        logger.error(f"Erro ao servir frontend: {e}")
        return jsonify({'error': f'Erro interno: {e}'}), 500

def get_frontend_html():
    """Retorna o HTML do frontend seguindo orientações iniciais"""
    return f'''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Sistema Excel → FTP (Orientações Iniciais)</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: #f0f0f0;
            margin: 0;
            padding: 20px;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }}
        
        .config-info {{
            background: #e3f2fd;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            border-left: 4px solid #2196f3;
        }}
        
        .upload-section {{
            text-align: center;
            margin-bottom: 30px;
        }}
        
        .btn {{
            background: #007bff;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 5px;
            cursor: pointer;
            margin: 10px;
            font-size: 16px;
        }}
        
        .btn:hover {{
            background: #0056b3;
        }}
        
        .btn:disabled {{
            background: #ccc;
            cursor: not-allowed;
        }}
        
        .btn-success {{
            background: #28a745;
        }}
        
        .btn-success:hover {{
            background: #1e7e34;
        }}
        
        .file-info {{
            background: #e9ecef;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
            text-align: center;
        }}
        
        .loading {{
            text-align: center;
            margin: 20px 0;
            color: #007bff;
            font-size: 18px;
            display: none;
        }}
        
        .loading-large {{
            text-align: center;
            margin: 20px 0;
            color: #007bff;
            font-size: 18px;
            padding: 30px;
            background: #f8f9fa;
            border-radius: 10px;
            border: 2px solid #007bff;
        }}
        
        .loading-large h3 {{
            margin: 15px 0;
            color: #0056b3;
        }}
        
        .loading-large p {{
            margin: 10px 0;
            color: #6c757d;
            font-size: 14px;
        }}
        
        .results {{
            margin-top: 30px;
            padding: 20px;
            border-radius: 5px;
            background: #f8f9fa;
            border: 2px solid #007bff;
            min-height: 100px;
        }}
        
        .success {{
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        
        .error {{
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        
        .stat-item {{
            background: white;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
            border: 1px solid #dee2e6;
        }}
        
        .stat-value {{
            font-size: 24px;
            font-weight: bold;
            color: #007bff;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            color: #666;
            font-size: 14px;
        }}
        
        .uploaded-files {{
            background: white;
            border-radius: 5px;
            padding: 15px;
            margin-top: 15px;
        }}
        
        .file-item {{
            padding: 8px 12px;
            margin: 5px 0;
            background: #f8f9fa;
            border-radius: 3px;
            font-size: 14px;
        }}
        
        .file-item.success {{
            background: #d4edda;
            color: #155724;
        }}
        
        .file-item.error {{
            background: #f8d7da;
            color: #721c24;
        }}
        
        .url-link {{
            color: #007bff;
            text-decoration: none;
            font-weight: bold;
        }}
        
        .url-link:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Sistema Excel → FTP</h1>
        <h2 style="text-align: center; color: #666; font-size: 18px;">Seguindo Orientações Iniciais do Projeto</h2>
        
        <div class="config-info">
            <h3>📋 Configuração Atual:</h3>
            <p><strong>🌐 Servidor FTP:</strong> {FTP_CONFIG['host']}</p>
            <p><strong>👤 Usuário:</strong> {FTP_CONFIG['user']}</p>
            <p><strong>📁 Diretório:</strong> {FTP_CONFIG['upload_dir']}</p>
            <p><strong>🔗 URLs:</strong> {URLS_CONFIG['images_base']}</p>
            <p><strong>📊 Coluna REF:</strong> A | <strong>Coluna PHOTO:</strong> H | <strong>Linha inicial:</strong> 4</p>
        </div>
        
        <div class="upload-section">
            <input type="file" id="fileInput" accept=".xlsx" style="display: none;">
            <button class="btn" onclick="selectFile()">📁 Selecionar Arquivo Excel</button>
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
        
        function selectFile() {{
            document.getElementById('fileInput').click();
        }}
        
        document.getElementById('fileInput').addEventListener('change', function(e) {{
            const file = e.target.files[0];
            if (file) {{
                selectedFile = file;
                document.getElementById('processBtn').disabled = false;
                document.getElementById('fileInfo').style.display = 'block';
                document.getElementById('fileInfo').innerHTML = `📄 Arquivo selecionado: <strong>${{file.name}}</strong> (${{(file.size / 1024 / 1024).toFixed(2)}} MB)`;
            }}
        }});

        function processFile() {{
            if (!selectedFile) {{
                alert('Por favor, selecione um arquivo primeiro.');
                return;
            }}
            
            uploadFile(selectedFile);
        }}

        async function uploadFile(file) {{
            console.log('🚀 Iniciando processamento:', file.name);
            
            const formData = new FormData();
            formData.append('file', file);
            
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');
            
            // Mostrar loading com mensagem para arquivos grandes
            loading.style.display = 'block';
            results.innerHTML = '';
            
            // Verificar se é arquivo grande (> 10MB)
            const fileSizeMB = file.size / (1024 * 1024);
            if (fileSizeMB > 10) {{
                loading.innerHTML = `
                    <div class="loading-large">
                        <div class="spinner"></div>
                        <h3>🔄 Processando arquivo grande ({fileSizeMB.toFixed(1)} MB)</h3>
                        <p>⏱️ Este processo pode levar alguns minutos...</p>
                        <p>📊 Extraindo imagens e enviando para FTP...</p>
                    </div>
                `;
            }}
            
            try {{
                console.log('📡 Enviando requisição...');
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 300000); // 5 minutos timeout
                
                const response = await fetch('/upload', {{
                    method: 'POST',
                    body: formData,
                    signal: controller.signal
                }});
                
                clearTimeout(timeoutId);
                
                console.log('📡 Resposta recebida:', response.status);
                
                if (!response.ok) {{
                    throw new Error(`HTTP ${{response.status}}: ${{response.statusText}}`);
                }}
                
                const data = await response.json();
                console.log('📊 Dados recebidos:', data);
                
                // Esconder loading
                loading.style.display = 'none';
                
                // Mostrar resultados
                displayResults(data);
                
            }} catch (error) {{
                console.error('❌ Erro no upload:', error);
                loading.style.display = 'none';
                displayError('Erro no processamento: ' + error.message);
            }}
        }}

        function displayResults(data) {{
            console.log('🎨 Exibindo resultados:', data);
            
            const results = document.getElementById('results');
            
            let html = '';
            
            if (data.success) {{
                console.log('✅ Processamento bem-sucedido');
                html += '<div class="success">✅ Arquivo processado e imagens enviadas para FTP com sucesso!</div>';
                
                html += '<div class="stats">';
                html += `<div class="stat-item"><div class="stat-value">${{data.stats.total_images || 0}}</div><div class="stat-label">🖼️ Imagens extraídas</div></div>`;
                html += `<div class="stat-item"><div class="stat-value">${{data.stats.successful_uploads || 0}}</div><div class="stat-label">✅ Uploads bem-sucedidos</div></div>`;
                html += `<div class="stat-item"><div class="stat-value">${{data.stats.failed_uploads || 0}}</div><div class="stat-label">❌ Uploads falharam</div></div>`;
                html += `<div class="stat-item"><div class="stat-value">${{(data.stats.total_size / 1024).toFixed(1)}} KB</div><div class="stat-label">📏 Total enviado</div></div>`;
                html += '</div>';
                
                if (data.uploaded_files && data.uploaded_files.length > 0) {{
                    html += '<div class="uploaded-files">';
                    html += '<div style="font-weight: bold; margin-bottom: 10px;">📁 Arquivos enviados para FTP:</div>';
                    
                    data.uploaded_files.forEach(file => {{
                        const url = `{URLS_CONFIG['images_base']}${{file.filename}}`;
                        html += `<div class="file-item success">✅ ${{file.filename}} (${{(file.size / 1024).toFixed(1)}} KB) - REF: ${{file.ref}} - Pos: ${{file.position}}</div>`;
                        html += `<div style="margin-left: 20px; margin-bottom: 10px;"><a href="${{url}}" target="_blank" class="url-link">🔗 ${{url}}</a></div>`;
                    }});
                    
                    html += '</div>';
                }}
                
                if (data.failed_files && data.failed_files.length > 0) {{
                    html += '<div class="uploaded-files">';
                    html += '<div style="font-weight: bold; margin-bottom: 10px;">❌ Arquivos com falha:</div>';
                    
                    data.failed_files.forEach(file => {{
                        html += `<div class="file-item error">❌ ${{file.filename}} - Erro: ${{file.error}}</div>`;
                    }});
                    
                    html += '</div>';
                }}
                
            }} else {{
                console.log('❌ Processamento falhou:', data.error);
                html += '<div class="error">❌ Erro no processamento: ' + (data.error || 'Erro desconhecido') + '</div>';
            }}
            
            console.log('📝 HTML gerado:', html);
            results.innerHTML = html;
            console.log('✅ Resultados exibidos na tela');
        }}

        function displayError(message) {{
            console.log('❌ Exibindo erro:', message);
            const results = document.getElementById('results');
            results.innerHTML = '<div class="error">❌ ' + message + '</div>';
        }}
    </script>
</body>
</html>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    """Processa upload de arquivo Excel e envia imagens para FTP seguindo orientações iniciais"""
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
            
            # 2. Conectar ao FTP e fazer upload seguindo orientações iniciais
            ftp_uploader = FTPUploaderOrientacoes(FTP_CONFIG)
            
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
                        'position': img.get('position', 'N/A'),
                        'url': f"{URLS_CONFIG['images_base']}{img['ftp_filename']}"
                    })
                else:
                    stats['failed_uploads'] += 1
                    stats['failed_files'].append({
                        'filename': img['ftp_filename'],
                        'error': 'Erro no upload FTP'
                    })
            
            ftp_uploader.desconectar()
            
            # 4. Retornar resultado seguindo formato das orientações iniciais
            return jsonify({
                'success': stats['successful_uploads'] > 0,
                'stats': stats,
                'message': f"Processadas {stats['total_images']} imagens. {stats['successful_uploads']} enviadas com sucesso para FTP.",
                'images_base_url': URLS_CONFIG['images_base']
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
            'user': FTP_CONFIG['user'],
            'upload_dir': FTP_CONFIG['upload_dir']
        },
        'urls_config': URLS_CONFIG,
        'timestamp': str(os.popen('date').read().strip())
    })

@app.route('/config')
def config():
    """Configuração do sistema seguindo orientações iniciais"""
    return jsonify({
        'max_file_size': '50MB',
        'allowed_extensions': list(ALLOWED_EXTENSIONS),
        'upload_folder': UPLOAD_FOLDER,
        'detector_integrado': DETECTOR_INTEGRADO_AVAILABLE,
        'ftp_config': FTP_CONFIG,
        'urls_config': URLS_CONFIG,
        'invalid_refs': list(INVALID_REFS),
        'excel_config': {
            'ref_column': 'A',
            'photo_column': 'H',
            'start_row': 4
        },
        'python_version': sys.version,
        'working_directory': os.getcwd()
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8087))  # Porta diferente para evitar conflito
    debug = os.getenv('FLASK_ENV') != 'production'

    print("🚀 SISTEMA FLASK SEGUINDO ORIENTAÇÕES FTP INICIAIS")
    print("=" * 60)
    print(f"📁 Frontend: http://localhost:{port}")
    print(f"💚 Health: http://localhost:{port}/health")
    print(f"⚙️  Config: http://localhost:{port}/config")
    print("=" * 60)
    print("🔧 Dependências:")
    print(f"   • Detector Integrado: {'✅' if DETECTOR_INTEGRADO_AVAILABLE else '❌'}")
    print("=" * 60)
    print("🌐 Configuração FTP (Seguindo Orientações Iniciais):")
    print(f"   • Host: {FTP_CONFIG['host']}")
    print(f"   • Usuário: {FTP_CONFIG['user']}")
    print(f"   • Diretório: {FTP_CONFIG['upload_dir']}")
    print(f"   • URLs: {URLS_CONFIG['images_base']}")
    print("=" * 60)
    print("📊 Configuração Excel:")
    print(f"   • Coluna REF: A")
    print(f"   • Coluna PHOTO: H")
    print(f"   • Linha inicial: 4")
    print(f"   • REFs inválidas: {len(INVALID_REFS)} palavras filtradas")
    print("=" * 60)

    if not DETECTOR_INTEGRADO_AVAILABLE:
        logger.error("❌ Detector integrado não disponível.")
        sys.exit(1)

    try:
        logger.info(f"✅ Servidor Flask iniciado!")
        print(f"✅ Servidor Flask iniciado!")
        print(f"🌐 Acesse: http://localhost:{port}")
        print("🎯 Sistema configurado seguindo orientações iniciais do projeto!")
        app.run(host='0.0.0.0', port=port, debug=debug)
    except Exception as e:
        logger.error(f"❌ Erro ao iniciar servidor Flask: {e}")
        print(f"❌ Erro ao iniciar servidor Flask: {e}")
        sys.exit(1)
