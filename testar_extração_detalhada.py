#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste específico para extrair dados da imagem
"""

import openpyxl
import os

def testar_extração_detalhada():
    """Testa extração detalhada de dados de imagem"""
    
    arquivo = "/Users/gustavo/upload/tartaruga.xlsx"
    
    try:
        workbook = openpyxl.load_workbook(arquivo)
        worksheet = workbook.active
        
        image = worksheet._images[0]
        print(f"🖼️ Tipo da imagem: {type(image)}")
        
        # Testa _data
        print("\n🔍 TESTANDO _data:")
        if hasattr(image, '_data'):
            data_method = image._data
            print(f"   Tipo: {type(data_method)}")
            print(f"   É callable: {callable(data_method)}")
            
            try:
                data_bytes = data_method()
                print(f"   ✅ Dados extraídos: {len(data_bytes)} bytes")
                print(f"   Tipo dos dados: {type(data_bytes)}")
                
                # Tenta salvar
                temp_path = "/tmp/teste_data.jpg"
                with open(temp_path, 'wb') as f:
                    f.write(data_bytes)
                    f.flush()
                
                if os.path.exists(temp_path):
                    size = os.path.getsize(temp_path)
                    print(f"   ✅ Arquivo salvo: {temp_path} ({size} bytes)")
                    os.remove(temp_path)
                else:
                    print(f"   ❌ Arquivo não foi criado")
                    
            except Exception as e:
                print(f"   ❌ Erro ao extrair dados: {e}")
                import traceback
                traceback.print_exc()
        
        # Testa ref
        print("\n🔍 TESTANDO ref:")
        if hasattr(image, 'ref'):
            ref_obj = image.ref
            print(f"   Tipo: {type(ref_obj)}")
            print(f"   Tem read: {hasattr(ref_obj, 'read')}")
            print(f"   É callable: {callable(ref_obj)}")
            
            try:
                if hasattr(ref_obj, 'read'):
                    # É BytesIO
                    ref_obj.seek(0)  # Volta para o início
                    data_bytes = ref_obj.read()
                    print(f"   ✅ Dados lidos: {len(data_bytes)} bytes")
                    
                    # Tenta salvar
                    temp_path = "/tmp/teste_ref.jpg"
                    with open(temp_path, 'wb') as f:
                        f.write(data_bytes)
                        f.flush()
                    
                    if os.path.exists(temp_path):
                        size = os.path.getsize(temp_path)
                        print(f"   ✅ Arquivo salvo: {temp_path} ({size} bytes)")
                        os.remove(temp_path)
                    else:
                        print(f"   ❌ Arquivo não foi criado")
                        
                elif callable(ref_obj):
                    data_bytes = ref_obj()
                    print(f"   ✅ Dados extraídos: {len(data_bytes)} bytes")
                    
                    # Tenta salvar
                    temp_path = "/tmp/teste_ref_callable.jpg"
                    with open(temp_path, 'wb') as f:
                        f.write(data_bytes)
                        f.flush()
                    
                    if os.path.exists(temp_path):
                        size = os.path.getsize(temp_path)
                        print(f"   ✅ Arquivo salvo: {temp_path} ({size} bytes)")
                        os.remove(temp_path)
                    else:
                        print(f"   ❌ Arquivo não foi criado")
                        
            except Exception as e:
                print(f"   ❌ Erro ao processar ref: {e}")
                import traceback
                traceback.print_exc()
        
        workbook.close()
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    testar_extração_detalhada()
