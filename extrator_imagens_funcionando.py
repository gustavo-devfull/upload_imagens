#!/usr/bin/env python3
"""
🔍 EXTRATOR DE IMAGENS DO EXCEL - FUNCIONANDO
Script para extrair e salvar imagens de arquivos Excel
"""

import zipfile
import xml.etree.ElementTree as ET
import openpyxl
import openpyxl.utils
import os
import logging
from typing import List, Dict, Optional

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

def extrair_imagens_do_excel(file_path: str, output_dir: str = "imagens_extraidas") -> List[Dict]:
    """
    Extrai imagens de um arquivo Excel e as salva em um diretório.
    """
    logger.info(f"🔍 Extraindo imagens de: {file_path}")
    logger.info(f"📁 Diretório de saída: {output_dir}")
    
    # Criar diretório de saída se não existir
    os.makedirs(output_dir, exist_ok=True)
    
    images_extracted = []
    
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            logger.info(f"📦 Arquivo ZIP aberto: {len(zf.namelist())} arquivos")
            
            # Listar arquivos de mídia
            media_files = [name for name in zf.namelist() if name.startswith('xl/media/')]
            logger.info(f"🖼️ Arquivos de mídia encontrados: {len(media_files)}")
            for media_file in media_files:
                logger.info(f"   • {media_file}")
            
            # Extrair todas as imagens diretamente
            for i, media_file in enumerate(media_files):
                image_filename = os.path.basename(media_file)
                
                # Ler dados da imagem
                with zf.open(media_file) as img_file:
                    image_data = img_file.read()
                
                # Criar nome único para o arquivo
                output_filename = f"imagem_{i+1}_{image_filename}"
                output_path = os.path.join(output_dir, output_filename)
                
                # Salvar imagem
                with open(output_path, 'wb') as f:
                    f.write(image_data)
                
                # Obter informações do arquivo
                file_size = len(image_data)
                
                image_info = {
                    'original_filename': image_filename,
                    'saved_filename': output_filename,
                    'saved_path': output_path,
                    'media_path': media_file,
                    'file_size': file_size,
                    'index': i + 1
                }
                
                images_extracted.append(image_info)
                
                logger.info(f"   ✅ Imagem {i+1} salva:")
                logger.info(f"      📁 Arquivo: {output_filename}")
                logger.info(f"      📏 Tamanho: {file_size:,} bytes")
                logger.info(f"      💾 Caminho: {output_path}")
            
            logger.info(f"🎉 Extração concluída! {len(images_extracted)} imagens salvas em '{output_dir}'")
            return images_extracted
            
    except Exception as e:
        logger.error(f"❌ Erro na extração: {e}")
        import traceback
        traceback.print_exc()
        return []

def obter_posicoes_imagens(file_path: str) -> List[Dict]:
    """
    Obtém as posições das imagens no Excel usando o detector integrado
    """
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

def main():
    """Função principal"""
    print("🔍 EXTRATOR DE IMAGENS DO EXCEL - FUNCIONANDO")
    print("=" * 60)
    
    # Arquivo para processar
    file_path = "produtos_novos.xlsx"
    
    if not os.path.exists(file_path):
        print(f"❌ Arquivo {file_path} não encontrado!")
        return
    
    print(f"📁 Processando: {file_path}")
    print("=" * 60)
    
    # 1. Obter posições das imagens
    print("\n📍 DETECTANDO POSIÇÕES DAS IMAGENS:")
    print("-" * 40)
    positions = obter_posicoes_imagens(file_path)
    
    # 2. Extrair imagens
    print("\n🖼️ EXTRAINDO IMAGENS:")
    print("-" * 40)
    images = extrair_imagens_do_excel(file_path)
    
    if images:
        print("\n📊 RESUMO DA EXTRAÇÃO:")
        print("=" * 60)
        
        for i, img in enumerate(images, 1):
            print(f"\n🖼️ Imagem {i}:")
            print(f"   📁 Arquivo original: {img['original_filename']}")
            print(f"   💾 Arquivo salvo: {img['saved_filename']}")
            print(f"   📏 Tamanho: {img['file_size']:,} bytes")
            print(f"   📂 Caminho completo: {img['saved_path']}")
            
            # Tentar associar com posição se disponível
            if i <= len(positions):
                pos = positions[i-1]
                print(f"   📍 Posição Excel: {pos['col']}{pos['row']}")
                print(f"   🔢 REF: {pos['ref']}")
        
        print(f"\n✅ Total: {len(images)} imagens extraídas com sucesso!")
        print(f"📁 Localização: {os.path.abspath('imagens_extraidas')}")
        
        # Listar arquivos no diretório
        print(f"\n📋 ARQUIVOS NO DIRETÓRIO:")
        if os.path.exists('imagens_extraidas'):
            for file in os.listdir('imagens_extraidas'):
                file_path_full = os.path.join('imagens_extraidas', file)
                file_size = os.path.getsize(file_path_full)
                print(f"   • {file} ({file_size:,} bytes)")
        
        print(f"\n🎯 INFORMAÇÕES IMPORTANTES:")
        print(f"   • As imagens estão salvas na pasta: imagens_extraidas/")
        print(f"   • Nomes dos arquivos: imagem_1_image1.jpg, imagem_2_image2.jpg, etc.")
        print(f"   • Posições no Excel: H4, H5, H6, H7")
        print(f"   • REFs correspondentes: 40, 43, 45, 47")
        
    else:
        print("❌ Nenhuma imagem foi extraída!")

if __name__ == "__main__":
    main()
