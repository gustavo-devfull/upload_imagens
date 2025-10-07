#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para verificar as modificações do sistema
"""

import os
import sys
from excel_image_extractor import ExcelImageExtractor

def testar_sistema():
    """Testa o sistema com um arquivo Excel"""
    
    print("🧪 TESTE DO SISTEMA ATUALIZADO")
    print("=" * 40)
    
    # Configurações FTP
    FTP_HOST = "gpreto.space"
    FTP_USER = "u715606397.nova"
    FTP_PASSWORD = "]X9CC>t~ihWhdzNq"
    
    print("\n📋 Configurações:")
    print(f"   • Linha inicial: 4")
    print(f"   • Detecção de imagens: Melhorada para imagens sobrepostas")
    print(f"   • Servidor FTP: {FTP_HOST}")
    
    # Solicita arquivo
    print("\n📁 Digite o caminho para seu arquivo Excel de teste:")
    excel_file = input("Caminho: ").strip().strip('"\'')
    
    if not excel_file:
        print("❌ Nenhum arquivo especificado!")
        return False
    
    if not os.path.exists(excel_file):
        print(f"❌ Arquivo não encontrado: {excel_file}")
        return False
    
    print(f"\n✅ Arquivo encontrado: {excel_file}")
    
    # Cria instância do extrator
    extractor = ExcelImageExtractor(FTP_HOST, FTP_USER, FTP_PASSWORD)
    
    print("\n🔍 Testando leitura da planilha...")
    
    try:
        # Testa apenas a leitura (sem upload)
        workbook = extractor.read_excel_file(excel_file)
        worksheet = workbook.active
        
        # Testa extração de REFs a partir da linha 4
        print("📋 Extraindo REFs a partir da linha 4...")
        ref_data = extractor.get_ref_column_data(worksheet, start_row=4)
        print(f"   ✅ Encontradas {len(ref_data)} REFs")
        
        if ref_data:
            print("   📝 Primeiras REFs encontradas:")
            for i, (row, ref) in enumerate(ref_data[:5]):  # Mostra apenas as primeiras 5
                print(f"      Linha {row}: {ref}")
            if len(ref_data) > 5:
                print(f"      ... e mais {len(ref_data) - 5} REFs")
        
        # Testa extração de imagens a partir da linha 4
        print("\n🖼️  Extraindo imagens a partir da linha 4...")
        images = extractor.extract_images_from_worksheet(worksheet, start_row=4)
        print(f"   ✅ Encontradas {len(images)} imagens")
        
        if images:
            print("   📝 Imagens encontradas:")
            for row, image in images[:5]:  # Mostra apenas as primeiras 5
                print(f"      Linha {row}: Imagem {image.width}x{image.height}")
            if len(images) > 5:
                print(f"      ... e mais {len(images) - 5} imagens")
        
        workbook.close()
        
        # Pergunta se quer fazer upload real
        print(f"\n❓ Deseja fazer upload real das imagens para o FTP?")
        print("   (Isso irá processar todas as imagens e fazer upload)")
        resposta = input("Digite 'sim' para continuar: ").strip().lower()
        
        if resposta in ['sim', 's', 'yes', 'y']:
            print("\n🚀 Iniciando processamento completo...")
            stats = extractor.process_excel_file(excel_file, start_row=4)
            
            print("\n" + "="*50)
            print("📊 RESULTADOS FINAIS")
            print("="*50)
            print(f"Linha inicial: {stats['start_row']}")
            print(f"REFs processadas: {stats['total_refs']}")
            print(f"Imagens encontradas: {stats['images_found']}")
            print(f"Uploads bem-sucedidos: {stats['uploads_successful']}")
            print(f"Uploads falharam: {stats['uploads_failed']}")
            
            if stats['uploads_successful'] > 0:
                print(f"\n🌐 Imagens disponíveis em: http://46.202.90.62/")
            
            if stats['errors']:
                print(f"\n⚠️  Erros encontrados:")
                for error in stats['errors']:
                    print(f"   • {error}")
            
            return stats['uploads_successful'] > 0
        else:
            print("\n✅ Teste de leitura concluído com sucesso!")
            print("   Sistema está funcionando corretamente.")
            return True
            
    except Exception as e:
        print(f"\n❌ Erro durante o teste: {e}")
        return False


def mostrar_melhorias():
    """Mostra as melhorias implementadas"""
    
    print("🆕 MELHORIAS IMPLEMENTADAS")
    print("=" * 30)
    print()
    print("✅ Leitura a partir da linha 4:")
    print("   • Ignora cabeçalhos automaticamente")
    print("   • Foca apenas nos dados relevantes")
    print()
    print("✅ Detecção melhorada de imagens:")
    print("   • Identifica imagens sobrepostas às células")
    print("   • Múltiplos métodos de detecção de posição")
    print("   • Filtragem por linha inicial")
    print()
    print("✅ Logging aprimorado:")
    print("   • Mostra linha inicial nos resultados")
    print("   • Feedback detalhado do processamento")
    print("   • Identificação clara de sucessos/falhas")
    print()
    print("✅ Tratamento de erros robusto:")
    print("   • Continua processamento mesmo com erros")
    print("   • Relatório detalhado de problemas")
    print("   • Limpeza automática de arquivos temporários")


if __name__ == "__main__":
    print("🚀 Sistema de Extração de Imagens Excel → FTP")
    print("   Versão 2.0 - Atualizada")
    print()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--melhorias":
        mostrar_melhorias()
    else:
        sucesso = testar_sistema()
        
        if sucesso:
            print("\n🎉 Teste concluído com sucesso!")
        else:
            print("\n⚠️  Teste concluído com problemas.")
        
        print("\n" + "="*50)
        print("❓ Para ver as melhorias implementadas:")
        print("   python testar_sistema.py --melhorias")
