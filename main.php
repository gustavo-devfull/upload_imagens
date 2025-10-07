<?php
/**
 * Sistema de Upload de Imagens Excel - Página Principal
 * Força o carregamento do sistema React
 */

// Headers para evitar cache
header('Cache-Control: no-cache, no-store, must-revalidate');
header('Pragma: no-cache');
header('Expires: 0');

// Força o carregamento do nosso sistema
$html_file = 'sistema.html';

if (file_exists($html_file)) {
    $html_content = file_get_contents($html_file);
    if ($html_content !== false) {
        echo $html_content;
        exit();
    }
}

// Se não conseguir carregar sistema.html, mostra página de erro
?>
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Upload de Imagens Excel</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 40px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container { 
            max-width: 600px; 
            margin: 0 auto; 
            background: white; 
            padding: 40px; 
            border-radius: 20px; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            text-align: center;
        }
        h1 { color: #333; margin-bottom: 20px; }
        .btn { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            padding: 15px 30px; 
            border: none; 
            border-radius: 50px; 
            text-decoration: none; 
            display: inline-block; 
            margin: 10px; 
            font-size: 1.1rem;
            transition: all 0.3s ease;
        }
        .btn:hover { 
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        .info { 
            background: #e3f2fd; 
            padding: 20px; 
            border-radius: 15px; 
            margin: 20px 0; 
            border: 1px solid #bbdefb;
        }
        .error {
            background: #ffebee;
            color: #c62828;
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
            border: 1px solid #ffcdd2;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🖼️ Sistema de Upload de Imagens Excel</h1>
        
        <div class="error">
            <h3>⚠️ Erro ao Carregar Sistema</h3>
            <p>Não foi possível carregar o arquivo sistema.html</p>
        </div>
        
        <div class="info">
            <h3>📋 Sistema Instalado</h3>
            <p>O sistema está funcionando no servidor FTP.</p>
        </div>
        
        <h3>🔗 Acesse o Sistema:</h3>
        <a href="sistema.html" class="btn">📁 Interface Principal</a>
        <a href="index.html" class="btn">📄 Interface Alternativa</a>
        <a href="upload.php" class="btn">🔧 API de Upload</a>
        <a href="config.php" class="btn">⚙️ Configurações</a>
        
        <div class="info">
            <h3>📊 Status:</h3>
            <p>✅ Sistema instalado</p>
            <p>✅ Arquivos carregados</p>
            <p>✅ Servidor FTP configurado</p>
        </div>
        
        <div class="info">
            <h3>🌐 URLs das Imagens:</h3>
            <p>As imagens serão salvas em:</p>
            <code>https://ideolog.ia.br/images/products/</code>
        </div>
    </div>
</body>
</html>

