#!/usr/bin/env python3
"""
🔍 INVESTIGADOR PROFUNDO DE XML
Investiga a estrutura completa do XML para entender como as imagens estão organizadas
"""

import zipfile
import xml.etree.ElementTree as ET
import os

def investigar_xml_profundo(arquivo):
    """Investiga profundamente a estrutura XML"""
    
    print(f"\n🔍 INVESTIGAÇÃO PROFUNDA DE XML")
    print(f"📁 Arquivo: {arquivo}")
    print("=" * 70)
    
    try:
        with zipfile.ZipFile(arquivo, 'r') as zip_file:
            # MÉTODO 1: Analisar drawing1.xml completamente
            print(f"\n🔍 MÉTODO 1: Análise completa do drawing1.xml")
            drawing_content = zip_file.read('xl/drawings/drawing1.xml')
            
            # Mostrar conteúdo XML completo
            print(f"📄 Conteúdo completo do drawing1.xml:")
            print("-" * 50)
            print(drawing_content.decode('utf-8'))
            print("-" * 50)
            
            # Parsear e mostrar estrutura
            root = ET.fromstring(drawing_content)
            print(f"\n📊 Estrutura XML:")
            self._print_xml_structure(root, 0)
            
            # MÉTODO 2: Procurar por todos os elementos que podem conter imagens
            print(f"\n🔍 MÉTODO 2: Busca por elementos de imagem")
            
            # Procurar por elementos com namespace de imagem
            image_elements = root.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/picture}*')
            print(f"   • Elementos de imagem encontrados: {len(image_elements)}")
            for elem in image_elements:
                print(f"     - {elem.tag}: {elem.attrib}")
            
            # Procurar por elementos blip
            blip_elements = root.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/picture}blip')
            print(f"   • Elementos blip encontrados: {len(blip_elements)}")
            for elem in blip_elements:
                print(f"     - {elem.tag}: {elem.attrib}")
            
            # Procurar por elementos blipFill
            blipfill_elements = root.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/picture}blipFill')
            print(f"   • Elementos blipFill encontrados: {len(blipfill_elements)}")
            for elem in blipfill_elements:
                print(f"     - {elem.tag}: {elem.attrib}")
            
            # Procurar por elementos pic
            pic_elements = root.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/picture}pic')
            print(f"   • Elementos pic encontrados: {len(pic_elements)}")
            for elem in pic_elements:
                print(f"     - {elem.tag}: {elem.attrib}")
            
            # MÉTODO 3: Analisar cada anchor individualmente
            print(f"\n🔍 MÉTODO 3: Análise individual de cada anchor")
            
            one_cell_anchors = root.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing}oneCellAnchor')
            two_cell_anchors = root.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing}twoCellAnchor')
            
            all_anchors = one_cell_anchors + two_cell_anchors
            
            for i, anchor in enumerate(all_anchors):
                print(f"\n   Anchor {i+1}:")
                print(f"   Tag: {anchor.tag}")
                print(f"   Atributos: {anchor.attrib}")
                
                # Mostrar estrutura completa do anchor
                print(f"   Estrutura completa:")
                self._print_xml_structure(anchor, 2)
                
                # Procurar por qualquer elemento que possa ser uma imagem
                for child in anchor.iter():
                    if 'image' in child.tag.lower() or 'pic' in child.tag.lower() or 'blip' in child.tag.lower():
                        print(f"   ✅ Elemento de imagem encontrado: {child.tag}")
                        print(f"      Atributos: {child.attrib}")
                        print(f"      Texto: {child.text}")
            
            # MÉTODO 4: Verificar se há elementos em outros namespaces
            print(f"\n🔍 MÉTODO 4: Verificação de outros namespaces")
            
            # Procurar por todos os elementos únicos
            all_elements = set()
            for elem in root.iter():
                all_elements.add(elem.tag)
            
            print(f"   • Todos os elementos únicos encontrados:")
            for elem_tag in sorted(all_elements):
                print(f"     - {elem_tag}")
            
            # MÉTODO 5: Verificar se há elementos sem namespace
            print(f"\n🔍 MÉTODO 5: Verificação de elementos sem namespace")
            
            # Procurar por elementos que não têm namespace
            no_ns_elements = []
            for elem in root.iter():
                if '}' not in elem.tag:
                    no_ns_elements.append(elem.tag)
            
            if no_ns_elements:
                print(f"   • Elementos sem namespace: {set(no_ns_elements)}")
            else:
                print(f"   • Todos os elementos têm namespace")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

def _print_xml_structure(element, depth=0):
    """Imprime a estrutura XML de forma recursiva"""
    indent = "  " * depth
    print(f"{indent}{element.tag}")
    
    if element.attrib:
        for attr, value in element.attrib.items():
            print(f"{indent}  @{attr}: {value}")
    
    if element.text and element.text.strip():
        print(f"{indent}  Text: {element.text.strip()}")
    
    for child in element:
        _print_xml_structure(child, depth + 1)

def main():
    """Função principal"""
    
    print("🔍 INVESTIGADOR PROFUNDO DE XML")
    print("=" * 70)
    
    arquivo = "produtos_novos.xlsx"
    investigar_xml_profundo(arquivo)

if __name__ == "__main__":
    main()

