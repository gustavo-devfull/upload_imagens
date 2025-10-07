#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo de uso do sistema de extração de imagens Excel
"""

import os
import sys
from excel_image_extractor import ExcelImageExtractor

def exemplo_uso():
    """Demonstra como usar o sistema"""
    
    print("🔧 EXEMPLO DE USO DO SISTEMA")
    print("=" * 40)
    
    # Configurações FTP (já configuradas)
    FTP_HOST = "gpreto.space"
    FTP_USER = "u715606397.nova"
    FTP_PASSWORD = "]X9CC>t~ihWhdzNq"
    
    # Solicita arquivo do usuário
    print("\n📁 Digite o caminho completo para seu arquivo Excel:")
    print("   Exemplo: /Users/usuario/Documents/planilha.xlsx")
    
    excel_file = input("\nCaminho: ").strip()
    
    # Remove aspas se o usuário colou com aspas
    excel_file = excel_file.strip('"\'')
    
    if not excel_file:
        print("❌ Nenhum arquivo especificado!")
        return
    
    if not os.path.exists(excel_file):
        print(f"❌ Arquivo não encontrado: {excel_file}")
        print("\n💡 Dicas:")
        print("   • Verifique se o caminho está correto")
        print("   • Use o caminho completo (absoluto)")
        print("   • No macOS, arraste o arquivo para o terminal para obter o caminho")
        return
    
    print(f"\n✅ Arquivo encontrado: {excel_file}")
    
    # Cria instância do extrator
    extractor = ExcelImageExtractor(FTP_HOST, FTP_USER, FTP_PASSWORD)
    
    print("\n🚀 Iniciando processamento...")
    print("   Isso pode levar alguns minutos dependendo do tamanho da planilha...")
    
    try:
        # Processa o arquivo (lendo a partir da linha 4, coluna PHOTO)
        stats = extractor.process_excel_file(excel_file, start_row=4, photo_column='H')
        
        # Exibe resultados detalhados
        print("\n" + "="*60)
        print("📊 RESULTADOS FINAIS")
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
            print(f"   http://46.202.90.62/A3.jpg")
            print(f"   http://46.202.90.62/A4.jpg")
            print(f"   http://46.202.90.62/A5.jpg")
        
        if stats['errors']:
            print(f"\n⚠️  Problemas encontrados ({len(stats['errors'])}):")
            for i, error in enumerate(stats['errors'], 1):
                print(f"   {i}. {error}")
        
        # Calcula taxa de sucesso
        if stats['total_refs'] > 0:
            success_rate = (stats['uploads_successful'] / stats['total_refs']) * 100
            print(f"\n📈 Taxa de sucesso: {success_rate:.1f}%")
            
            if success_rate == 100:
                print("🎉 Perfeito! Todas as imagens foram processadas com sucesso!")
            elif success_rate >= 80:
                print("👍 Bom resultado! A maioria das imagens foi processada.")
            elif success_rate >= 50:
                print("⚠️  Resultado parcial. Verifique os erros acima.")
            else:
                print("❌ Muitos problemas. Verifique a estrutura da planilha.")
        
        print("\n✨ Processamento concluído!")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Processamento interrompido pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        print("\n💡 Possíveis soluções:")
        print("   • Verifique se o arquivo Excel não está corrompido")
        print("   • Confirme se há imagens na planilha")
        print("   • Teste a conectividade com o servidor FTP")


def mostrar_instrucoes():
    """Mostra instruções de uso"""
    
    print("📖 INSTRUÇÕES DE USO")
    print("=" * 30)
    print()
    print("1️⃣  Prepare sua planilha Excel:")
    print("   • Coluna A deve conter os valores REF (ex: A3, A4, A5)")
    print("   • Coluna H (PHOTO) deve conter as imagens sobrepostas")
    print("   • Sistema lê a partir da linha 4 (ignora cabeçalhos)")
    print()
    print("2️⃣  Execute o sistema:")
    print("   python exemplo_uso.py")
    print()
    print("3️⃣  Digite o caminho para seu arquivo Excel")
    print()
    print("4️⃣  Aguarde o processamento")
    print()
    print("5️⃣  Acesse suas imagens em:")
    print("   http://46.202.90.62/")
    print()
    print("💡 DICAS:")
    print("   • Use caminhos absolutos para o arquivo Excel")
    print("   • No macOS, arraste o arquivo para o terminal")
    print("   • Certifique-se de que há imagens na planilha")
    print("   • O sistema salva as imagens como REF.jpg")


if __name__ == "__main__":
    print("🚀 Sistema de Extração de Imagens Excel → FTP")
    print("   Versão 1.0")
    print()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        mostrar_instrucoes()
    else:
        exemplo_uso()
        
        print("\n" + "="*50)
        print("❓ Precisa de ajuda? Execute:")
        print("   python exemplo_uso.py --help")
