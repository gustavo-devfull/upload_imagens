#!/usr/bin/env python3
"""
🔍 EXTRATOR DE IMAGENS DO EXCEL
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
    
    Args:
        file_path: Caminho para o arquivo Excel
        output_dir: Diretório onde salvar as imagens
    
    Returns:
        Lista de dicionários com informações das imagens extraídas
    """
    logger.info(f"🔍 Extraindo imagens de: {file_path}")
    logger.info(f"📁 Diretório de saída: {output_dir}")
    
    # Criar diretório de saída se não existir
    os.makedirs(output_dir, exist_ok=True)
    
    images_extracted = []
    
    try:
        # Namespaces XML
        ns_xdr = "{http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing}"
        ns_a = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
        ns_r = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
        
        drawing_xml_path = 'xl/drawings/drawing1.xml'
        drawing_rels_path = 'xl/drawings/_rels/drawing1.xml.rels'
        worksheet_xml_path = 'xl/worksheets/sheet1.xml'
        
        with zipfile.ZipFile(file_path, 'r') as zf:
            logger.info(f"📦 Arquivo ZIP aberto: {len(zf.namelist())} arquivos")
            
            # 1. Ler drawing1.xml.rels para mapear rId para nome do arquivo de imagem
            image_id_map = {}
            if drawing_rels_path in zf.namelist():
                with zf.open(drawing_rels_path) as f:
                    tree = ET.parse(f)
                    root = tree.getroot()
                    for rel in root.findall(f"{ns_r}Relationship"):
                        if rel.get('Type') == 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image':
                            r_id = rel.get('Id')
                            target = rel.get('Target')  # e.g., ../media/image1.jpg
                            image_filename = os.path.basename(target)
                            image_id_map[r_id] = image_filename
                            logger.info(f"   • Mapeamento: {r_id} -> {image_filename}")
            else:
                logger.warning(f"⚠️ {drawing_rels_path} não encontrado no arquivo ZIP.")
                return []
            
            # 2. Ler drawing1.xml para encontrar anchors e suas posições
            anchors_data = []
            if drawing_xml_path in zf.namelist():
                with zf.open(drawing_xml_path) as f:
                    tree = ET.parse(f)
                    root = tree.getroot()
                    
                    for anchor in root.findall(f".//{ns_xdr}oneCellAnchor"):
                        from_el = anchor.find(f"{ns_xdr}from")
                        col = int(from_el.find(f"{ns_xdr}col").text)
                        row = int(from_el.find(f"{ns_xdr}row").text) + 1  # 0-based to 1-based
                        col_letter = openpyxl.utils.get_column_letter(col + 1)
                        
                        # Encontrar o blipFill e o r:embed
                        blip_fill = anchor.find(f".//{ns_xdr}pic/{ns_xdr}blipFill")
                        if blip_fill is not None:
                            blip = blip_fill.find(f"{ns_a}blip")
                            if blip is not None:
                                embed_id = blip.get(f"{ns_r}embed")
                                if embed_id and embed_id in image_id_map:
                                    image_filename = image_id_map[embed_id]
                                    anchors_data.append({
                                        'col': col_letter,
                                        'row': row,
                                        'embed_id': embed_id,
                                        'image_filename': image_filename,
                                        'element': anchor
                                    })
                                    logger.info(f"   • Anchor encontrado: {col_letter}{row} -> {image_filename}")
            
            # 3. Extrair e salvar as imagens
            logger.info(f"🖼️ Extraindo {len(anchors_data)} imagens...")
            
            for i, anchor_data in enumerate(anchors_data):
                image_filename = anchor_data['image_filename']
                media_path = f'xl/media/{image_filename}'
                
                if media_path in zf.namelist():
                    # Ler dados da imagem
                    with zf.open(media_path) as img_file:
                        image_data = img_file.read()
                    
                    # Criar nome único para o arquivo
                    ref_value = f"REF_{anchor_data['row']}"  # Usar linha como REF temporário
                    output_filename = f"{ref_value}_{image_filename}"
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
                        'position': f"{anchor_data['col']}{anchor_data['row']}",
                        'embed_id': anchor_data['embed_id'],
                        'file_size': file_size,
                        'ref': ref_value
                    }
                    
                    images_extracted.append(image_info)
                    
                    logger.info(f"   ✅ Imagem {i+1} salva:")
                    logger.info(f"      📁 Arquivo: {output_filename}")
                    logger.info(f"      📍 Posição: {anchor_data['col']}{anchor_data['row']}")
                    logger.info(f"      📏 Tamanho: {file_size:,} bytes")
                    logger.info(f"      💾 Caminho: {output_path}")
                else:
                    logger.warning(f"   ❌ Arquivo de mídia não encontrado: {media_path}")
            
            logger.info(f"🎉 Extração concluída! {len(images_extracted)} imagens salvas em '{output_dir}'")
            return images_extracted
            
    except Exception as e:
        logger.error(f"❌ Erro na extração: {e}")
        return []

def obter_ref_real(file_path: str, row: int) -> str:
    """Obtém a REF real da linha especificada"""
    try:
        workbook = openpyxl.load_workbook(file_path)
        worksheet = workbook.active
        ref_cell = worksheet[f'A{row}']
        ref_value = str(ref_cell.value).strip() if ref_cell.value else f"LINHA_{row}"
        workbook.close()
        return ref_value
    except Exception as e:
        logger.warning(f"Erro ao obter REF da linha {row}: {e}")
        return f"LINHA_{row}"

def main():
    """Função principal"""
    print("🔍 EXTRATOR DE IMAGENS DO EXCEL")
    print("=" * 50)
    
    # Arquivo para processar
    file_path = "produtos_novos.xlsx"
    
    if not os.path.exists(file_path):
        print(f"❌ Arquivo {file_path} não encontrado!")
        return
    
    print(f"📁 Processando: {file_path}")
    print("=" * 50)
    
    # Extrair imagens
    images = extrair_imagens_do_excel(file_path)
    
    if images:
        print("\n📊 RESUMO DA EXTRAÇÃO:")
        print("=" * 50)
        
        for i, img in enumerate(images, 1):
            print(f"\n🖼️ Imagem {i}:")
            print(f"   📁 Arquivo original: {img['original_filename']}")
            print(f"   💾 Arquivo salvo: {img['saved_filename']}")
            print(f"   📍 Posição Excel: {img['position']}")
            print(f"   📏 Tamanho: {img['file_size']:,} bytes")
            print(f"   🔗 Embed ID: {img['embed_id']}")
            print(f"   📂 Caminho completo: {img['saved_path']}")
        
        print(f"\n✅ Total: {len(images)} imagens extraídas com sucesso!")
        print(f"📁 Localização: {os.path.abspath('imagens_extraidas')}")
        
        # Listar arquivos no diretório
        print(f"\n📋 ARQUIVOS NO DIRETÓRIO:")
        if os.path.exists('imagens_extraidas'):
            for file in os.listdir('imagens_extraidas'):
                file_path_full = os.path.join('imagens_extraidas', file)
                file_size = os.path.getsize(file_path_full)
                print(f"   • {file} ({file_size:,} bytes)")
    else:
        print("❌ Nenhuma imagem foi extraída!")

if __name__ == "__main__":
    main()

