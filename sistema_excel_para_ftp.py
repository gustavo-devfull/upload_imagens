#!/usr/bin/env python3
"""
🚀 SISTEMA COMPLETO: EXCEL → IMAGENS → FTP
Sistema que extrai imagens do Excel e salva diretamente no FTP
"""

import zipfile
import xml.etree.ElementTree as ET
import openpyxl
import openpyxl.utils
import os
import logging
import ftplib
from typing import List, Dict, Optional
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

class SistemaExcelParaFTP:
    def __init__(self, ftp_host: str, ftp_user: str, ftp_pass: str, ftp_dir: str = "/"):
        """
        Inicializa o sistema de upload para FTP
        
        Args:
            ftp_host: Servidor FTP
            ftp_user: Usuário FTP
            ftp_pass: Senha FTP
            ftp_dir: Diretório no FTP (padrão: /)
        """
        self.ftp_host = ftp_host
        self.ftp_user = ftp_user
        self.ftp_pass = ftp_pass
        self.ftp_dir = ftp_dir
        self.ftp_connection = None
        
    def conectar_ftp(self) -> bool:
        """Conecta ao servidor FTP"""
        try:
            logger.info(f"🔗 Conectando ao FTP: {self.ftp_host}")
            self.ftp_connection = ftplib.FTP()
            self.ftp_connection.connect(self.ftp_host, 21)
            self.ftp_connection.login(self.ftp_user, self.ftp_pass)
            self.ftp_connection.cwd(self.ftp_dir)
            logger.info("✅ Conectado ao FTP com sucesso!")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao conectar FTP: {e}")
            return False
    
    def desconectar_ftp(self):
        """Desconecta do servidor FTP"""
        if self.ftp_connection:
            try:
                self.ftp_connection.quit()
                logger.info("🔌 Desconectado do FTP")
            except Exception as e:
                logger.warning(f"⚠️ Erro ao desconectar FTP: {e}")
    
    def extrair_imagens_do_excel(self, file_path: str) -> List[Dict]:
        """
        Extrai imagens de um arquivo Excel
        
        Args:
            file_path: Caminho para o arquivo Excel
            
        Returns:
            Lista de dicionários com informações das imagens
        """
        logger.info(f"🔍 Extraindo imagens de: {file_path}")
        
        images_extracted = []
        
        try:
            with zipfile.ZipFile(file_path, 'r') as zf:
                logger.info(f"📦 Arquivo ZIP aberto: {len(zf.namelist())} arquivos")
                
                # Listar arquivos de mídia
                media_files = [name for name in zf.namelist() if name.startswith('xl/media/') and name.endswith(('.jpg', '.jpeg', '.png'))]
                logger.info(f"🖼️ Arquivos de mídia encontrados: {len(media_files)}")
                
                # Obter posições das imagens usando detector integrado
                positions = self.obter_posicoes_imagens(file_path)
                
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
                        'media_path': media_file,
                        'index': i + 1,
                        **position_info
                    }
                    
                    images_extracted.append(image_info)
                    
                    logger.info(f"   ✅ Imagem {i+1} preparada:")
                    logger.info(f"      📁 Arquivo: {output_filename}")
                    logger.info(f"      📏 Tamanho: {len(image_data):,} bytes")
                    if position_info.get('position'):
                        logger.info(f"      📍 Posição: {position_info['position']}")
                        logger.info(f"      🔢 REF: {position_info['ref']}")
                
                logger.info(f"🎉 {len(images_extracted)} imagens extraídas e preparadas!")
                return images_extracted
                
        except Exception as e:
            logger.error(f"❌ Erro na extração: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def obter_posicoes_imagens(self, file_path: str) -> List[Dict]:
        """Obtém as posições das imagens no Excel usando o detector integrado"""
        try:
            from detector_integrado import DetectorImagensIntegrado
            
            detector = DetectorImagensIntegrado(debug_mode=False)
            images = detector.detectar_imagens(file_path, target_columns=['H'], start_row=4, ref_column='A')
            
            logger.info(f"📍 Posições detectadas: {len(images)}")
            for img in images:
                logger.info(f"   • REF: {img['ref']} | Posição: {img['col']}{img['row']} | Arquivo: {img.get('image_filename', 'N/A')}")
            
            return images
        except Exception as e:
            logger.error(f"❌ Erro ao obter posições: {e}")
            return []
    
    def upload_imagens_para_ftp(self, images: List[Dict]) -> Dict:
        """
        Faz upload das imagens para o FTP
        
        Args:
            images: Lista de imagens extraídas
            
        Returns:
            Dicionário com estatísticas do upload
        """
        if not self.ftp_connection:
            logger.error("❌ Não conectado ao FTP!")
            return {'success': False, 'error': 'Não conectado ao FTP'}
        
        stats = {
            'total_images': len(images),
            'successful_uploads': 0,
            'failed_uploads': 0,
            'uploaded_files': [],
            'failed_files': [],
            'total_size': 0
        }
        
        logger.info(f"🚀 Iniciando upload de {len(images)} imagens para FTP...")
        
        for i, img in enumerate(images, 1):
            try:
                logger.info(f"📤 Upload {i}/{len(images)}: {img['ftp_filename']}")
                
                # Criar arquivo temporário
                temp_path = f"/tmp/{img['ftp_filename']}"
                with open(temp_path, 'wb') as f:
                    f.write(img['image_data'])
                
                # Fazer upload para FTP
                with open(temp_path, 'rb') as f:
                    self.ftp_connection.storbinary(f'STOR {img["ftp_filename"]}', f)
                
                # Remover arquivo temporário
                os.remove(temp_path)
                
                stats['successful_uploads'] += 1
                stats['total_size'] += img['file_size']
                stats['uploaded_files'].append({
                    'filename': img['ftp_filename'],
                    'size': img['file_size'],
                    'ref': img.get('ref', 'N/A'),
                    'position': img.get('position', 'N/A')
                })
                
                logger.info(f"   ✅ Upload bem-sucedido!")
                logger.info(f"      📁 Arquivo: {img['ftp_filename']}")
                logger.info(f"      📏 Tamanho: {img['file_size']:,} bytes")
                if img.get('position'):
                    logger.info(f"      📍 Posição: {img['position']}")
                    logger.info(f"      🔢 REF: {img['ref']}")
                
            except Exception as e:
                logger.error(f"   ❌ Erro no upload: {e}")
                stats['failed_uploads'] += 1
                stats['failed_files'].append({
                    'filename': img['ftp_filename'],
                    'error': str(e)
                })
        
        logger.info(f"🎉 Upload concluído!")
        logger.info(f"   ✅ Sucessos: {stats['successful_uploads']}")
        logger.info(f"   ❌ Falhas: {stats['failed_uploads']}")
        logger.info(f"   📏 Total enviado: {stats['total_size']:,} bytes")
        
        return stats
    
    def processar_arquivo_completo(self, file_path: str) -> Dict:
        """
        Processa um arquivo Excel completo: extrai imagens e faz upload para FTP
        
        Args:
            file_path: Caminho para o arquivo Excel
            
        Returns:
            Dicionário com resultado completo do processamento
        """
        logger.info("🚀 INICIANDO PROCESSAMENTO COMPLETO")
        logger.info("=" * 60)
        logger.info(f"📁 Arquivo: {file_path}")
        logger.info(f"🌐 FTP: {self.ftp_host}")
        logger.info("=" * 60)
        
        result = {
            'success': False,
            'file_path': file_path,
            'ftp_host': self.ftp_host,
            'images_extracted': 0,
            'upload_stats': {},
            'error': None
        }
        
        try:
            # 1. Conectar ao FTP
            if not self.conectar_ftp():
                result['error'] = 'Falha na conexão FTP'
                return result
            
            # 2. Extrair imagens do Excel
            images = self.extrair_imagens_do_excel(file_path)
            result['images_extracted'] = len(images)
            
            if not images:
                result['error'] = 'Nenhuma imagem encontrada no arquivo'
                return result
            
            # 3. Fazer upload para FTP
            upload_stats = self.upload_imagens_para_ftp(images)
            result['upload_stats'] = upload_stats
            
            # 4. Verificar sucesso
            if upload_stats['successful_uploads'] > 0:
                result['success'] = True
                logger.info("🎉 PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
            else:
                result['error'] = 'Nenhuma imagem foi enviada com sucesso'
            
        except Exception as e:
            logger.error(f"❌ Erro no processamento: {e}")
            result['error'] = str(e)
        
        finally:
            # Desconectar do FTP
            self.desconectar_ftp()
        
        return result

def main():
    """Função principal para teste"""
    print("🚀 SISTEMA COMPLETO: EXCEL → IMAGENS → FTP")
    print("=" * 60)
    
    # Configurações FTP (substitua pelos seus dados)
    FTP_HOST = "seu-servidor-ftp.com"
    FTP_USER = "seu-usuario"
    FTP_PASS = "sua-senha"
    FTP_DIR = "/uploads/"
    
    # Arquivo para processar
    file_path = "produtos_novos.xlsx"
    
    if not os.path.exists(file_path):
        print(f"❌ Arquivo {file_path} não encontrado!")
        return
    
    print(f"📁 Processando: {file_path}")
    print(f"🌐 FTP: {FTP_HOST}")
    print("=" * 60)
    
    # Criar sistema
    sistema = SistemaExcelParaFTP(FTP_HOST, FTP_USER, FTP_PASS, FTP_DIR)
    
    # Processar arquivo
    result = sistema.processar_arquivo_completo(file_path)
    
    # Exibir resultado
    print("\n📊 RESULTADO FINAL:")
    print("=" * 60)
    
    if result['success']:
        print("✅ SUCESSO!")
        print(f"📁 Arquivo processado: {result['file_path']}")
        print(f"🖼️ Imagens extraídas: {result['images_extracted']}")
        print(f"📤 Uploads bem-sucedidos: {result['upload_stats']['successful_uploads']}")
        print(f"❌ Uploads falharam: {result['upload_stats']['failed_uploads']}")
        print(f"📏 Total enviado: {result['upload_stats']['total_size']:,} bytes")
        
        print("\n📋 ARQUIVOS ENVIADOS:")
        for file_info in result['upload_stats']['uploaded_files']:
            print(f"   • {file_info['filename']} ({file_info['size']:,} bytes) - REF: {file_info['ref']} - Pos: {file_info['position']}")
        
        if result['upload_stats']['failed_files']:
            print("\n❌ ARQUIVOS COM FALHA:")
            for file_info in result['upload_stats']['failed_files']:
                print(f"   • {file_info['filename']} - Erro: {file_info['error']}")
    else:
        print("❌ FALHA!")
        print(f"Erro: {result['error']}")

if __name__ == "__main__":
    main()

