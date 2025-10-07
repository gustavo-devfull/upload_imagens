#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema Completo de Upload de Imagens Excel - Render Deploy
"""

from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import tempfile
import json
import logging

# Importação condicional para evitar erros no Render
try:
    from upload_ftp_corrigido import FTPImageExtractorCorrigido
    FTP_AVAILABLE = True
except ImportError as e:
    logging.warning(f"FTP module not available: {e}")
    FTP_AVAILABLE = False

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Configurações FTP (usando variáveis de ambiente para segurança)
FTP_HOST = os.getenv('FTP_HOST', "46.202.90.62")
FTP_USER = os.getenv('FTP_USER', "u715606397.ideolog.ia.br")
FTP_PASSWORD = os.getenv('FTP_PASSWORD', "]X9CC>t~ihWhdzNq")

# Diretório para uploads temporários (compatível com Render)
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', '/tmp/excel_uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'xlsx'}

def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def serve_frontend():
    """Serve o frontend ou página inicial"""
    try:
        return send_from_directory('.', 'frontend.html')
    except Exception as e:
        logger.error(f"Erro ao servir frontend: {e}")
        return jsonify({
            'status': 'ok', 
            'message': 'Sistema de Upload de Imagens Excel',
            'version': '2.0.0',
            'ftp_available': FTP_AVAILABLE,
            'endpoints': {
                'health': '/health',
                'config': '/config',
                'upload': '/upload'
            },
            'frontend_error': str(e)
        }), 200

@app.route('/health')
def health_check():
    """Endpoint de verificação de saúde"""
    return jsonify({
        'status': 'ok', 
        'message': 'Servidor funcionando',
        'environment': os.getenv('FLASK_ENV', 'development'),
        'port': os.getenv('PORT', '8080'),
        'ftp_available': FTP_AVAILABLE
    }), 200

@app.route('/config')
def get_config():
    """Retorna configurações do sistema"""
    return jsonify({
        'ftp_host': FTP_HOST,
        'ftp_user': FTP_USER,
        'domain': 'https://ideolog.ia.br',
        'upload_path': 'images/products/',
        'max_file_size': '50MB',
        'allowed_extensions': list(ALLOWED_EXTENSIONS),
        'ftp_available': FTP_AVAILABLE
    }), 200

@app.route('/upload', methods=['POST'])
def upload_file():
    """Processa upload de arquivo Excel"""
    try:
        # Verifica se FTP está disponível
        if not FTP_AVAILABLE:
            return jsonify({
                'error': 'Sistema FTP não disponível no momento. Verifique as variáveis de ambiente.',
                'ftp_available': False
            }), 503
        
        # Verifica se há arquivo na requisição
        if 'excel_file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['excel_file']
        
        # Verifica se arquivo foi selecionado
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        # Verifica se arquivo é permitido
        if not allowed_file(file.filename):
            return jsonify({'error': 'Apenas arquivos .xlsx são permitidos'}), 400
        
        # Salva arquivo temporariamente
        filename = secure_filename(file.filename)
        temp_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(temp_path)
        
        logger.info(f"Arquivo salvo temporariamente: {temp_path}")
        
        try:
            # Processa arquivo com o sistema FTP
            extractor = FTPImageExtractorCorrigido(FTP_HOST, FTP_USER, FTP_PASSWORD)
            stats = extractor.process_excel_file(temp_path, start_row=4, photo_column='H')
            
            # Prepara resposta com resultados
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
                        'url': f'https://ideolog.ia.br/images/products/'
                    }
                ]
            
            logger.info(f"Processamento concluído: {stats['uploads_successful']} uploads bem-sucedidos")
            return jsonify(response_data)
            
        except Exception as e:
            logger.error(f"Erro no processamento: {e}")
            return jsonify({'error': f'Erro no processamento: {str(e)}'}), 500
            
        finally:
            # Remove arquivo temporário
            try:
                os.remove(temp_path)
                logger.info(f"Arquivo temporário removido: {temp_path}")
            except Exception as e:
                logger.warning(f"Erro ao remover arquivo temporário: {e}")
    
    except Exception as e:
        logger.error(f"Erro geral no upload: {e}")
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

@app.errorhandler(413)
def too_large(e):
    """Trata arquivos muito grandes"""
    return jsonify({'error': 'Arquivo muito grande. Máximo permitido: 50MB'}), 413

@app.errorhandler(404)
def not_found(e):
    """Trata rotas não encontradas"""
    return jsonify({'error': 'Rota não encontrada'}), 404

@app.errorhandler(500)
def internal_error(e):
    """Trata erros internos"""
    return jsonify({'error': 'Erro interno do servidor'}), 500

if __name__ == '__main__':
    # Detecta se está rodando em produção ou desenvolvimento
    port = int(os.getenv('PORT', 8080))
    debug = os.getenv('FLASK_ENV') != 'production'
    
    print("🚀 Iniciando Sistema de Upload de Imagens Excel...")
    print(f"📁 Frontend: http://localhost:{port}")
    print(f"🔧 API: http://localhost:{port}/upload")
    print(f"💚 Health Check: http://localhost:{port}/health")
    print(f"⚙️  Config: http://localhost:{port}/config")
    print(f"🌍 Ambiente: {'Produção' if not debug else 'Desenvolvimento'}")
    print(f"🔧 Porta: {port}")
    print(f"📡 FTP Disponível: {FTP_AVAILABLE}")
    print()
    
    # Cria diretório de uploads se não existir
    try:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        print(f"✅ Diretório de uploads criado: {UPLOAD_FOLDER}")
    except Exception as e:
        print(f"⚠️  Erro ao criar diretório de uploads: {e}")
    
    # Inicia servidor
    try:
        app.run(host='0.0.0.0', port=port, debug=debug)
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        raise
