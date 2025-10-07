<?php
/**
 * Sistema de Upload de Imagens Excel - Página Principal
 * Versão que funciona no servidor FTP
 */

// Headers para evitar cache e problemas de segurança
header('Cache-Control: no-cache, no-store, must-revalidate');
header('Pragma: no-cache');
header('Expires: 0');
header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: DENY');

// Configurações do sistema
$system_config = [
    'version' => '1.0.0',
    'name' => 'Sistema de Upload de Imagens Excel',
    'ftp_host' => '46.202.90.62',
    'ftp_user' => 'u715606397.ideolog.ia.br',
    'domain' => 'https://ideolog.ia.br',
    'images_url' => 'https://ideolog.ia.br/images/products/'
];

?>
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo $system_config['name']; ?></title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            font-weight: 300;
        }

        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }

        .content {
            padding: 40px;
        }

        .upload-area {
            border: 3px dashed #667eea;
            border-radius: 15px;
            padding: 40px;
            text-align: center;
            margin-bottom: 30px;
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .upload-area:hover {
            border-color: #764ba2;
            background: #f8f9ff;
        }

        .upload-icon {
            font-size: 4rem;
            color: #667eea;
            margin-bottom: 20px;
        }

        .upload-text {
            font-size: 1.2rem;
            color: #333;
            margin-bottom: 10px;
        }

        .upload-subtext {
            color: #666;
            font-size: 0.9rem;
        }

        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 50px;
            font-size: 1.1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            margin: 10px;
            text-decoration: none;
            display: inline-block;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }

        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .info-box {
            background: #e3f2fd;
            border: 1px solid #bbdefb;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }

        .info-box h3 {
            color: #1976d2;
            margin-bottom: 10px;
        }

        .info-box ul {
            margin-left: 20px;
        }

        .info-box li {
            margin-bottom: 5px;
            color: #424242;
        }

        .status-box {
            background: #e8f5e8;
            border: 1px solid #c8e6c9;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }

        .status-box h3 {
            color: #2e7d32;
            margin-bottom: 10px;
        }

        .urls-box {
            background: #fff3e0;
            border: 1px solid #ffcc02;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }

        .urls-box h3 {
            color: #f57c00;
            margin-bottom: 10px;
        }

        .url-item {
            background: white;
            padding: 10px;
            border-radius: 5px;
            margin: 5px 0;
            border: 1px solid #e0e0e0;
        }

        .url-item code {
            background: #f5f5f5;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: monospace;
        }

        @media (max-width: 768px) {
            .container {
                margin: 10px;
                border-radius: 15px;
            }
            
            .header {
                padding: 20px;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .content {
                padding: 20px;
            }
            
            .upload-area {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🖼️ Sistema de Upload de Imagens Excel</h1>
            <p>Extraia imagens de planilhas Excel e faça upload para o servidor FTP</p>
        </div>

        <div class="content">
            <div class="status-box">
                <h3>✅ Sistema Funcionando</h3>
                <p>O sistema está instalado e funcionando no servidor FTP.</p>
                <p><strong>Versão:</strong> <?php echo $system_config['version']; ?></p>
                <p><strong>Servidor:</strong> <?php echo $system_config['ftp_host']; ?></p>
            </div>

            <div class="info-box">
                <h3>📋 Informações Importantes</h3>
                <ul>
                    <li><strong>Coluna REF:</strong> A (códigos dos produtos)</li>
                    <li><strong>Coluna PHOTO:</strong> H (imagens)</li>
                    <li><strong>Linha inicial:</strong> 4</li>
                    <li><strong>Formato:</strong> Apenas arquivos .xlsx</li>
                    <li><strong>Limite:</strong> 50MB por arquivo</li>
                </ul>
            </div>

            <div class="upload-area" onclick="document.getElementById('fileInput').click()">
                <div class="upload-icon">📁</div>
                <div class="upload-text">Clique para selecionar arquivo Excel</div>
                <div class="upload-subtext">Apenas arquivos .xlsx são aceitos</div>
            </div>

            <input type="file" id="fileInput" accept=".xlsx" style="display: none;" onchange="handleFileSelect(this.files[0])">

            <div style="text-align: center;">
                <button class="btn" onclick="uploadFile()" id="uploadBtn" disabled>
                    🚀 Fazer Upload
                </button>
                <button class="btn" onclick="resetForm()" id="resetBtn" disabled>
                    🔄 Limpar
                </button>
            </div>

            <div id="progressContainer" style="display: none; margin: 30px 0;">
                <div style="width: 100%; height: 20px; background: #e9ecef; border-radius: 10px; overflow: hidden; margin-bottom: 10px;">
                    <div id="progressFill" style="height: 100%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); width: 0%; transition: width 0.3s ease;"></div>
                </div>
                <div id="progressText" style="text-align: center; color: #666; font-size: 0.9rem;"></div>
            </div>

            <div id="results" style="display: none; margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 15px;">
                <h3 style="margin-bottom: 20px; color: #333;">📊 Resultados do Processamento</h3>
                <div id="resultsContent"></div>
            </div>

            <div class="urls-box">
                <h3>🌐 URLs das Imagens</h3>
                <p>As imagens processadas estarão disponíveis em:</p>
                <div class="url-item">
                    <strong>Base URL:</strong> <code><?php echo $system_config['images_url']; ?></code>
                </div>
                <div class="url-item">
                    <strong>Exemplo:</strong> <code><?php echo $system_config['images_url']; ?>CHDJ25001.jpg</code>
                </div>
            </div>

            <div class="info-box">
                <h3>🔧 APIs Disponíveis</h3>
                <div class="url-item">
                    <strong>Upload:</strong> <code>upload.php</code>
                </div>
                <div class="url-item">
                    <strong>Configurações:</strong> <code>config.php</code>
                </div>
            </div>
        </div>
    </div>

    <script>
        let selectedFile = null;

        function handleFileSelect(file) {
            if (file && file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') {
                selectedFile = file;
                document.getElementById('uploadBtn').disabled = false;
                document.getElementById('resetBtn').disabled = false;
                document.querySelector('.upload-text').textContent = file.name;
                document.querySelector('.upload-area').style.borderColor = '#28a745';
                document.querySelector('.upload-area').style.backgroundColor = '#f8fff8';
            } else {
                alert('Por favor, selecione um arquivo Excel (.xlsx) válido.');
            }
        }

        function uploadFile() {
            if (!selectedFile) {
                alert('Por favor, selecione um arquivo Excel.');
                return;
            }

            const formData = new FormData();
            formData.append('excel_file', selectedFile);

            // Mostra progresso
            document.getElementById('progressContainer').style.display = 'block';
            document.getElementById('uploadBtn').disabled = true;
            document.getElementById('resetBtn').disabled = true;

            // Simula progresso
            let progress = 0;
            const progressInterval = setInterval(() => {
                progress += 10;
                document.getElementById('progressFill').style.width = progress + '%';
                
                if (progress < 50) {
                    document.getElementById('progressText').textContent = 'Enviando arquivo...';
                } else if (progress < 90) {
                    document.getElementById('progressText').textContent = 'Processando imagens...';
                } else {
                    document.getElementById('progressText').textContent = 'Finalizando upload...';
                }
            }, 200);

            fetch('upload.php', {
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                clearInterval(progressInterval);
                document.getElementById('progressFill').style.width = '100%';
                document.getElementById('progressText').textContent = 'Upload concluído!';
                
                setTimeout(() => {
                    showResults(data);
                }, 500);
            })
            .catch(error => {
                clearInterval(progressInterval);
                alert('Erro no upload: ' + error.message);
                document.getElementById('uploadBtn').disabled = false;
                document.getElementById('resetBtn').disabled = false;
            });
        }

        function showResults(data) {
            const resultsDiv = document.getElementById('results');
            const contentDiv = document.getElementById('resultsContent');
            
            let html = `
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 20px; margin: 20px 0;">
                    <div style="background: white; padding: 20px; border-radius: 15px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.08);">
                        <div style="font-size: 2rem; font-weight: bold; color: #667eea; margin-bottom: 5px;">${data.total_refs}</div>
                        <div style="color: #666; font-size: 0.9rem;">REFs Processadas</div>
                    </div>
                    <div style="background: white; padding: 20px; border-radius: 15px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.08);">
                        <div style="font-size: 2rem; font-weight: bold; color: #667eea; margin-bottom: 5px;">${data.images_found}</div>
                        <div style="color: #666; font-size: 0.9rem;">Imagens Encontradas</div>
                    </div>
                    <div style="background: white; padding: 20px; border-radius: 15px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.08);">
                        <div style="font-size: 2rem; font-weight: bold; color: #28a745; margin-bottom: 5px;">${data.uploads_successful}</div>
                        <div style="color: #666; font-size: 0.9rem;">Uploads Bem-sucedidos</div>
                    </div>
                    <div style="background: white; padding: 20px; border-radius: 15px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.08);">
                        <div style="font-size: 2rem; font-weight: bold; color: #dc3545; margin-bottom: 5px;">${data.uploads_failed}</div>
                        <div style="color: #666; font-size: 0.9rem;">Uploads Falharam</div>
                    </div>
                </div>
            `;

            if (data.images && data.images.length > 0) {
                html += '<h4 style="margin-bottom: 15px; color: #333;">🖼️ Imagens Processadas</h4>';
                data.images.forEach(image => {
                    html += `
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 15px; background: white; border-radius: 10px; margin-bottom: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                            <div style="flex: 1; margin-left: 15px;">
                                <div style="font-weight: 600; color: #333; margin-bottom: 5px;">${image.name}</div>
                                <div style="font-size: 0.8rem; color: #666; word-break: break-all;">${image.url}</div>
                            </div>
                            <button onclick="copyToClipboard('${image.url}')" style="background: #28a745; color: white; border: none; padding: 8px 15px; border-radius: 20px; font-size: 0.8rem; cursor: pointer;">
                                📋 Copiar URL
                            </button>
                        </div>
                    `;
                });
            }

            contentDiv.innerHTML = html;
            resultsDiv.style.display = 'block';
            
            document.getElementById('uploadBtn').disabled = false;
            document.getElementById('resetBtn').disabled = false;
        }

        function resetForm() {
            selectedFile = null;
            document.getElementById('fileInput').value = '';
            document.getElementById('uploadBtn').disabled = true;
            document.getElementById('resetBtn').disabled = true;
            document.querySelector('.upload-text').textContent = 'Clique para selecionar arquivo Excel';
            document.querySelector('.upload-area').style.borderColor = '#667eea';
            document.querySelector('.upload-area').style.backgroundColor = 'transparent';
            document.getElementById('progressContainer').style.display = 'none';
            document.getElementById('results').style.display = 'none';
        }

        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(() => {
                alert('URL copiada para a área de transferência!');
            }).catch(() => {
                // Fallback para navegadores mais antigos
                const textArea = document.createElement('textarea');
                textArea.value = text;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                alert('URL copiada para a área de transferência!');
            });
        }
    </script>
</body>
</html>


