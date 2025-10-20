#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste para identificar onde está a corrupção
"""

import ftplib
import tempfile
import os
import requests
from PIL import Image
import io

def test_ftp_upload_integrity():
    """Testa integridade do upload FTP"""
    
    print("🔍 Testando Integridade do Upload FTP")
    print("=" * 50)
    
    try:
        import openpyxl
        
        # Carrega Excel e extrai imagem
        workbook = openpyxl.load_workbook("tartaruga.xlsx", data_only=True, read_only=False)
        worksheet = workbook.active
        
        image = worksheet._images[0]
        image_bytes = image._data()
        
        # Converte para JPEG
        image_stream = io.BytesIO(image_bytes)
        pil_image = Image.open(image_stream)
        
        if pil_image.mode in ('RGBA', 'LA', 'P'):
            pil_image = pil_image.convert('RGB')
        
        # Salva arquivo local
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            local_path = temp_file.name
        
        pil_image.save(local_path, 'JPEG', quality=95, optimize=False, progressive=False)
        local_size = os.path.getsize(local_path)
        
        print(f"📁 Arquivo local criado: {local_size} bytes")
        
        # Lê conteúdo do arquivo local
        with open(local_path, 'rb') as f:
            local_content = f.read()
        
        print(f"📋 Cabeçalho local: {local_content[:8].hex()}")
        
        # Conecta FTP
        ftp = ftplib.FTP()
        ftp.connect("46.202.90.62", 21, timeout=30)
        ftp.login("u715606397.ideolog.ia.br", "]X9CC>t~ihWhdzNq")
        
        # Vai para diretório
        ftp.cwd('/public_html/images/products')
        
        # Upload do arquivo
        test_filename = "TESTE_INTEGRIDADE.jpg"
        
        print(f"⬆️ Fazendo upload: {test_filename}")
        with open(local_path, 'rb') as file:
            ftp.voidcmd('TYPE I')  # Modo binário
            ftp.storbinary(f'STOR {test_filename}', file)
        
        print(f"✅ Upload concluído")
        
        # Verifica se arquivo está no servidor
        file_list = ftp.nlst()
        if test_filename in file_list:
            print(f"✅ Arquivo confirmado no servidor")
        else:
            print(f"❌ Arquivo não encontrado no servidor")
        
        ftp.quit()
        
        # Baixa arquivo do servidor
        download_url = f"https://ideolog.ia.br/images/products/{test_filename}"
        print(f"📥 Baixando: {download_url}")
        
        response = requests.get(download_url, timeout=30)
        if response.status_code == 200:
            downloaded_content = response.content
            downloaded_size = len(downloaded_content)
            
            print(f"📊 Arquivo baixado: {downloaded_size} bytes")
            print(f"📋 Cabeçalho baixado: {downloaded_content[:8].hex()}")
            
            # Compara
            if local_content == downloaded_content:
                print(f"✅ Arquivos idênticos! Problema não é FTP")
            else:
                print(f"❌ Arquivos diferentes! Há corrupção")
                
                # Analisa diferenças
                analyze_differences(local_content, downloaded_content)
        
        else:
            print(f"❌ Erro no download: {response.status_code}")
        
        # Remove arquivo local
        os.unlink(local_path)
        
        workbook.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

def analyze_differences(local_content, downloaded_content):
    """Analisa diferenças entre arquivos"""
    
    print(f"\n🔬 Análise das Diferenças:")
    
    # Compara tamanhos
    local_size = len(local_content)
    downloaded_size = len(downloaded_content)
    
    print(f"📊 Tamanho local: {local_size} bytes")
    print(f"📊 Tamanho baixado: {downloaded_size} bytes")
    print(f"📊 Diferença: {abs(local_size - downloaded_size)} bytes")
    
    # Compara cabeçalhos
    print(f"📋 Cabeçalho local: {local_content[:16].hex()}")
    print(f"📋 Cabeçalho baixado: {downloaded_content[:16].hex()}")
    
    # Verifica se é JPEG válido
    if downloaded_content.startswith(b'\xff\xd8'):
        print(f"✅ Arquivo baixado tem cabeçalho JPEG válido")
    else:
        print(f"❌ Arquivo baixado não tem cabeçalho JPEG válido")
    
    # Tenta abrir com PIL
    try:
        image_stream = io.BytesIO(downloaded_content)
        pil_image = Image.open(image_stream)
        print(f"✅ PIL consegue abrir arquivo baixado: {pil_image.size}, {pil_image.format}")
    except Exception as e:
        print(f"❌ PIL não consegue abrir arquivo baixado: {e}")

def test_different_upload_methods():
    """Testa diferentes métodos de upload"""
    
    print(f"\n🧪 Testando Diferentes Métodos de Upload:")
    
    try:
        import openpyxl
        
        # Carrega Excel e extrai imagem
        workbook = openpyxl.load_workbook("tartaruga.xlsx", data_only=True, read_only=False)
        worksheet = workbook.active
        
        image = worksheet._images[0]
        image_bytes = image._data()
        
        # Converte para JPEG
        image_stream = io.BytesIO(image_bytes)
        pil_image = Image.open(image_stream)
        
        if pil_image.mode in ('RGBA', 'LA', 'P'):
            pil_image = pil_image.convert('RGB')
        
        # Testa diferentes configurações de salvamento
        configs = [
            ("JPEG qualidade 90", {'quality': 90, 'optimize': False, 'progressive': False}),
            ("JPEG qualidade 85", {'quality': 85, 'optimize': False, 'progressive': False}),
            ("JPEG qualidade 80", {'quality': 80, 'optimize': False, 'progressive': False}),
        ]
        
        for config_name, save_kwargs in configs:
            try:
                # Salva arquivo local
                with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                    local_path = temp_file.name
                
                pil_image.save(local_path, 'JPEG', **save_kwargs)
                local_size = os.path.getsize(local_path)
                
                print(f"   {config_name}: {local_size} bytes")
                
                # Upload via FTP
                ftp = ftplib.FTP()
                ftp.connect("46.202.90.62", 21, timeout=30)
                ftp.login("u715606397.ideolog.ia.br", "]X9CC>t~ihWhdzNq")
                ftp.cwd('/public_html/images/products')
                
                test_filename = f"TESTE_{config_name.replace(' ', '_')}.jpg"
                
                with open(local_path, 'rb') as file:
                    ftp.voidcmd('TYPE I')
                    ftp.storbinary(f'STOR {test_filename}', file)
                
                ftp.quit()
                
                # Baixa e compara
                download_url = f"https://ideolog.ia.br/images/products/{test_filename}"
                response = requests.get(download_url, timeout=30)
                
                if response.status_code == 200:
                    downloaded_size = len(response.content)
                    print(f"      Baixado: {downloaded_size} bytes")
                    
                    if local_size == downloaded_size:
                        print(f"      ✅ Integridade mantida!")
                    else:
                        print(f"      ❌ Corrupção detectada!")
                
                # Remove arquivo local
                os.unlink(local_path)
                
            except Exception as e:
                print(f"   ❌ Erro {config_name}: {e}")
        
        workbook.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    test_ftp_upload_integrity()
    test_different_upload_methods()
    
    print(f"\n💡 PRÓXIMOS PASSOS:")
    print(f"1. Se há corrupção, problema é no servidor ou FTP")
    print(f"2. Se não há corrupção, problema é na configuração JPEG")
    print(f"3. Teste diferentes configurações para encontrar uma que funcione")


