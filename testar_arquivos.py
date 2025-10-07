#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para verificar qual arquivo está sendo usado
"""

import os
import tempfile
from upload_ftp_corrigido import FTPImageExtractorCorrigido

def testar_arquivo(file_path):
    """Testa um arquivo específico"""
    print(f"🧪 Testando arquivo: {file_path}")
    print("=" * 50)
    
    try:
        extractor = FTPImageExtractorCorrigido(
            "46.202.90.62", 
            "u715606397.ideolog.ia.br", 
            "]X9CC>t~ihWhdzNq"
        )
        
        stats = extractor.process_excel_file(file_path, start_row=4, photo_column='H')
        
        print(f"📊 Resultados:")
        print(f"  REFs processadas: {stats['total_refs']}")
        print(f"  Imagens encontradas: {stats['images_found']}")
        print(f"  Uploads bem-sucedidos: {stats['uploads_successful']}")
        print(f"  Uploads falharam: {stats['uploads_failed']}")
        
        if stats['errors']:
            print(f"  Erros: {stats['errors']}")
        
        return stats
        
    except Exception as e:
        print(f"❌ Erro ao processar arquivo: {e}")
        return None

def main():
    """Função principal"""
    # Lista arquivos Excel disponíveis
    excel_files = [f for f in os.listdir('.') if f.endswith('.xlsx')]
    
    print("📁 Arquivos Excel disponíveis:")
    for i, file in enumerate(excel_files, 1):
        print(f"  {i}. {file}")
    
    print()
    
    # Testa cada arquivo
    for excel_file in excel_files:
        stats = testar_arquivo(excel_file)
        if stats:
            print(f"✅ {excel_file}: {stats['images_found']} imagens encontradas")
        else:
            print(f"❌ {excel_file}: Erro no processamento")
        print()

if __name__ == "__main__":
    main()
