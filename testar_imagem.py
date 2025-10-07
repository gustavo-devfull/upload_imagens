#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar extração de dados de imagem do openpyxl
"""

import openpyxl
import os

def testar_extração_imagem():
    """Testa diferentes métodos de extração de dados de imagem"""
    
    arquivo = "/Users/gustavo/upload/tartaruga.xlsx"
    
    if not os.path.exists(arquivo):
        print("❌ Arquivo não encontrado")
        return
    
    try:
        workbook = openpyxl.load_workbook(arquivo)
        worksheet = workbook.active
        
        print(f"📊 Total de imagens: {len(worksheet._images)}")
        
        if len(worksheet._images) == 0:
            print("❌ Nenhuma imagem encontrada")
            return
        
        image = worksheet._images[0]
        print(f"🖼️ Tipo da imagem: {type(image)}")
        print(f"📋 Atributos disponíveis: {[attr for attr in dir(image) if not attr.startswith('_')]}")
        
        # Testa diferentes métodos de extração
        print("\n🔍 TESTANDO MÉTODOS DE EXTRAÇÃO:")
        
        # Método 1: _data
        if hasattr(image, '_data'):
            print("✅ Tem atributo _data")
            try:
                data = image._data
                print(f"   Tipo: {type(data)}")
                if callable(data):
                    data_bytes = data()
                    print(f"   Dados extraídos: {len(data_bytes)} bytes")
                else:
                    print(f"   Dados diretos: {len(data)} bytes")
            except Exception as e:
                print(f"   ❌ Erro: {e}")
        else:
            print("❌ Sem atributo _data")
        
        # Método 2: ref
        if hasattr(image, 'ref'):
            print("✅ Tem atributo ref")
            try:
                ref_data = image.ref
                print(f"   Tipo: {type(ref_data)}")
                if callable(ref_data):
                    ref_bytes = ref_data()
                    print(f"   Dados extraídos: {len(ref_bytes)} bytes")
                else:
                    print(f"   Dados diretos: {len(ref_data)} bytes")
            except Exception as e:
                print(f"   ❌ Erro: {e}")
        else:
            print("❌ Sem atributo ref")
        
        # Método 3: path
        if hasattr(image, 'path'):
            print("✅ Tem atributo path")
            try:
                path = image.path
                print(f"   Path: {path}")
            except Exception as e:
                print(f"   ❌ Erro: {e}")
        else:
            print("❌ Sem atributo path")
        
        # Método 4: Tentar salvar diretamente
        print("\n💾 TESTANDO SALVAMENTO DIRETO:")
        try:
            temp_path = "/tmp/teste_imagem.jpg"
            image.save(temp_path)
            if os.path.exists(temp_path):
                size = os.path.getsize(temp_path)
                print(f"✅ Salvamento direto funcionou: {temp_path} ({size} bytes)")
                os.remove(temp_path)
            else:
                print("❌ Arquivo não foi criado")
        except Exception as e:
            print(f"❌ Erro no salvamento direto: {e}")
        
        # Método 5: Usar PIL
        print("\n🖼️ TESTANDO COM PIL:")
        try:
            from PIL import Image as PILImage
            import io
            
            # Tenta obter dados brutos
            if hasattr(image, '_data'):
                data = image._data
                if callable(data):
                    data = data()
                
                if isinstance(data, bytes):
                    # Cria imagem PIL a partir dos dados
                    pil_image = PILImage.open(io.BytesIO(data))
                    temp_path = "/tmp/teste_pil.jpg"
                    pil_image.save(temp_path)
                    
                    if os.path.exists(temp_path):
                        size = os.path.getsize(temp_path)
                        print(f"✅ Salvamento com PIL funcionou: {temp_path} ({size} bytes)")
                        os.remove(temp_path)
                    else:
                        print("❌ Arquivo PIL não foi criado")
                else:
                    print("❌ Dados não são bytes")
            else:
                print("❌ Sem dados para PIL")
                
        except Exception as e:
            print(f"❌ Erro com PIL: {e}")
        
        workbook.close()
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    testar_extração_imagem()
