<?php
// Sistema de Upload Simples
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit(0);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['excel_file'])) {
    $file = $_FILES['excel_file'];
    
    // Verifica se é um arquivo Excel
    if ($file['type'] !== 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') {
        echo json_encode(['error' => 'Apenas arquivos .xlsx são permitidos']);
        exit;
    }
    
    // Simula processamento
    $result = [
        'success' => true,
        'message' => 'Arquivo recebido com sucesso',
        'filename' => $file['name'],
        'size' => $file['size'],
        'type' => $file['type'],
        'uploads_successful' => 1,
        'uploads_failed' => 0,
        'images' => [
            [
                'name' => 'Imagem de teste',
                'url' => 'https://ideolog.ia.br/images/products/teste.jpg'
            ]
        ]
    ];
    
    echo json_encode($result);
} else {
    echo json_encode(['error' => 'Método não permitido ou arquivo não enviado']);
}
?>