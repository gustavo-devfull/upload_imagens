#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste direto da função save_image_to_temp corrigida
"""

import openpyxl
import os
import logging
from excel_image_extractor import ExcelImageExtractor

# Configuração de logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def testar_save_direto():
    """Testa a função save_image_to_temp diretamente"""
    
    arquivo = "/Users/gustavo/upload/tartaruga.xlsx"
    
    try:
        workbook = openpyxl.load_workbook(arquivo)
        worksheet = workbook.active
        
        image = worksheet._images[0]
        print(f"🖼️ Tipo da imagem: {type(image)}")
        
        # Cria instância do extrator
        extractor = ExcelImageExtractor("test", "test", "test")
        
        # Testa salvamento
        print("\n💾 TESTANDO SAVEMENTO DIRETO:")
        try:
            temp_path = extractor.save_image_to_temp(image, "CHDJ25001")
            print(f"✅ Imagem salva: {temp_path}")
            
            if os.path.exists(temp_path):
                size = os.path.getsize(temp_path)
                print(f"✅ Arquivo existe: {size} bytes")
                os.remove(temp_path)
            else:
                print("❌ Arquivo não existe")
                
        except Exception as e:
            print(f"❌ Erro ao salvar: {e}")
            import traceback
            traceback.print_exc()
        
        workbook.close()
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    testar_save_direto()
