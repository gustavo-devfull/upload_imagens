#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar a correção do erro 'bytes-like object is required, not method'
"""

import os
import sys
from excel_image_extractor import ExcelImageExtractor

def testar_correcao_bytes():
    """Testa especificamente a correção do erro de bytes"""
    
    print("🔧 TESTE DA CORREÇÃO DO ERRO DE BYTES")
    print("=" * 45)
    
    # Configurações FTP
    FTP_HOST = "gpreto.space"
    FTP_USER = "u715606397.nova"
    FTP_PASSWORD = "]X9CC>t~ihWhdzNq"
    
    print("\n📋 Problema corrigido:")
    print("   ❌ Antes: 'a bytes-like object is required, not method'")
    print("   ✅ Agora: Verificação se atributo é callable antes de usar")
    
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
    
    print("\n🔍 Testando correção...")
    
    try:
        # Carrega o arquivo
        workbook = extractor.read_excel_file(excel_file)
        worksheet = workbook.active
        
        # Extrai imagens
        images = extractor.extract_images_from_worksheet(worksheet, start_row=4, photo_column='H')
        print(f"✅ Encontradas {len(images)} imagens")
        
        if not images:
            print("⚠️  Nenhuma imagem encontrada para testar")
            workbook.close()
            return True
        
        # Testa salvamento de cada imagem
        print("\n🧪 Testando salvamento de imagens...")
        sucessos = 0
        falhas = 0
        
        for i, (row, image) in enumerate(images[:5]):  # Testa apenas as primeiras 5
            try:
                print(f"   Testando imagem {i+1} (linha {row})...")
                print(f"   Tipo do objeto: {type(image)}")
                
                # Lista atributos disponíveis
                attrs = [attr for attr in dir(image) if not attr.startswith('_')]
                print(f"   Atributos disponíveis: {attrs[:10]}...")  # Mostra apenas os primeiros 10
                
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
                print(f"   Tipo do erro: {type(e)}")
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
                stats = extractor.process_excel_file(excel_file, start_row=4, photo_column='H')
                
                print("\n" + "="*50)
                print("📊 RESULTADOS FINAIS")
                print("="*50)
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
                return True
        else:
            print("\n⚠️  Ainda há problemas com algumas imagens")
            return False
            
    except Exception as e:
        print(f"\n❌ Erro durante o teste: {e}")
        return False


def mostrar_correcao_detalhada():
    """Mostra detalhes da correção implementada"""
    
    print("🔧 DETALHES DA CORREÇÃO DE BYTES")
    print("=" * 35)
    print()
    print("❌ Problema original:")
    print("   image._data  # Se _data for um método")
    print("   → 'a bytes-like object is required, not method'")
    print()
    print("✅ Solução implementada:")
    print("   data = image._data")
    print("   if callable(data):")
    print("       data = data()  # Chama o método")
    print("   f.write(data)")
    print()
    print("🎯 Melhorias:")
    print("   • Verifica se atributo é callable antes de usar")
    print("   • Múltiplos métodos de obtenção de dados")
    print("   • Tratamento robusto de diferentes tipos")
    print("   • Logging detalhado para debug")
    print()
    print("📋 Métodos testados:")
    print("   1. image.save() - método direto")
    print("   2. image.image.save() - através de image.image")
    print("   3. image._data - dados brutos")
    print("   4. image.ref - referência")
    print("   5. Busca automática em múltiplos atributos")


if __name__ == "__main__":
    print("🚀 Teste da Correção - Sistema de Extração de Imagens")
    print("   Versão 2.3 - Correção de Bytes")
    print()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--detalhes":
        mostrar_correcao_detalhada()
    else:
        sucesso = testar_correcao_bytes()
        
        if sucesso:
            print("\n🎉 Teste concluído com sucesso!")
            print("   A correção de bytes está funcionando!")
        else:
            print("\n⚠️  Ainda há problemas a resolver.")
        
        print("\n" + "="*50)
        print("❓ Para ver detalhes da correção:")
        print("   python testar_correcao_bytes.py --detalhes")
