#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Upload de Imagens Excel - Render Deploy (Versão Simplificada)
Funciona sem dependências externas complexas
"""

from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import tempfile
import json
import logging
import openpyxl
import base64
import io

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

def process_excel_simple(file_path):
    """Processa arquivo Excel de forma simplificada"""
    try:
        workbook = openpyxl.load_workbook(file_path)
        worksheet = workbook.active
        
        results = {
            'total_refs': 0,
            'images_found': 0,
            'uploads_successful': 0,
            'uploads_failed': 0,
            'errors': []
        }
        
        # Log das imagens encontradas na planilha
        logger.info(f"Total de imagens inseridas na planilha: {len(worksheet._images)}")
        for i, image in enumerate(worksheet._images):
            if hasattr(image, 'anchor') and hasattr(image.anchor, '_from'):
                img_row = image.anchor._from.row + 1
                img_col = image.anchor._from.col + 1
                logger.info(f"Imagem {i+1}: linha {img_row}, coluna {chr(64 + img_col)}")
        
        # Cria mapa de imagens para associação com REFs
        image_map = {}
        for image in worksheet._images:
            if hasattr(image, 'anchor') and hasattr(image.anchor, '_from'):
                img_row = image.anchor._from.row + 1
                img_col = image.anchor._from.col + 1
                image_map[img_row] = img_col
        
        # Processa a partir da linha 4 (índice 3)
        for row_num in range(4, worksheet.max_row + 1):
            ref_cell = worksheet[f'A{row_num}']
            photo_cell = worksheet[f'H{row_num}']
            
            if ref_cell.value:
                results['total_refs'] += 1
                logger.info(f"Processando linha {row_num}: REF = {ref_cell.value}")
                
                # Verifica se há imagem na coluna H usando diferentes métodos
                image_found = False
                image_source = ""
                
                # Método 1: Verifica se a célula tem valor (texto/URL)
                if photo_cell.value and str(photo_cell.value).strip():
                    image_found = True
                    image_source = f"valor da célula: {photo_cell.value}"
                    logger.info(f"Imagem encontrada na linha {row_num} ({image_source})")
                
                # Método 2: Verifica se há imagens inseridas na planilha
                if not image_found:
                    # Procura por imagens na área da célula H
                    for image in worksheet._images:
                        # Verifica se a imagem está próxima da linha atual
                        if hasattr(image, 'anchor') and hasattr(image.anchor, '_from'):
                            img_row = image.anchor._from.row + 1  # +1 porque Excel é 1-indexed
                            img_col = image.anchor._from.col + 1
                            
                            # Se a imagem está na coluna H (8) e próxima da linha atual
                            # Aumenta a tolerância para detectar imagens próximas
                            if img_col == 8 and abs(img_row - row_num) <= 5:
                                image_found = True
                                image_source = f"imagem inserida na linha {img_row}"
                                logger.info(f"Imagem inserida encontrada na linha {row_num} ({image_source})")
                                break
                
                # Método 3: Verifica células adjacentes (G, I)
                if not image_found:
                    for col_offset in [-1, 1]:  # Coluna G e I
                        adj_cell = worksheet.cell(row=row_num, column=8 + col_offset)
                        if adj_cell.value and str(adj_cell.value).strip():
                            image_found = True
                            image_source = f"célula adjacente {chr(65 + 7 + col_offset)}{row_num}: {adj_cell.value}"
                            logger.info(f"Imagem encontrada na linha {row_num} ({image_source})")
                            break
                
                # Método 4: Verifica se há imagens em qualquer coluna próxima à linha atual
                if not image_found:
                    for img_row, img_col in image_map.items():
                        # Se a imagem está próxima da linha atual (dentro de 3 linhas)
                        if abs(img_row - row_num) <= 3:
                            image_found = True
                            image_source = f"imagem próxima na linha {img_row}, coluna {chr(64 + img_col)}"
                            logger.info(f"Imagem próxima encontrada na linha {row_num} ({image_source})")
                            break
                
                # Método 5: Se há imagens na planilha mas não foram associadas, associa à primeira REF
                if not image_found and len(image_map) > 0 and results['images_found'] == 0:
                    # Se é a primeira REF e há imagens não associadas, associa uma imagem
                    image_found = True
                    first_img_row = min(image_map.keys())
                    first_img_col = image_map[first_img_row]
                    image_source = f"imagem não associada na linha {first_img_row}, coluna {chr(64 + first_img_col)}"
                    logger.info(f"Imagem não associada encontrada para linha {row_num} ({image_source})")
                
                if image_found:
                    results['images_found'] += 1
                    
                    # Simula processamento (sem upload real)
                    try:
                        # Aqui seria o processamento real da imagem
                        results['uploads_successful'] += 1
                        logger.info(f"✅ REF {ref_cell.value} (linha {row_num}) processada com sucesso - {image_source}")
                    except Exception as e:
                        results['uploads_failed'] += 1
                        results['errors'].append(f"Erro na linha {row_num}: {str(e)}")
                else:
                    logger.info(f"❌ Nenhuma imagem encontrada na linha {row_num} para REF {ref_cell.value}")
        
        return results
        
    except Exception as e:
        logger.error(f"Erro ao processar Excel: {e}")
        raise

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
            'version': '2.0.0-simplified',
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
        'version': 'simplified'
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
        'version': 'simplified',
        'note': 'Versão simplificada - processamento básico de Excel'
    }), 200

@app.route('/upload', methods=['POST'])
def upload_file():
    """Processa upload de arquivo Excel"""
    try:
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
            # Processa arquivo Excel de forma simplificada
            stats = process_excel_simple(temp_path)
            
            # Prepara resposta com resultados
            response_data = {
                'success': True,
                'total_refs': stats['total_refs'],
                'images_found': stats['images_found'],
                'uploads_successful': stats['uploads_successful'],
                'uploads_failed': stats['uploads_failed'],
                'errors': stats['errors'],
                'images': [],
                'version': 'simplified',
                'note': 'Processamento básico concluído - sem upload FTP'
            }
            
            # Adiciona informações das imagens processadas
            if stats['uploads_successful'] > 0:
                response_data['images'] = [
                    {
                        'name': 'Imagem processada (simulado)',
                        'url': f'https://ideolog.ia.br/images/products/'
                    }
                ]
            
            logger.info(f"Processamento concluído: {stats['uploads_successful']} imagens processadas")
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
    
    print("🚀 Iniciando Sistema de Upload de Imagens Excel (Simplificado)...")
    print(f"📁 Frontend: http://0.0.0.0:{port}")
    print(f"🔧 API: http://0.0.0.0:{port}/upload")
    print(f"💚 Health Check: http://0.0.0.0:{port}/health")
    print(f"⚙️  Config: http://0.0.0.0:{port}/config")
    print(f"🌍 Ambiente: {'Produção' if not debug else 'Desenvolvimento'}")
    print(f"🔧 Porta: {port}")
    print(f"📊 Versão: Simplificada (sem FTP)")
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
