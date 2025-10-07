<?php
/**
 * Sistema de Upload de Imagens Excel - Versão Online Corrigida
 * Upload direto para o diretório raiz do servidor
 */

// Headers para evitar problemas de CORS e cache
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
header('Cache-Control: no-cache, no-store, must-revalidate');
header('Pragma: no-cache');
header('Expires: 0');

// Configurações do sistema
$config = [
    'ftp_host' => '46.202.90.62',
    'ftp_user' => 'u715606397.ideolog.ia.br',
    'ftp_password' => ']X9CC>t~ihWhdzNq',
    'ftp_remote_dir' => 'public_html/images/products/',
    'base_url' => 'https://ideolog.ia.br/images/products/',
    'max_file_size' => 50 * 1024 * 1024, // 50MB
    'allowed_types' => ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
];

// Função para log de erros
function log_error($message) {
    error_log("[Excel Upload] " . $message);
}

// Função para criar diretórios FTP
function create_ftp_directories($ftp, $path) {
    $dirs = explode('/', trim($path, '/'));
    $current_path = '';
    
    foreach ($dirs as $dir) {
        if (empty($dir)) continue;
        
        $current_path .= '/' . $dir;
        
        try {
            $ftp->mkdir($current_path);
            error_log("Diretório criado: $current_path");
        } catch (Exception $e) {
            // Diretório já existe ou erro
            error_log("Diretório $current_path já existe ou erro: " . $e->getMessage());
        }
    }
}

// Função para fazer upload FTP
function upload_to_ftp($local_file, $remote_filename, $config) {
    try {
        $ftp = new FTPConnection();
        $ftp->connect($config['ftp_host'], 21);
        $ftp->login($config['ftp_user'], $config['ftp_password']);
        
        // Cria diretórios necessários
        create_ftp_directories($ftp, $config['ftp_remote_dir']);
        
        // Faz upload do arquivo
        $remote_path = $config['ftp_remote_dir'] . $remote_filename;
        $result = $ftp->put($remote_path, $local_file, FTP_BINARY);
        
        $ftp->close();
        
        if ($result) {
            return [
                'success' => true,
                'url' => $config['base_url'] . $remote_filename,
                'path' => $remote_path
            ];
        } else {
            return [
                'success' => false,
                'error' => 'Falha no upload FTP'
            ];
        }
        
    } catch (Exception $e) {
        log_error("Erro FTP: " . $e->getMessage());
        return [
            'success' => false,
            'error' => 'Erro de conexão FTP: ' . $e->getMessage()
        ];
    }
}

// Função para processar arquivo Excel (simulação)
function process_excel_file($file_path) {
    // Por enquanto, simula o processamento
    // Em uma implementação real, você usaria uma biblioteca PHP para ler Excel
    
    $result = [
        'total_refs' => 1,
        'images_found' => 1,
        'uploads_successful' => 0,
        'uploads_failed' => 0,
        'images' => []
    ];
    
    // Simula uma imagem processada
    $test_filename = 'teste_' . time() . '.jpg';
    $test_image_path = sys_get_temp_dir() . '/' . $test_filename;
    
    // Cria um arquivo de teste (imagem vazia)
    file_put_contents($test_image_path, '');
    
    // Tenta fazer upload
    $upload_result = upload_to_ftp($test_image_path, $test_filename, $GLOBALS['config']);
    
    if ($upload_result['success']) {
        $result['uploads_successful'] = 1;
        $result['images'][] = [
            'name' => 'Imagem de teste',
            'url' => $upload_result['url']
        ];
    } else {
        $result['uploads_failed'] = 1;
        $result['error'] = $upload_result['error'];
    }
    
    // Remove arquivo temporário
    if (file_exists($test_image_path)) {
        unlink($test_image_path);
    }
    
    return $result;
}

// Processa requisições
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit(0);
}

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    // Retorna informações do sistema
    echo json_encode([
        'status' => 'ok',
        'message' => 'Sistema de Upload de Imagens Excel',
        'version' => '2.0',
        'config' => [
            'ftp_host' => $config['ftp_host'],
            'base_url' => $config['base_url'],
            'max_file_size' => $config['max_file_size']
        ]
    ]);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Verifica se há arquivo enviado
    if (!isset($_FILES['excel_file'])) {
        echo json_encode(['error' => 'Nenhum arquivo enviado']);
        exit;
    }
    
    $file = $_FILES['excel_file'];
    
    // Verifica erros de upload
    if ($file['error'] !== UPLOAD_ERR_OK) {
        echo json_encode(['error' => 'Erro no upload: ' . $file['error']]);
        exit;
    }
    
    // Verifica tamanho do arquivo
    if ($file['size'] > $config['max_file_size']) {
        echo json_encode(['error' => 'Arquivo muito grande. Máximo: 50MB']);
        exit;
    }
    
    // Verifica tipo do arquivo
    if (!in_array($file['type'], $config['allowed_types'])) {
        echo json_encode(['error' => 'Apenas arquivos .xlsx são permitidos']);
        exit;
    }
    
    // Salva arquivo temporariamente
    $temp_path = sys_get_temp_dir() . '/' . uniqid() . '_' . $file['name'];
    
    if (!move_uploaded_file($file['tmp_name'], $temp_path)) {
        echo json_encode(['error' => 'Erro ao salvar arquivo temporário']);
        exit;
    }
    
    try {
        // Processa o arquivo Excel
        $result = process_excel_file($temp_path);
        
        // Adiciona informações do arquivo
        $result['filename'] = $file['name'];
        $result['size'] = $file['size'];
        $result['success'] = true;
        
        echo json_encode($result);
        
    } catch (Exception $e) {
        log_error("Erro no processamento: " . $e->getMessage());
        echo json_encode(['error' => 'Erro no processamento: ' . $e->getMessage()]);
    } finally {
        // Remove arquivo temporário
        if (file_exists($temp_path)) {
            unlink($temp_path);
        }
    }
} else {
    echo json_encode(['error' => 'Método não permitido']);
}
?>
