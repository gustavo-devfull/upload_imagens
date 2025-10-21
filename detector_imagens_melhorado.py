#!/usr/bin/env python3
"""
Sistema MELHORADO para detecção e leitura de imagens em células do Excel
Versão mais robusta e precisa
"""

import openpyxl
import openpyxl.utils
import os
import logging
from typing import List, Dict, Optional, Tuple

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExcelImageDetector:
    """Classe melhorada para detectar imagens em células do Excel"""
    
    def __init__(self, debug_mode: bool = True):
        self.debug_mode = debug_mode
        self.debug_info = []
    
    def log_debug(self, message: str):
        """Adiciona mensagem de debug"""
        if self.debug_mode:
            logger.info(message)
            self.debug_info.append(message)
    
    def detect_images_in_worksheet(self, worksheet, target_columns: List[str] = ['H'], 
                                 start_row: int = 4, ref_column: str = 'A') -> List[Dict]:
        """
        Detecta imagens em células específicas da planilha
        
        Args:
            worksheet: Planilha do openpyxl
            target_columns: Lista de colunas onde procurar imagens (ex: ['H', 'I'])
            start_row: Linha inicial para procurar (padrão: 4)
            ref_column: Coluna onde estão as REFs (padrão: 'A')
        
        Returns:
            Lista de dicionários com informações das imagens encontradas
        """
        images_found = []
        
        self.log_debug(f"🔍 Iniciando detecção de imagens...")
        self.log_debug(f"   • Colunas alvo: {target_columns}")
        self.log_debug(f"   • Linha inicial: {start_row}")
        self.log_debug(f"   • Coluna REF: {ref_column}")
        
        # Converte colunas para índices
        target_col_indices = []
        for col in target_columns:
            try:
                col_idx = openpyxl.utils.column_index_from_string(col) - 1  # 0-based
                target_col_indices.append(col_idx)
                self.log_debug(f"   • Coluna {col} = índice {col_idx}")
            except Exception as e:
                self.log_debug(f"   ❌ Erro ao converter coluna {col}: {e}")
        
        # Analisa todas as imagens da planilha
        total_images = len(worksheet._images)
        self.log_debug(f"🖼️ Total de imagens na planilha: {total_images}")
        
        for i, image in enumerate(worksheet._images):
            self.log_debug(f"\n🖼️ Analisando imagem {i+1}/{total_images}")
            
            try:
                # Obtém informações da imagem
                image_info = self._analyze_image_anchor(image, i+1)
                
                if image_info:
                    col_idx = image_info['col_idx']
                    row_idx = image_info['row_idx']
                    col_letter = image_info['col_letter']
                    
                    self.log_debug(f"   📍 Posição: {col_letter}{row_idx}")
                    
                    # Verifica se está em uma das colunas alvo
                    if col_idx in target_col_indices and row_idx >= start_row:
                        # Busca a REF correspondente
                        ref_value = self._get_ref_for_row(worksheet, row_idx, ref_column)
                        
                        if ref_value:
                            image_data = {
                                'image': image,
                                'ref': ref_value,
                                'row': row_idx,
                                'col': col_letter,
                                'col_idx': col_idx,
                                'image_index': i,
                                'anchor_type': image_info['anchor_type']
                            }
                            
                            images_found.append(image_data)
                            self.log_debug(f"   ✅ Imagem válida encontrada!")
                            self.log_debug(f"      REF: {ref_value}")
                            self.log_debug(f"      Posição: {col_letter}{row_idx}")
                            self.log_debug(f"      Tipo anchor: {image_info['anchor_type']}")
                        else:
                            self.log_debug(f"   ⚠️ Imagem sem REF válida na linha {row_idx}")
                    else:
                        self.log_debug(f"   ❌ Imagem fora da área alvo ({col_letter}{row_idx})")
                        
            except Exception as e:
                self.log_debug(f"   ❌ Erro ao analisar imagem {i+1}: {e}")
                continue
        
        self.log_debug(f"\n📊 Resumo da detecção:")
        self.log_debug(f"   • Total de imagens analisadas: {total_images}")
        self.log_debug(f"   • Imagens válidas encontradas: {len(images_found)}")
        
        return images_found
    
    def _analyze_image_anchor(self, image, image_number: int) -> Optional[Dict]:
        """
        Analisa o anchor de uma imagem e retorna informações de posição
        
        Args:
            image: Objeto de imagem do openpyxl
            image_number: Número da imagem para debug
        
        Returns:
            Dicionário com informações de posição ou None se erro
        """
        try:
            if not hasattr(image, 'anchor') or not image.anchor:
                self.log_debug(f"   ❌ Imagem {image_number} sem anchor")
                return None
            
            anchor = image.anchor
            anchor_type = type(anchor).__name__
            self.log_debug(f"   🔗 Tipo de anchor: {anchor_type}")
            
            # Tenta diferentes métodos de acesso ao anchor
            col_idx = None
            row_idx = None
            
            if hasattr(anchor, '_from') and anchor._from:
                # TwoCellAnchor
                col_idx = anchor._from.col
                row_idx = anchor._from.row
                self.log_debug(f"   📍 TwoCellAnchor: col={col_idx}, row={row_idx}")
            elif hasattr(anchor, 'col') and hasattr(anchor, 'row'):
                # OneCellAnchor
                col_idx = anchor.col
                row_idx = anchor.row
                self.log_debug(f"   📍 OneCellAnchor: col={col_idx}, row={row_idx}")
            else:
                self.log_debug(f"   ❌ Anchor sem propriedades de posição conhecidas")
                self.log_debug(f"   🔍 Propriedades disponíveis: {[attr for attr in dir(anchor) if not attr.startswith('_')]}")
                return None
            
            # Converte para formato Excel (1-based para linhas)
            excel_row = row_idx + 1
            col_letter = openpyxl.utils.get_column_letter(col_idx + 1)
            
            return {
                'col_idx': col_idx,
                'row_idx': excel_row,
                'col_letter': col_letter,
                'anchor_type': anchor_type
            }
            
        except Exception as e:
            self.log_debug(f"   ❌ Erro ao analisar anchor da imagem {image_number}: {e}")
            return None
    
    def _get_ref_for_row(self, worksheet, row: int, ref_column: str) -> Optional[str]:
        """
        Obtém a REF para uma linha específica
        
        Args:
            worksheet: Planilha do openpyxl
            row: Número da linha
            ref_column: Coluna onde estão as REFs
        
        Returns:
            REF limpa ou None se inválida
        """
        try:
            ref_cell = worksheet[f'{ref_column}{row}']
            if not ref_cell.value:
                return None
            
            ref_value = str(ref_cell.value).strip()
            
            # Filtra REFs inválidas
            invalid_refs = ['TOTAL', 'SUBTOTAL', '', 'None', 'null']
            if ref_value.upper() in invalid_refs:
                return None
            
            return ref_value
            
        except Exception as e:
            self.log_debug(f"   ❌ Erro ao obter REF da linha {row}: {e}")
            return None
    
    def get_detailed_image_info(self, worksheet) -> Dict:
        """
        Obtém informações detalhadas sobre todas as imagens da planilha
        
        Args:
            worksheet: Planilha do openpyxl
        
        Returns:
            Dicionário com estatísticas detalhadas
        """
        stats = {
            'total_images': len(worksheet._images),
            'images_by_column': {},
            'images_by_row': {},
            'anchor_types': {},
            'images_with_refs': 0,
            'images_without_refs': 0
        }
        
        for i, image in enumerate(worksheet._images):
            try:
                image_info = self._analyze_image_anchor(image, i+1)
                if image_info:
                    col = image_info['col_letter']
                    row = image_info['row_idx']
                    anchor_type = image_info['anchor_type']
                    
                    # Conta por coluna
                    if col not in stats['images_by_column']:
                        stats['images_by_column'][col] = 0
                    stats['images_by_column'][col] += 1
                    
                    # Conta por linha
                    if row not in stats['images_by_row']:
                        stats['images_by_row'][row] = 0
                    stats['images_by_row'][row] += 1
                    
                    # Conta tipos de anchor
                    if anchor_type not in stats['anchor_types']:
                        stats['anchor_types'][anchor_type] = 0
                    stats['anchor_types'][anchor_type] += 1
                    
                    # Verifica se tem REF
                    ref_value = self._get_ref_for_row(worksheet, row, 'A')
                    if ref_value:
                        stats['images_with_refs'] += 1
                    else:
                        stats['images_without_refs'] += 1
                        
            except Exception as e:
                self.log_debug(f"Erro ao analisar imagem {i+1}: {e}")
                continue
        
        return stats

