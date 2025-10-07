#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de upload via FTP para extração de imagens Excel
"""

import ftplib
import os
from excel_image_extractor import ExcelImageExtractor
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FTPImageExtractor(ExcelImageExtractor):
    """Classe para extrair imagens de planilhas Excel e fazer upload via FTP"""
    
    def __init__(self, ftp_host: str, ftp_user: str, ftp_password: str):
        """
        Inicializa o extrator com credenciais FTP
        
        Args:
            ftp_host: Host do servidor FTP
            ftp_user: Usuário FTP
            ftp_password: Senha FTP
        """
        self.ftp_host = ftp_host
        self.ftp_user = ftp_user
        self.ftp_password = ftp_password
        
        # Chama construtor pai
        super().__init__(ftp_host, ftp_user, ftp_password)
    
    def upload_to_ftp(self, local_file_path: str, remote_filename: str) -> bool:
        """
        Faz upload do arquivo para o servidor via FTP
        
        Args:
            local_file_path: Caminho do arquivo local
            remote_filename: Nome do arquivo no servidor
            
        Returns:
            True se upload foi bem-sucedido
        """
        try:
            # Verifica se arquivo existe e tem conteúdo
            if not os.path.exists(local_file_path):
                logger.error(f"Arquivo local não encontrado: {local_file_path}")
                return False
            
            file_size = os.path.getsize(local_file_path)
            if file_size == 0:
                logger.error(f"Arquivo local está vazio: {local_file_path}")
                return False
            
            logger.debug(f"Fazendo upload FTP de {local_file_path} ({file_size} bytes) como {remote_filename}")
            
            # Conecta via FTP
            with ftplib.FTP(timeout=300) as ftp:  # Timeout de 5 minutos
                ftp.connect(self.ftp_host, 21)  # Conecta explicitamente na porta 21
                ftp.login(self.ftp_user, self.ftp_password)
                
                # Cria diretórios se não existirem
                try:
                    ftp.mkd('public_html')
                    logger.debug("Diretório 'public_html' criado")
                except:
                    logger.debug("Diretório 'public_html' já existe")
                
                try:
                    ftp.cwd('public_html')
                    ftp.mkd('images')
                    logger.debug("Diretório 'images' criado")
                except:
                    logger.debug("Diretório 'images' já existe")
                
                try:
                    ftp.cwd('images')
                    ftp.mkd('products')
                    logger.debug("Diretório 'products' criado")
                except:
                    logger.debug("Diretório 'products' já existe")
                
                # Volta para o diretório raiz
                ftp.cwd('/')
                
                # Caminho completo para upload
                remote_path = f"public_html/images/products/{remote_filename}"
                
                # Abre arquivo local e faz upload
                with open(local_file_path, 'rb') as file:
                    ftp.storbinary(f'STOR {remote_path}', file)
                    
            logger.info(f"Upload FTP concluído: {remote_path}")
            logger.info(f"Imagem disponível em: https://ideolog.ia.br/images/products/{remote_filename}")
            return True
            
        except Exception as e:
            logger.error(f"Erro no upload FTP: {e}")
            return False
    
    def process_excel_file(self, excel_file_path: str, start_row: int = 4, photo_column: str = 'H') -> dict:
        """
        Processa arquivo Excel completo: extrai REFs, imagens e faz upload via FTP
        
        Args:
            excel_file_path: Caminho para o arquivo Excel
            start_row: Linha inicial para leitura (padrão: 4)
            photo_column: Coluna onde estão as imagens (padrão: 'H' para PHOTO)
            
        Returns:
            Dicionário com estatísticas do processamento
        """
        stats = {
            'total_refs': 0,
            'images_found': 0,
            'uploads_successful': 0,
            'uploads_failed': 0,
            'errors': [],
            'start_row': start_row,
            'photo_column': photo_column
        }
        
        try:
            # Carrega o arquivo Excel
            workbook = self.read_excel_file(excel_file_path)
            worksheet = workbook.active
            
            # Extrai dados da coluna REF a partir da linha especificada
            ref_data = self.get_ref_column_data(worksheet, start_row)
            stats['total_refs'] = len(ref_data)
            
            # Extrai imagens da coluna PHOTO a partir da linha especificada
            images = self.extract_images_from_worksheet(worksheet, start_row, photo_column)
            stats['images_found'] = len(images)
            
            # Processa cada REF
            for ref_row, ref_value in ref_data:
                try:
                    # Encontra imagem associada na mesma linha
                    image = self.find_image_for_ref(ref_row, images)
                    
                    if image:
                        temp_path = None
                        try:
                            # Salva imagem temporariamente
                            temp_path = self.save_image_to_temp(image, ref_value)
                            
                            # Faz upload via FTP
                            remote_filename = f"{ref_value}.jpg"
                            if self.upload_to_ftp(temp_path, remote_filename):
                                stats['uploads_successful'] += 1
                                logger.info(f"✅ REF {ref_value} (linha {ref_row}) processada com sucesso")
                            else:
                                stats['uploads_failed'] += 1
                                
                        finally:
                            # Remove arquivo temporário se foi criado
                            if temp_path and os.path.exists(temp_path):
                                try:
                                    os.remove(temp_path)
                                    logger.debug(f"Arquivo temporário removido: {temp_path}")
                                except Exception as e:
                                    logger.warning(f"Erro ao remover arquivo temporário {temp_path}: {e}")
                    else:
                        logger.warning(f"Nenhuma imagem encontrada para REF {ref_value} (linha {ref_row}) na coluna {photo_column}")
                        
                except Exception as e:
                    error_msg = f"Erro ao processar REF {ref_value}: {e}"
                    logger.error(error_msg)
                    stats['errors'].append(error_msg)
                    stats['uploads_failed'] += 1
            
            workbook.close()
            
        except Exception as e:
            error_msg = f"Erro geral no processamento: {e}"
            logger.error(error_msg)
            stats['errors'].append(error_msg)
            
        return stats


def main():
    """Função principal para upload via FTP"""
    
    print("🚀 UPLOAD VIA FTP - Sistema de Extração de Imagens")
    print("=" * 55)
    
    # Configurações FTP
    FTP_HOST = "46.202.90.62"
    FTP_USER = "u715606397.ideolog.ia.br"
    FTP_PASSWORD = "]X9CC>t~ihWhdzNq"
    
    print("\n📋 Configurações FTP:")
    print(f"   • Servidor: {FTP_HOST}")
    print(f"   • Porta: 21")
    print(f"   • Usuário: {FTP_USER}")
    print(f"   • Coluna REF: A")
    print(f"   • Coluna PHOTO: H")
    print(f"   • Linha inicial: 4")
    
    # Caminho do arquivo Excel
    excel_file_path = "/Users/gustavo/upload/tartaruga.xlsx"
    
    print(f"\n📁 Arquivo Excel: {excel_file_path}")
    
    # Verifica se arquivo existe
    if not os.path.exists(excel_file_path):
        print(f"❌ Arquivo não encontrado: {excel_file_path}")
        print("\n💡 Para usar este script:")
        print("   1. Edite a variável 'excel_file_path' no código")
        print("   2. Coloque o caminho completo para seu arquivo Excel")
        print("   3. Execute novamente: python3 upload_ftp_novo.py")
        return
    
    print(f"✅ Arquivo encontrado!")
    
    # Cria instância do extrator FTP
    extractor = FTPImageExtractor(FTP_HOST, FTP_USER, FTP_PASSWORD)
    
    print("\n🚀 Iniciando processamento e upload via FTP...")
    print("   Isso pode levar alguns minutos...")
    
    try:
        # Processa o arquivo e faz upload
        stats = extractor.process_excel_file(excel_file_path, start_row=4, photo_column='H')
        
        # Exibe resultados
        print("\n" + "="*60)
        print("📊 RESULTADOS DO UPLOAD FTP")
        print("="*60)
        print(f"📋 Linha inicial: {stats['start_row']}")
        print(f"🖼️  Coluna das imagens: {stats['photo_column']}")
        print(f"📋 REFs processadas: {stats['total_refs']}")
        print(f"🖼️  Imagens encontradas: {stats['images_found']}")
        print(f"✅ Uploads bem-sucedidos: {stats['uploads_successful']}")
        print(f"❌ Uploads falharam: {stats['uploads_failed']}")
        
        if stats['uploads_successful'] > 0:
            print(f"\n🌐 Suas imagens estão disponíveis em:")
            print(f"   https://ideolog.ia.br/images/products/")
            print(f"\n📝 Exemplos de URLs:")
            print(f"   https://ideolog.ia.br/images/products/T608.jpg")
            print(f"   https://ideolog.ia.br/images/products/106-6S.jpg")
        
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
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Upload interrompido pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro durante o upload: {e}")
        print("\n💡 Possíveis soluções:")
        print("   • Verifique se o arquivo Excel não está corrompido")
        print("   • Confirme se há imagens na coluna H")
        print("   • Teste a conectividade FTP")


if __name__ == "__main__":
    main()
