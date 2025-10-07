#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para ajudar a identificar o arquivo correto
"""

import os
import openpyxl

def verificar_arquivo(file_path):
    """Verifica se um arquivo tem imagens"""
    try:
        workbook = openpyxl.load_workbook(file_path)
        worksheet = workbook.active
        
        # Conta REFs válidas
        ref_count = 0
        for row in range(4, worksheet.max_row + 1):
            cell_value = worksheet[f'A{row}'].value
            if cell_value and str(cell_value).strip() and str(cell_value).strip().upper() not in ['TOTAL', 'SUBTOTAL']:
                ref_count += 1
        
        # Conta imagens
        image_count = len(worksheet._images)
        
        workbook.close()
        
        return {
            'refs': ref_count,
            'images': image_count,
            'has_images': image_count > 0
        }
        
    except Exception as e:
        return {'error': str(e)}

def main():
    """Função principal"""
    print("🔍 Verificando arquivos Excel disponíveis...")
    print("=" * 50)
    
    excel_files = [f for f in os.listdir('.') if f.endswith('.xlsx')]
    
    for file in excel_files:
        print(f"📁 Arquivo: {file}")
        result = verificar_arquivo(file)
        
        if 'error' in result:
            print(f"  ❌ Erro: {result['error']}")
        else:
            print(f"  📊 REFs válidas: {result['refs']}")
            print(f"  🖼️ Imagens: {result['images']}")
            
            if result['has_images']:
                print(f"  ✅ RECOMENDADO - Use este arquivo!")
            else:
                print(f"  ❌ Sem imagens - Não use este arquivo")
        
        print()
    
    print("💡 INSTRUÇÕES:")
    print("1. Use 'tartaruga.xlsx' (com 't') ou 'carrinho.xlsx'")
    print("2. NÃO use 'artaruga.xlsx' (sem 't')")
    print("3. NÃO use 'cotacao.xlsx' (sem imagens)")
    print()
    print("🚀 Para usar o sistema:")
    print("   python3 sistema_hibrido.py")
    print("   Acesse: http://localhost:8081")

if __name__ == "__main__":
    main()
