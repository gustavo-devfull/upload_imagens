#!/usr/bin/env python3
"""
🔍 DETECTOR CORRIGIDO DE IMAGENS EXCEL
Detector corrigido que funciona com o namespace correto (xdr:)
"""

import zipfile
import xml.etree.ElementTree as ET
import os
import logging
from typing import List, Dict, Optional

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DetectorImagensCorrigido:
    """Detector corrigido que usa o namespace correto"""
    
    def __init__(self, debug_mode: bool = True):
        self.debug_mode = debug_mode
        self.debug_info = []
    
    def log_debug(self, message: str):
        """Adiciona mensagem de debug"""
        if self.debug_mode:
            logger.info(message)
            self.debug_info.append(message)
    
    def detectar_imagens_corrigido(self, arquivo: str, target_columns: List[str] = ['H'], 
                                  start_row: int = 4, ref_column: str = 'A') -> List[Dict]:
        """
        Detecta imagens usando o namespace correto (xdr:)
        """
        images_found = []
        
        self.log_debug(f"🔍 Iniciando detecção corrigida de imagens...")
        self.log_debug(f"   • Arquivo: {arquivo}")
        self.log_debug(f"   • Colunas alvo: {target_columns}")
        self.log_debug(f"   • Linha inicial: {start_row}")
        self.log_debug(f"   • Coluna REF: {ref_column}")
        
        try:
            with zipfile.ZipFile(arquivo, 'r') as zip_file:
                # Passo 1: Ler drawing1.xml
                self.log_debug(f"📄 Lendo drawing1.xml...")
                drawing_content = zip_file.read('xl/drawings/drawing1.xml')
                root = ET.fromstring(drawing_content)
                
                # Encontrar todos os OneCellAnchor (usando namespace correto)
                one_cell_anchors = root.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing}oneCellAnchor')
                two_cell_anchors = root.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing}twoCellAnchor')
                
                all_anchors = one_cell_anchors + two_cell_anchors
                self.log_debug(f"   • Total de anchors encontrados: {len(all_anchors)}")
                
                # Passo 2: Ler drawing1.xml.rels para obter IDs das imagens
                self.log_debug(f"📄 Lendo drawing1.xml.rels...")
                rels_content = zip_file.read('xl/drawings/_rels/drawing1.xml.rels')
                rels_root = ET.fromstring(rels_content)
                
                # Criar mapeamento de IDs para arquivos de imagem
                image_mapping = {}
                relationships = rels_root.findall('.//{http://schemas.openxmlformats.org/package/2006/relationships}Relationship')
                
                for rel in relationships:
                    rel_id = rel.get('Id')
                    rel_type = rel.get('Type')
                    rel_target = rel.get('Target')
                    
                    if 'image' in rel_type.lower():
                        image_filename = os.path.basename(rel_target)
                        image_mapping[rel_id] = image_filename
                        self.log_debug(f"   • Mapeamento: {rel_id} -> {image_filename}")
                
                # Passo 3: Ler worksheet XML para obter REFs
                self.log_debug(f"📄 Lendo worksheet XML...")
                worksheet_files = [f for f in zip_file.namelist() if 'worksheet' in f and f.endswith('.xml')]
                
                refs_data = {}
                for ws_file in worksheet_files:
                    ws_content = zip_file.read(ws_file)
                    ws_root = ET.fromstring(ws_content)
                    
                    # Ler todas as células para obter REFs
                    rows = ws_root.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row')
                    for row in rows:
                        row_num = int(row.get('r', 0))
                        cells = row.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c')
                        
                        for cell in cells:
                            cell_ref = cell.get('r', '')
                            if cell_ref.startswith(ref_column):  # Coluna A (REFs)
                                cell_value_elem = cell.find('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
                                if cell_value_elem is not None:
                                    cell_value = cell_value_elem.text
                                    if cell_value and cell_value.strip():
                                        refs_data[row_num] = cell_value.strip()
                                        self.log_debug(f"   • REF encontrada: Linha {row_num} = {cell_value.strip()}")
                
                # Passo 4: Processar cada anchor
                self.log_debug(f"🖼️ Processando anchors...")
                for i, anchor in enumerate(all_anchors):
                    self.log_debug(f"   Anchor {i+1}:")
                    
                    # Obter posição
                    from_elem = anchor.find('.//{http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing}from')
                    if from_elem is not None:
                        col_elem = from_elem.find('.//{http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing}col')
                        row_elem = from_elem.find('.//{http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing}row')
                        
                        if col_elem is not None and row_elem is not None:
                            col = int(col_elem.text)
                            row = int(row_elem.text) + 1  # Excel rows são 1-based
                            
                            # Converter coluna para letra
                            col_letter = self._col_index_to_letter(col)
                            
                            self.log_debug(f"     - Posição: {col_letter}{row}")
                            
                            # Verificar se está nas colunas alvo e linha inicial
                            if col_letter in target_columns and row >= start_row:
                                # Obter REF correspondente
                                ref_value = refs_data.get(row, '')
                                
                                if ref_value and ref_value.upper() not in ['TOTAL', 'SUBTOTAL', '']:
                                    # Procurar por blipFill usando namespace correto (xdr:)
                                    blip_fill = anchor.find('.//{http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing}blipFill')
                                    if blip_fill is not None:
                                        # Procurar por blip usando namespace correto (a:)
                                        blip = blip_fill.find('.//{http://schemas.openxmlformats.org/drawingml/2006/main}blip')
                                        if blip is not None:
                                            embed_id = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                                            
                                            if embed_id in image_mapping:
                                                image_filename = image_mapping[embed_id]
                                                
                                                self.log_debug(f"     - ✅ Imagem válida encontrada!")
                                                self.log_debug(f"        REF: {ref_value}")
                                                self.log_debug(f"        Posição: {col_letter}{row}")
                                                self.log_debug(f"        Arquivo: {image_filename}")
                                                
                                                images_found.append({
                                                    'ref': ref_value,
                                                    'row': row,
                                                    'col': col_letter,
                                                    'col_index': col,
                                                    'image_filename': image_filename,
                                                    'embed_id': embed_id,
                                                    'anchor_type': 'OneCellAnchor' if anchor in one_cell_anchors else 'TwoCellAnchor'
                                                })
                                            else:
                                                self.log_debug(f"     - ❌ ID de imagem não encontrado: {embed_id}")
                                        else:
                                            self.log_debug(f"     - ❌ Blip não encontrado")
                                    else:
                                        self.log_debug(f"     - ❌ BlipFill não encontrado")
                                else:
                                    self.log_debug(f"     - ❌ REF inválida ou vazia: '{ref_value}'")
                            else:
                                self.log_debug(f"     - ❌ Fora da área alvo ({col_letter} não está em {target_columns} ou linha {row} < {start_row})")
                        else:
                            self.log_debug(f"     - ❌ Posição não encontrada")
                    else:
                        self.log_debug(f"     - ❌ Elemento 'from' não encontrado")
                
                self.log_debug(f"📊 Resumo da detecção:")
                self.log_debug(f"   • Total de imagens analisadas: {len(all_anchors)}")
                self.log_debug(f"   • Imagens válidas encontradas: {len(images_found)}")
                
                return images_found
                
        except Exception as e:
            self.log_debug(f"❌ Erro na detecção: {e}")
            return []
    
    def _col_index_to_letter(self, col_index: int) -> str:
        """Converte índice de coluna para letra (0=A, 1=B, etc.)"""
        result = ""
        while col_index >= 0:
            result = chr(ord('A') + col_index % 26) + result
            col_index = col_index // 26 - 1
        return result

def testar_detector_corrigido(arquivo: str):
    """Testa o detector corrigido"""
    
    print(f"\n🔍 TESTE DO DETECTOR CORRIGIDO")
    print(f"📁 Arquivo: {arquivo}")
    print("=" * 70)
    
    detector = DetectorImagensCorrigido(debug_mode=True)
    images = detector.detectar_imagens_corrigido(arquivo, target_columns=['H'], start_row=4, ref_column='A')
    
    print(f"\n📊 RESULTADOS:")
    print(f"   • Total de imagens encontradas: {len(images)}")
    
    if images:
        print(f"   • Detalhes das imagens:")
        for i, img in enumerate(images):
            print(f"     {i+1}. REF: {img['ref']} | Posição: {img['col']}{img['row']} | Arquivo: {img['image_filename']}")
        
        print(f"\n✅ SUCESSO! Detector corrigido funcionando!")
        print(f"   • {len(images)} imagens detectadas na coluna H")
        print(f"   • Todas as imagens têm REFs válidas")
        print(f"   • Problema resolvido!")
    else:
        print(f"\n❌ Nenhuma imagem encontrada")
    
    return images

def main():
    """Função principal"""
    
    print("🔍 DETECTOR CORRIGIDO DE IMAGENS EXCEL")
    print("=" * 70)
    
    arquivo = "produtos_novos.xlsx"
    testar_detector_corrigido(arquivo)

if __name__ == "__main__":
    main()

