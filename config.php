<?php
/**
 * Configuração do Sistema de Upload de Imagens Excel
 * 
 * INSTRUÇÕES DE INSTALAÇÃO NO SERVIDOR FTP:
 * 
 * 1. Faça upload dos seguintes arquivos para o diretório public_html:
 *    - index.html (interface React)
 *    - upload.php (processador de uploads)
 *    - config.php (este arquivo)
 * 
 * 2. Configure as credenciais FTP no arquivo upload.php:
 *    - FTP_HOST: Seu servidor FTP
 *    - FTP_USER: Seu usuário FTP
 *    - FTP_PASS: Sua senha FTP
 * 
 * 3. Teste o sistema acessando: https://seudominio.com/
 * 
 * 4. Para processar Excel real, instale PhpSpreadsheet:
 *    composer require phpoffice/phpspreadsheet
 */

// Configurações do sistema
$config = [
    'version' => '1.0.0',
    'name' => 'Sistema de Upload de Imagens Excel',
    'description' => 'Extrai imagens de planilhas Excel e faz upload via FTP',
    
    // Configurações FTP
    'ftp' => [
        'host' => '46.202.90.62',
        'port' => 21,
        'user' => 'u715606397.ideolog.ia.br',
        'pass' => ']X9CC>t~ihWhdzNq',
        'upload_dir' => 'images/products/',
        'timeout' => 300
    ],
    
    // Configurações de upload
    'upload' => [
        'max_file_size' => 50 * 1024 * 1024, // 50MB
        'allowed_extensions' => ['xlsx'],
        'temp_dir' => sys_get_temp_dir()
    ],
    
    // Configurações da planilha Excel
    'excel' => [
        'ref_column' => 'A',
        'photo_column' => 'H', 
        'start_row' => 4,
        'invalid_refs' => [
            'TOTAL', 'SUBTOTAL', 'SUM', 'COUNT', 'AVERAGE', 'MAX', 'MIN',
            'TOTAIS', 'SUBTOTAIS', 'SOMA', 'CONTAGEM', 'MÉDIA', 'MÁXIMO', 'MÍNIMO'
        ]
    ],
    
    // URLs
    'urls' => [
        'domain' => 'https://ideolog.ia.br',
        'images_base' => 'https://ideolog.ia.br/images/products/',
        'api_base' => 'https://ideolog.ia.br/upload.php'
    ]
];

// Função para obter configuração
function getConfig($key = null) {
    global $config;
    
    if ($key === null) {
        return $config;
    }
    
    $keys = explode('.', $key);
    $value = $config;
    
    foreach ($keys as $k) {
        if (isset($value[$k])) {
            $value = $value[$k];
        } else {
            return null;
        }
    }
    
    return $value;
}

// Função para verificar se o sistema está configurado corretamente
function checkSystemRequirements() {
    $requirements = [
        'php_version' => version_compare(PHP_VERSION, '7.4.0', '>='),
        'ftp_extension' => extension_loaded('ftp'),
        'file_uploads' => ini_get('file_uploads'),
        'upload_max_filesize' => ini_get('upload_max_filesize'),
        'post_max_size' => ini_get('post_max_size'),
        'temp_dir_writable' => is_writable(sys_get_temp_dir())
    ];
    
    return $requirements;
}

// Função para testar conexão FTP
function testFTPConnection() {
    $config = getConfig('ftp');
    
    try {
        $connection = ftp_connect($config['host'], $config['port']);
        if (!$connection) {
            return ['success' => false, 'error' => 'Erro ao conectar ao servidor FTP'];
        }
        
        if (!ftp_login($connection, $config['user'], $config['pass'])) {
            ftp_close($connection);
            return ['success' => false, 'error' => 'Erro ao fazer login no FTP'];
        }
        
        ftp_close($connection);
        return ['success' => true, 'message' => 'Conexão FTP funcionando'];
        
    } catch (Exception $e) {
        return ['success' => false, 'error' => $e->getMessage()];
    }
}

// Função para criar diretórios necessários
function createDirectories() {
    $config = getConfig('ftp');
    
    try {
        $connection = ftp_connect($config['host'], $config['port']);
        ftp_login($connection, $config['user'], $config['pass']);
        
        $directories = [
            'public_html',
            'public_html/images',
            'public_html/images/products'
        ];
        
        foreach ($directories as $dir) {
            if (!@ftp_chdir($connection, $dir)) {
                if (!@ftp_mkdir($connection, $dir)) {
                    error_log("Erro ao criar diretório: $dir");
                }
            }
        }
        
        ftp_close($connection);
        return true;
        
    } catch (Exception $e) {
        error_log("Erro ao criar diretórios: " . $e->getMessage());
        return false;
    }
}

// Se acessado diretamente, mostra informações do sistema
if (basename($_SERVER['PHP_SELF']) === 'config.php') {
    header('Content-Type: application/json');
    
    $systemInfo = [
        'config' => $config,
        'requirements' => checkSystemRequirements(),
        'ftp_test' => testFTPConnection(),
        'directories_created' => createDirectories(),
        'server_info' => [
            'php_version' => PHP_VERSION,
            'server_software' => $_SERVER['SERVER_SOFTWARE'] ?? 'Unknown',
            'document_root' => $_SERVER['DOCUMENT_ROOT'] ?? 'Unknown',
            'current_time' => date('Y-m-d H:i:s')
        ]
    ];
    
    echo json_encode($systemInfo, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
}
?>


