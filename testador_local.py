#!/usr/bin/env python3
"""
🚀 TESTADOR LOCAL SIMPLES - Testa arquivos Excel diretamente
Versão que funciona sem servidor web
"""

import os
import sys
from sistema_melhorado import SistemaExcelMelhorado

def testar_arquivo_local(arquivo):
    """Testa um arquivo Excel local"""
    
    if not os.path.exists(arquivo):
        print(f"❌ Arquivo {arquivo} não existe!")
        return False
    
    print(f"\n🔍 TESTANDO ARQUIVO LOCAL")
    print(f"📁 Arquivo: {arquivo}")
    print("=" * 60)
    
    try:
        # Cria sistema melhorado
        sistema = SistemaExcelMelhorado(debug_mode=True)
        
        # Processa arquivo
        resultado = sistema.process_excel_melhorado(arquivo)
        
        if resultado['success']:
            print(f"\n✅ SUCESSO!")
            print(f"📊 Total de imagens: {resultado['total_images']}")
            print(f"🖼️ Imagens válidas: {resultado['images_found']}")
            print(f"📈 Imagens com REFs: {resultado['images_with_refs']}")
            print(f"❌ Imagens sem REFs: {resultado['images_without_refs']}")
            
            if resultado['images_by_column']:
                print(f"\n📋 Imagens por coluna:")
                for col, count in resultado['images_by_column'].items():
                    print(f"   • Coluna {col}: {count} imagens")
            
            if resultado['anchor_types']:
                print(f"\n🔗 Tipos de anchor:")
                for anchor_type, count in resultado['anchor_types'].items():
                    print(f"   • {anchor_type}: {count} imagens")
            
            if resultado['images_data']:
                print(f"\n🖼️ Detalhes das imagens:")
                for i, img in enumerate(resultado['images_data'], 1):
                    print(f"   {i}. REF: {img['ref']} | Posição: {img['col']}{img['row']} | Tipo: {img['anchor_type']}")
            
            if resultado['recommendations']:
                print(f"\n💡 Recomendações:")
                for rec in resultado['recommendations']:
                    print(f"   • {rec}")
            
            return True
        else:
            print(f"\n❌ ERRO!")
            print(f"Erro: {resultado['error']}")
            return False
            
    except Exception as e:
        print(f"\n❌ ERRO NO PROCESSAMENTO:")
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Função principal"""
    
    print("🚀 TESTADOR LOCAL SIMPLES")
    print("=" * 60)
    print("Testa arquivos Excel diretamente sem servidor web")
    print("=" * 60)
    
    # Lista de arquivos para testar
    arquivos_teste = [
        "fabrica_com_imagens.xlsx",
        "tartaruga.xlsx",
        "carrinho.xlsx",
        "nova.xlsx",
        "produto.xlsx"
    ]
    
    print("\n📋 ARQUIVOS DISPONÍVEIS:")
    for i, arquivo in enumerate(arquivos_teste, 1):
        existe = "✅" if os.path.exists(arquivo) else "❌"
        print(f"   {i}. {existe} {arquivo}")
    
    print(f"\n🎯 TESTANDO TODOS OS ARQUIVOS:")
    print("=" * 60)
    
    resultados = {}
    
    for arquivo in arquivos_teste:
        resultado = testar_arquivo_local(arquivo)
        resultados[arquivo] = resultado
    
    # Resumo final
    print(f"\n{'='*60}")
    print("📋 RESUMO FINAL")
    print("=" * 60)
    
    arquivos_validos = [arquivo for arquivo, valido in resultados.items() if valido]
    arquivos_invalidos = [arquivo for arquivo, valido in resultados.items() if not valido]
    
    if arquivos_validos:
        print("✅ ARQUIVOS VÁLIDOS:")
        for arquivo in arquivos_validos:
            print(f"   • {arquivo}")
    
    if arquivos_invalidos:
        print("❌ ARQUIVOS INVÁLIDOS:")
        for arquivo in arquivos_invalidos:
            print(f"   • {arquivo}")
    
    print(f"\n💡 Use os arquivos válidos para upload!")
    print(f"🔧 Para testar um arquivo específico:")
    print(f"   python testador_local.py fabrica_com_imagens.xlsx")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Testa arquivo específico passado como argumento
        arquivo = sys.argv[1]
        testar_arquivo_local(arquivo)
    else:
        # Testa todos os arquivos
        main()

