#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simples para upload - apenas modifique o caminho e execute
"""

from excel_image_extractor import ExcelImageExtractor

# ========================================
# CONFIGURAÇÃO - MODIFIQUE AQUI
# ========================================

# Caminho para seu arquivo Excel (MODIFIQUE ESTA LINHA)
EXCEL_FILE = "/Users/gustavo/upload/carrinho.xlsx"

# Configurações FTP (já configuradas)
FTP_HOST = "gpreto.space"
FTP_USER = "u715606397.nova"
FTP_PASSWORD = "]X9CC>t~ihWhdzNq"

# ========================================
# EXECUÇÃO
# ========================================

def main():
    print("🚀 UPLOAD SIMPLES PARA FTP")
    print("=" * 30)
    print(f"📁 Arquivo: {EXCEL_FILE}")
    print(f"🌐 Servidor: {FTP_HOST}")
    print()
    
    # Verifica arquivo
    import os
    if not os.path.exists(EXCEL_FILE):
        print(f"❌ Arquivo não encontrado: {EXCEL_FILE}")
        print("\n💡 Para usar:")
        print("   1. Edite a variável EXCEL_FILE neste arquivo")
        print("   2. Coloque o caminho do seu arquivo Excel")
        print("   3. Execute: python3 upload_simples.py")
        return
    
    print("✅ Arquivo encontrado!")
    print("🚀 Iniciando upload...")
    
    # Cria extrator e processa
    extractor = ExcelImageExtractor(FTP_HOST, FTP_USER, FTP_PASSWORD)
    stats = extractor.process_excel_file(EXCEL_FILE, start_row=4, photo_column='H')
    
    # Resultados
    print("\n" + "="*40)
    print("📊 RESULTADOS")
    print("="*40)
    print(f"REFs: {stats['total_refs']}")
    print(f"Imagens: {stats['images_found']}")
    print(f"Uploads OK: {stats['uploads_successful']}")
    print(f"Uploads FALHARAM: {stats['uploads_failed']}")
    
    if stats['uploads_successful'] > 0:
        print(f"\n🌐 Acesse: https://gpreto.space/images/products/")
        print(f"📝 Exemplo: https://gpreto.space/images/products/T608.jpg")
    
    if stats['errors']:
        print(f"\n⚠️  Erros:")
        for error in stats['errors']:
            print(f"   • {error}")
    
    print("\n✨ Concluído!")

if __name__ == "__main__":
    main()
