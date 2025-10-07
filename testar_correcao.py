#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar especificamente a correção do erro de imagem
"""

import os
import sys
from excel_image_extractor import ExcelImageExtractor

def testar_correcao_imagem():
    """Testa especificamente a correção do erro de imagem"""
    
    print("🔧 TESTE DA CORREÇÃO DO ERRO DE IMAGEM")
    print("=" * 45)
    
    # Configurações FTP
    FTP_HOST = "46.202.90.62"
    FTP_USER = "u715606397.gpreto.space"
    FTP_PASSWORD = "8:fRP;*OVPp3Oyc&"
    
    print("\n📋 Problema corrigido:")
    print("   ❌ Antes: 'Image' object has no attribute 'image'")
    print("   ✅ Agora: Método robusto com múltiplas tentativas")
    
    # Solicita arquivo
    print("\n📁 Digite o caminho para o arquivo Excel que estava dando erro:")
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
    
    print("\n🔍 Testando extração de imagens...")
    
    try:
        # Carrega o arquivo
        workbook = extractor.read_excel_file(excel_file)
        worksheet = workbook.active
        
        # Extrai imagens
        images = extractor.extract_images_from_worksheet(worksheet, start_row=4)
        print(f"✅ Encontradas {len(images)} imagens")
        
        if not images:
            print("⚠️  Nenhuma imagem encontrada para testar")
            workbook.close()
            return True
        
        # Testa salvamento de cada imagem
        print("\n🧪 Testando salvamento de imagens...")
        sucessos = 0
        falhas = 0
        
        for i, (row, image) in enumerate(images[:3]):  # Testa apenas as primeiras 3
            try:
                print(f"   Testando imagem {i+1} (linha {row})...")
                
                # Tenta salvar a imagem
                temp_path = extractor.save_image_to_temp(image, f"teste_{i+1}")
                
                # Verifica se arquivo foi criado
                if os.path.exists(temp_path):
                    file_size = os.path.getsize(temp_path)
                    print(f"   ✅ Sucesso! Arquivo criado: {file_size} bytes")
                    sucessos += 1
                    
                    # Remove arquivo de teste
                    os.remove(temp_path)
                else:
                    print(f"   ❌ Falha! Arquivo não foi criado")
                    falhas += 1
                    
            except Exception as e:
                print(f"   ❌ Erro ao salvar imagem {i+1}: {e}")
                falhas += 1
        
        workbook.close()
        
        print(f"\n📊 Resultado do teste:")
        print(f"   ✅ Sucessos: {sucessos}")
        print(f"   ❌ Falhas: {falhas}")
        
        if falhas == 0:
            print("\n🎉 Correção funcionando perfeitamente!")
            
            # Pergunta se quer fazer upload real
            print(f"\n❓ Deseja fazer upload real das imagens?")
            resposta = input("Digite 'sim' para continuar: ").strip().lower()
            
            if resposta in ['sim', 's', 'yes', 'y']:
                print("\n🚀 Iniciando processamento completo...")
                stats = extractor.process_excel_file(excel_file, start_row=4)
                
                print("\n" + "="*50)
                print("📊 RESULTADOS FINAIS")
                print("="*50)
                print(f"REFs processadas: {stats['total_refs']}")
                print(f"Imagens encontradas: {stats['images_found']}")
                print(f"Uploads bem-sucedidos: {stats['uploads_successful']}")
                print(f"Uploads falharam: {stats['uploads_failed']}")
                
                if stats['uploads_successful'] > 0:
                    print(f"\n🌐 Imagens disponíveis em: http://46.202.90.62/")
                
                return stats['uploads_successful'] > 0
            else:
                return True
        else:
            print("\n⚠️  Ainda há problemas com algumas imagens")
            return False
            
    except Exception as e:
        print(f"\n❌ Erro durante o teste: {e}")
        return False


def mostrar_correcao():
    """Mostra detalhes da correção implementada"""
    
    print("🔧 DETALHES DA CORREÇÃO")
    print("=" * 25)
    print()
    print("❌ Problema original:")
    print("   image.image.save(temp_path)")
    print("   → 'Image' object has no attribute 'image'")
    print()
    print("✅ Solução implementada:")
    print("   if hasattr(image, 'save'):")
    print("       image.save(temp_path)")
    print("   elif hasattr(image, 'image') and hasattr(image.image, 'save'):")
    print("       image.image.save(temp_path)")
    print("   elif hasattr(image, '_data'):")
    print("       f.write(image._data)")
    print("   else:")
    print("       # Converter para PIL e salvar")
    print()
    print("🎯 Benefícios:")
    print("   • Compatível com diferentes versões do openpyxl")
    print("   • Múltiplos métodos de salvamento")
    print("   • Tratamento robusto de erros")
    print("   • Logging detalhado para debug")


if __name__ == "__main__":
    print("🚀 Teste da Correção - Sistema de Extração de Imagens")
    print("   Versão 2.1 - Correção de Bug")
    print()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--detalhes":
        mostrar_correcao()
    else:
        sucesso = testar_correcao_imagem()
        
        if sucesso:
            print("\n🎉 Teste concluído com sucesso!")
            print("   A correção está funcionando!")
        else:
            print("\n⚠️  Ainda há problemas a resolver.")
        
        print("\n" + "="*50)
        print("❓ Para ver detalhes da correção:")
        print("   python testar_correcao.py --detalhes")

