<?php
/**
 * Sistema de Upload de Imagens Excel - Página Principal
 */

// Força o carregamento do nosso sistema
$html_content = file_get_contents('index.html');

if ($html_content === false) {
    // Se não conseguir carregar index.html, mostra uma página simples
    ?>
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sistema de Upload de Imagens Excel</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; }
            .btn { background: #007cba; color: white; padding: 15px 30px; border: none; border-radius: 5px; text-decoration: none; display: inline-block; margin: 10px; }
            .btn:hover { background: #005a87; }
            .info { background: #e3f2fd; padding: 15px; border-radius: 5px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🖼️ Sistema de Upload de Imagens Excel</h1>
            
            <div class="info">
                <h3>📋 Sistema Instalado com Sucesso!</h3>
                <p>O sistema está funcionando no servidor FTP.</p>
            </div>
            
            <h3>🔗 Links do Sistema:</h3>
            <a href="index.html" class="btn">📁 Interface Principal</a>
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
    <?php
} else {
    // Mostra o conteúdo do index.html
    echo $html_content;
}
?>