#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simplificado para processar arquivo Excel específico
Modifique o caminho do arquivo abaixo e execute
"""

from excel_image_extractor import ExcelImageExtractor
import os

def process_excel_file(file_path: str):
    """
    Processa um arquivo Excel específico
    
    Args:
        file_path: Caminho para o arquivo Excel
    """
    
    # Configurações FTP
    FTP_HOST = "46.202.90.62"
    FTP_USER = "u715606397.gpreto.space"
    FTP_PASSWORD = "8:fRP;*OVPp3Oyc&"
    
    # Verifica se arquivo existe
    if not os.path.exists(file_path):
        print(f"❌ Arquivo não encontrado: {file_path}")
        return False
    
    print(f"📁 Processando arquivo: {file_path}")
    print("🔄 Iniciando extração de imagens...")
    
    # Cria instância do extrator
    extractor = ExcelImageExtractor(FTP_HOST, FTP_USER, FTP_PASSWORD)
    
    try:
        # Processa o arquivo
        stats = extractor.process_excel_file(file_path)
        
        # Exibe resultados
        print("\n" + "="*60)
        print("📊 RESULTADOS DO PROCESSAMENTO")
        print("="*60)
        print(f"📋 Total de REFs encontradas: {stats['total_refs']}")
        print(f"🖼️  Imagens encontradas: {stats['images_found']}")
        print(f"✅ Uploads bem-sucedidos: {stats['uploads_successful']}")
        print(f"❌ Uploads falharam: {stats['uploads_failed']}")
        
        if stats['errors']:
            print(f"\n⚠️  Erros encontrados ({len(stats['errors'])}):")
            for error in stats['errors']:
                print(f"   • {error}")
        
        success_rate = (stats['uploads_successful'] / max(stats['total_refs'], 1)) * 100
        print(f"\n📈 Taxa de sucesso: {success_rate:.1f}%")
        
        if stats['uploads_successful'] > 0:
            print(f"\n🌐 Imagens disponíveis em: http://46.202.90.62/")
            print("   Exemplo: http://46.202.90.62/A3.jpg")
        
        print("\n✨ Processamento concluído!")
        return True
        
    except Exception as e:
        print(f"❌ Erro durante o processamento: {e}")
        return False


if __name__ == "__main__":
    # MODIFIQUE AQUI O CAMINHO PARA SEU ARQUIVO EXCEL
    excel_file_path = "/Users/gustavo/upload/exemplo.xlsx"  # ← Altere este caminho
    
    print("🚀 Sistema de Extração de Imagens Excel → FTP")
    print("=" * 50)
    
    # Verifica se o arquivo foi especificado
    if excel_file_path == "/Users/gustavo/upload/exemplo.xlsx":
        print("⚠️  ATENÇÃO: Modifique a variável 'excel_file_path' no código")
        print("   para apontar para seu arquivo Excel.")
        print("\n   Exemplo:")
        print("   excel_file_path = '/caminho/para/sua/planilha.xlsx'")
        print("\n   Ou execute o script principal:")
        print("   python excel_image_extractor.py")
    else:
        process_excel_file(excel_file_path)