def testar_deteccao_melhorada(arquivo: str):
    """Testa o sistema melhorado de detecção de imagens"""
    
    if not os.path.exists(arquivo):
        print(f"❌ Arquivo {arquivo} não existe!")
        return False
    
    print(f"\n🔍 TESTE DE DETECÇÃO MELHORADA")
    print(f"📁 Arquivo: {arquivo}")
    print("=" * 60)
    
    try:
        # Carrega o arquivo
        workbook = openpyxl.load_workbook(arquivo)
        worksheet = workbook.active
        
        # Cria detector
        detector = ExcelImageDetector(debug_mode=True)
        
        # Obtém estatísticas detalhadas
        print("\n📊 ESTATÍSTICAS DETALHADAS:")
        stats = detector.get_detailed_image_info(worksheet)
        
        print(f"   • Total de imagens: {stats['total_images']}")
        print(f"   • Imagens com REFs: {stats['images_with_refs']}")
        print(f"   • Imagens sem REFs: {stats['images_without_refs']}")
        
        if stats['images_by_column']:
            print(f"   • Imagens por coluna:")
            for col, count in sorted(stats['images_by_column'].items()):
                print(f"     - Coluna {col}: {count} imagens")
        
        if stats['anchor_types']:
            print(f"   • Tipos de anchor:")
            for anchor_type, count in stats['anchor_types'].items():
                print(f"     - {anchor_type}: {count} imagens")
        
        # Testa detecção na coluna H
        print(f"\n🎯 DETECÇÃO NA COLUNA H:")
        images_h = detector.detect_images_in_worksheet(
            worksheet, 
            target_columns=['H'], 
            start_row=4, 
            ref_column='A'
        )
        
        print(f"   • Imagens encontradas na coluna H: {len(images_h)}")
        
        if images_h:
            print(f"   • Detalhes das imagens:")
            for img in images_h:
                print(f"     ✅ REF: {img['ref']} | Posição: {img['col']}{img['row']} | Tipo: {img['anchor_type']}")
        
        # Testa detecção em múltiplas colunas
        print(f"\n🎯 DETECÇÃO EM MÚLTIPLAS COLUNAS (H, I, J):")
        images_multi = detector.detect_images_in_worksheet(
            worksheet, 
            target_columns=['H', 'I', 'J'], 
            start_row=4, 
            ref_column='A'
        )
        
        print(f"   • Imagens encontradas nas colunas H, I, J: {len(images_multi)}")
        
        workbook.close()
        
        # Resultado final
        if len(images_h) > 0:
            print(f"\n✅ SUCESSO! Arquivo válido para upload.")
            print(f"   Pode processar {len(images_h)} imagens da coluna H.")
            return True
        else:
            print(f"\n❌ FALHA! Nenhuma imagem válida encontrada na coluna H.")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao processar arquivo: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Função principal para testar o sistema melhorado"""
    
    print("🚀 SISTEMA MELHORADO DE DETECÇÃO DE IMAGENS")
    print("=" * 60)
    
    # Lista de arquivos para testar
    arquivos_teste = [
        "fabrica_com_imagens.xlsx",
        "tartaruga.xlsx", 
        "carrinho.xlsx",
        "nova.xlsx"
    ]
    
    resultados = {}
    
    for arquivo in arquivos_teste:
        print(f"\n{'='*60}")
        resultado = testar_deteccao_melhorada(arquivo)
        resultados[arquivo] = resultado
    
    # Resumo final
    print(f"\n{'='*60}")
    print("📋 RESUMO FINAL")
    print("=" * 60)
    
    arquivos_validos = [arquivo for arquivo, valido in resultados.items() if valido]
    arquivos_invalidos = [arquivo for arquivo, valido in resultados.items() if not valido]
    
    if arquivos_validos:
        print("✅ ARQUIVOS VÁLIDOS:")
        for arquivo in arquivos_validos:
            print(f"   • {arquivo}")
    
    if arquivos_invalidos:
        print("❌ ARQUIVOS INVÁLIDOS:")
        for arquivo in arquivos_invalidos:
            print(f"   • {arquivo}")
    
    print(f"\n💡 Use os arquivos válidos para fazer upload!")

if __name__ == "__main__":
    main()
