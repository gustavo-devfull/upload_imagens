#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para verificar a detecção de posição das imagens
"""

import openpyxl
import logging

# Configuração de logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def testar_deteccao_posicao(file_path):
    """Testa a detecção de posição das imagens"""
    print(f"🧪 Testando detecção de posição: {file_path}")
    print("=" * 50)
    
    try:
        workbook = openpyxl.load_workbook(file_path)
        worksheet = workbook.active
        
        print(f"📊 Planilha: {worksheet.title}")
        print(f"🖼️ Total de imagens: {len(worksheet._images)}")
        
        if len(worksheet._images) == 0:
            print("❌ Nenhuma imagem para testar")
            return
        
        # Converte coluna H para número
        photo_col_num = openpyxl.utils.column_index_from_string('H')
        print(f"📸 Coluna H = {photo_col_num}")
        
        # Testa cada imagem
        for i, image in enumerate(worksheet._images):
            print(f"\n🖼️ Imagem {i+1}:")
            
            anchor = image.anchor
            print(f"  Anchor: {anchor}")
            print(f"  Tipo anchor: {type(anchor)}")
            
            # Testa diferentes métodos de obtenção de posição
            row = None
            col = None
            metodo_usado = None
            
            # Método 1: _from.row e _from.col
            if hasattr(anchor, '_from') and hasattr(anchor._from, 'row') and hasattr(anchor._from, 'col'):
                try:
                    row = anchor._from.row + 1
                    col = anchor._from.col + 1
                    metodo_usado = "Método 1: _from.row e _from.col"
                    print(f"  ✅ {metodo_usado}: linha {row}, coluna {col}")
                except Exception as e:
                    print(f"  ❌ {metodo_usado}: erro {e}")
            
            # Método 2: _from como tupla
            elif hasattr(anchor, '_from') and isinstance(anchor._from, tuple) and len(anchor._from) >= 2:
                try:
                    row = anchor._from[0] + 1
                    col = anchor._from[1] + 1
                    metodo_usado = "Método 2: _from como tupla"
                    print(f"  ✅ {metodo_usado}: linha {row}, coluna {col}")
                except Exception as e:
                    print(f"  ❌ {metodo_usado}: erro {e}")
            
            # Método 3: propriedades diretas
            elif hasattr(anchor, 'row') and hasattr(anchor, 'col'):
                try:
                    row = anchor.row + 1
                    col = anchor.col + 1
                    metodo_usado = "Método 3: propriedades diretas"
                    print(f"  ✅ {metodo_usado}: linha {row}, coluna {col}")
                except Exception as e:
                    print(f"  ❌ {metodo_usado}: erro {e}")
            
            else:
                print(f"  ❌ Nenhum método funcionou")
                print(f"  🔍 Atributos do anchor: {[attr for attr in dir(anchor) if not attr.startswith('_')]}")
                if hasattr(anchor, '_from'):
                    print(f"  🔍 _from: {anchor._from}")
                    print(f"  🔍 Tipo _from: {type(anchor._from)}")
                    if hasattr(anchor._from, '__dict__'):
                        print(f"  🔍 _from.__dict__: {anchor._from.__dict__}")
            
            # Se conseguiu obter posição, verifica critérios
            if row and col:
                col_letter = openpyxl.utils.get_column_letter(col)
                print(f"  📍 Posição: {col_letter}{row}")
                
                # Verifica se está na coluna H
                if col == photo_col_num:
                    print(f"  ✅ Está na coluna H (PHOTO)")
                else:
                    print(f"  ❌ Está na coluna {col_letter}, não na H")
                
                # Verifica se está a partir da linha 4
                if row >= 4:
                    print(f"  ✅ Está a partir da linha 4")
                else:
                    print(f"  ❌ Está antes da linha 4")
                
                # Verifica REF correspondente
                ref_value = worksheet[f'A{row}'].value
                if ref_value:
                    print(f"  🔍 REF: {ref_value}")
                else:
                    print(f"  ❌ Sem REF na linha {row}")
                
                # RESULTADO FINAL
                if row >= 4 and col == photo_col_num:
                    print(f"  🎯 RESULTADO: IMAGEM VÁLIDA!")
                else:
                    print(f"  ❌ RESULTADO: Imagem não atende aos critérios")
            else:
                print(f"  ❌ Não foi possível determinar a posição")
        
        workbook.close()
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        logger.error(f"Erro no teste de detecção: {e}")

def main():
    """Função principal"""
    # Testa arquivos com imagens
    arquivos_com_imagens = ['tartaruga.xlsx', 'carrinho.xlsx']
    
    for arquivo in arquivos_com_imagens:
        try:
            testar_deteccao_posicao(arquivo)
            print("\n" + "="*60 + "\n")
        except FileNotFoundError:
            print(f"❌ Arquivo {arquivo} não encontrado")
        except Exception as e:
            print(f"❌ Erro ao processar {arquivo}: {e}")

if __name__ == "__main__":
    main()
