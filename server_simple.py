#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor Flask simples para Railway
"""

from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    """Página inicial"""
    return jsonify({
        'status': 'ok', 
        'message': 'Sistema de Upload de Imagens Excel',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'config': '/config',
            'upload': '/upload'
        }
    }), 200

@app.route('/health')
def health_check():
    """Endpoint de verificação de saúde"""
    return jsonify({
        'status': 'ok', 
        'message': 'Servidor funcionando',
        'environment': os.getenv('FLASK_ENV', 'development'),
        'port': os.getenv('PORT', '8080')
    }), 200

@app.route('/config')
def get_config():
    """Retorna configurações do sistema"""
    return jsonify({
        'ftp_host': os.getenv('FTP_HOST', 'not_configured'),
        'ftp_user': os.getenv('FTP_USER', 'not_configured'),
        'domain': 'https://ideolog.ia.br',
        'upload_path': 'images/products/',
        'max_file_size': '50MB',
        'allowed_extensions': ['xlsx']
    }), 200

@app.route('/upload', methods=['POST'])
def upload_file():
    """Endpoint de upload (simplificado)"""
    return jsonify({
        'error': 'Sistema em manutenção. Configure as variáveis de ambiente FTP.'
    }), 503

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    debug = os.getenv('FLASK_ENV') != 'production'
    
    print("🚀 Iniciando servidor Flask simples...")
    print(f"🌍 Ambiente: {'Produção' if not debug else 'Desenvolvimento'}")
    print(f"🔧 Porta: {port}")
    print(f"💚 Health Check: http://localhost:{port}/health")
    print()
    
    app.run(host='0.0.0.0', port=port, debug=debug)
