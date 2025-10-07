#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para fazer upload direto para FTP
Modifique o caminho do arquivo abaixo e execute
"""

import os
import sys
from excel_image_extractor import ExcelImageExtractor

def fazer_upload_ftp():
    """Faz upload das imagens para o FTP"""
    
    print("🚀 UPLOAD PARA FTP - Sistema de Extração de Imagens")
    print("=" * 55)
    
    # Configurações FTP
    FTP_HOST = "gpreto.space"
    FTP_USER = "u715606397.nova"
    FTP_PASSWORD = "]X9CC>t~ihWhdzNq"
    
    print("\n📋 Configurações:")
    print(f"   • Servidor FTP: {FTP_HOST}")
    print(f"   • Usuário: {FTP_USER}")
    print(f"   • Coluna REF: A")
    print(f"   • Coluna PHOTO: H")
    print(f"   • Linha inicial: 4")
    
    # MODIFIQUE AQUI O CAMINHO PARA SEU ARQUIVO EXCEL
    excel_file_path = "/Users/gustavo/upload/sua_planilha.xlsx"  # ← Altere este caminho
    
    print(f"\n📁 Arquivo Excel: {excel_file_path}")
    
    # Verifica se arquivo existe
    if not os.path.exists(excel_file_path):
        print(f"❌ Arquivo não encontrado: {excel_file_path}")
        print("\n💡 Para usar este script:")
        print("   1. Edite a variável 'excel_file_path' no código")
        print("   2. Coloque o caminho completo para seu arquivo Excel")
        print("   3. Execute novamente: python3 upload_ftp.py")
        print("\n   Exemplo:")
        print("   excel_file_path = '/Users/usuario/Documents/planilha.xlsx'")
        return False
    
    print(f"✅ Arquivo encontrado!")
    
    # Cria instância do extrator
    extractor = ExcelImageExtractor(FTP_HOST, FTP_USER, FTP_PASSWORD)
    
    print("\n🚀 Iniciando processamento e upload...")
    print("   Isso pode levar alguns minutos...")
    
    try:
        # Processa o arquivo e faz upload
        stats = extractor.process_excel_file(excel_file_path, start_row=4, photo_column='H')
        
        # Exibe resultados
        print("\n" + "="*60)
        print("📊 RESULTADOS DO UPLOAD")
        print("="*60)
        print(f"📋 Linha inicial: {stats['start_row']}")
        print(f"🖼️  Coluna das imagens: {stats['photo_column']}")
        print(f"📋 REFs processadas: {stats['total_refs']}")
        print(f"🖼️  Imagens encontradas: {stats['images_found']}")
        print(f"✅ Uploads bem-sucedidos: {stats['uploads_successful']}")
        print(f"❌ Uploads falharam: {stats['uploads_failed']}")
        
        if stats['uploads_successful'] > 0:
            print(f"\n🌐 Suas imagens estão disponíveis em:")
            print(f"   http://46.202.90.62/")
            print(f"\n📝 Exemplos de URLs:")
            print(f"   http://46.202.90.62/CHDJ25001.jpg")
            print(f"   http://46.202.90.62/TOTAL.jpg")
            print(f"   http://46.202.90.62/[nome_da_ref].jpg")
        
        if stats['errors']:
            print(f"\n⚠️  Erros encontrados ({len(stats['errors'])}):")
            for i, error in enumerate(stats['errors'], 1):
                print(f"   {i}. {error}")
        
        # Calcula taxa de sucesso
        if stats['total_refs'] > 0:
            success_rate = (stats['uploads_successful'] / stats['total_refs']) * 100
            print(f"\n📈 Taxa de sucesso: {success_rate:.1f}%")
            
            if success_rate == 100:
                print("🎉 Perfeito! Todas as imagens foram enviadas com sucesso!")
            elif success_rate >= 80:
                print("👍 Bom resultado! A maioria das imagens foi enviada.")
            elif success_rate >= 50:
                print("⚠️  Resultado parcial. Verifique os erros acima.")
            else:
                print("❌ Muitos problemas. Verifique a estrutura da planilha.")
        
        print("\n✨ Processamento concluído!")
        return stats['uploads_successful'] > 0
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Upload interrompido pelo usuário.")
        return False
    except Exception as e:
        print(f"\n❌ Erro durante o upload: {e}")
        print("\n💡 Possíveis soluções:")
        print("   • Verifique se o arquivo Excel não está corrompido")
        print("   • Confirme se há imagens na coluna H")
        print("   • Teste a conectividade com o servidor FTP")
        return False


def mostrar_instrucoes():
    """Mostra instruções de uso"""
    
    print("📖 INSTRUÇÕES PARA UPLOAD")
    print("=" * 30)
    print()
    print("1️⃣  Edite o arquivo upload_ftp.py:")
    print("   • Encontre a linha: excel_file_path = '/Users/gustavo/upload/sua_planilha.xlsx'")
    print("   • Substitua pelo caminho do seu arquivo Excel")
    print()
    print("2️⃣  Execute o script:")
    print("   python3 upload_ftp.py")
    print()
    print("3️⃣  Aguarde o processamento")
    print()
    print("4️⃣  Acesse suas imagens em:")
    print("   http://46.202.90.62/")
    print()
    print("💡 DICAS:")
    print("   • Use caminhos absolutos para o arquivo Excel")
    print("   • No macOS, arraste o arquivo para o terminal para obter o caminho")
    print("   • Certifique-se de que há imagens na coluna H")
    print("   • O sistema salva as imagens como REF.jpg")


if __name__ == "__main__":
    print("🚀 Sistema de Extração de Imagens Excel → FTP")
    print("   Versão 2.3 - Upload Direto")
    print()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        mostrar_instrucoes()
    else:
        sucesso = fazer_upload_ftp()
        
        if sucesso:
            print("\n🎉 Upload concluído com sucesso!")
        else:
            print("\n⚠️  Upload concluído com problemas.")
        
        print("\n" + "="*50)
        print("❓ Precisa de ajuda? Execute:")
        print("   python3 upload_ftp.py --help")
