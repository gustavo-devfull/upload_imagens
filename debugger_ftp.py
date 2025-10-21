#!/usr/bin/env python3
"""
🔍 DEBUGGER FTP - Verificar problema no upload
"""

import zipfile
import xml.etree.ElementTree as ET
import openpyxl
import openpyxl.utils
import os
import logging
import ftplib
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

def debug_extracao_imagens(file_path: str):
    """Debug da extração de imagens"""
    print("🔍 DEBUG: EXTRAÇÃO DE IMAGENS")
    print("=" * 50)
    
    images_extracted = []
    
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            print(f"📦 Arquivo ZIP aberto: {len(zf.namelist())} arquivos")
            
            # Listar arquivos de mídia
            media_files = [name for name in zf.namelist() if name.startswith('xl/media/') and name.endswith(('.jpg', '.jpeg', '.png'))]
            print(f"🖼️ Arquivos de mídia encontrados: {len(media_files)}")
            
            for i, media_file in enumerate(media_files):
                print(f"   {i+1}. {media_file}")
            
            # Obter posições das imagens usando detector integrado
            print("\n📍 Obtendo posições das imagens...")
            try:
                from detector_integrado import DetectorImagensIntegrado
                detector = DetectorImagensIntegrado(debug_mode=False)
                positions = detector.detectar_imagens(file_path, target_columns=['H'], start_row=4, ref_column='A')
                print(f"   ✅ {len(positions)} posições detectadas")
                
                for pos in positions:
                    print(f"      • REF: {pos['ref']} | Posição: {pos['col']}{pos['row']}")
                
            except Exception as e:
                print(f"   ❌ Erro ao obter posições: {e}")
                positions = []
            
            # Extrair imagens
            print(f"\n🖼️ Extraindo {len(media_files)} imagens...")
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
                    'image_data': image_data,
                    'file_size': len(image_data),
                    'index': i + 1,
                    **position_info
                }
                
                images_extracted.append(image_info)
                
                print(f"   ✅ Imagem {i+1}:")
                print(f"      📁 Arquivo original: {image_filename}")
                print(f"      📁 Arquivo FTP: {output_filename}")
                print(f"      📏 Tamanho: {len(image_data):,} bytes")
                if position_info.get('position'):
                    print(f"      📍 Posição: {position_info['position']}")
                    print(f"      🔢 REF: {position_info['ref']}")
            
            print(f"\n🎉 {len(images_extracted)} imagens extraídas!")
            return images_extracted
            
    except Exception as e:
        print(f"❌ Erro na extração: {e}")
        import traceback
        traceback.print_exc()
        return []

def debug_upload_ftp(images):
    """Debug do upload FTP"""
    print("\n🔍 DEBUG: UPLOAD FTP")
    print("=" * 50)
    
    # Configurações FTP
    FTP_HOST = "46.202.90.62"
    FTP_USER = "u715606397.ideolog.ia.br"
    FTP_PASS = "]X9CC>t~ihWhdzNq"
    
    try:
        print("🔗 Conectando ao FTP...")
        ftp = ftplib.FTP()
        ftp.connect(FTP_HOST, 21)
        ftp.login(FTP_USER, FTP_PASS)
        
        print("✅ Conectado ao FTP!")
        
        # Criar diretórios
        print("📁 Criando diretórios...")
        try:
            ftp.mkd('public_html')
            print("   ✅ public_html criado")
        except:
            print("   ℹ️ public_html já existe")
        
        try:
            ftp.cwd('public_html')
            ftp.mkd('images')
            print("   ✅ images criado")
        except:
            print("   ℹ️ images já existe")
        
        try:
            ftp.cwd('images')
            ftp.mkd('products')
            print("   ✅ products criado")
        except:
            print("   ℹ️ products já existe")
        
        # Volta para raiz
        ftp.cwd('/')
        
        # Upload das imagens
        print(f"\n📤 Fazendo upload de {len(images)} imagens...")
        successful_uploads = 0
        
        for i, img in enumerate(images, 1):
            try:
                print(f"\n   📤 Upload {i}/{len(images)}: {img['ftp_filename']}")
                
                # Criar arquivo temporário
                temp_path = f"/tmp/{img['ftp_filename']}"
                with open(temp_path, 'wb') as f:
                    f.write(img['image_data'])
                
                # Caminho completo
                remote_path = f"public_html/images/products/{img['ftp_filename']}"
                
                # Fazer upload
                with open(temp_path, 'rb') as f:
                    ftp.storbinary(f'STOR {remote_path}', f)
                
                # Remover arquivo temporário
                os.remove(temp_path)
                
                print(f"      ✅ Upload bem-sucedido!")
                print(f"      📁 Arquivo: {remote_path}")
                print(f"      📏 Tamanho: {img['file_size']:,} bytes")
                if img.get('position'):
                    print(f"      📍 Posição: {img['position']}")
                    print(f"      🔢 REF: {img['ref']}")
                
                successful_uploads += 1
                
            except Exception as e:
                print(f"      ❌ Erro no upload: {e}")
        
        ftp.quit()
        
        print(f"\n🎉 Upload concluído!")
        print(f"   ✅ Sucessos: {successful_uploads}")
        print(f"   ❌ Falhas: {len(images) - successful_uploads}")
        
        return successful_uploads > 0
        
    except Exception as e:
        print(f"❌ Erro na conexão FTP: {e}")
        return False

def main():
    """Função principal de debug"""
    print("🔍 DEBUGGER FTP - VERIFICANDO PROBLEMA NO UPLOAD")
    print("=" * 60)
    
    # Arquivo para testar
    file_path = "produtos_novos.xlsx"
    
    if not os.path.exists(file_path):
        print(f"❌ Arquivo {file_path} não encontrado!")
        return
    
    print(f"📁 Testando arquivo: {file_path}")
    
    # 1. Debug da extração
    images = debug_extracao_imagens(file_path)
    
    if not images:
        print("❌ Nenhuma imagem extraída!")
        return
    
    # 2. Debug do upload
    success = debug_upload_ftp(images)
    
    if success:
        print("\n🎉 DEBUG CONCLUÍDO COM SUCESSO!")
        print("✅ O sistema está funcionando corretamente!")
    else:
        print("\n❌ DEBUG FALHOU!")
        print("❌ Há problemas no upload FTP!")

if __name__ == "__main__":
    main()

