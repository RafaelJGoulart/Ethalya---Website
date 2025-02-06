<!DOCTYPE html>
<html lang="pt-br">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Página Principal - Ethalya</title>
    <link rel="shortcut icon" href="assets/images/sparkle.png" type="image/x-icon">
    <link rel="stylesheet" href="css/home.css">
    <link rel="stylesheet" href="css/animation.css">
</head>

<body>
    <header>
        <img src="assets/images/ethalya_livro_branco.svg" alt="" class="ethalya_logo">
        <h1>Bem vindo a lista de capítulos.</h1>
        <p>Aqui esta a lista de todos os capítulos finalizados em ordem!</p>
        <p>Acompanhe as aventuras de Farah e seus amigos.</p>
    </header>

    <main>
        <h2>Capítulos Disponíveis</h2>
        <ul>
            <?php
            // Caminho para o diretório onde os capítulos PHP estão armazenados
            $charptersDir = 'charpters';

            // Verificar se o diretório existe
            if (is_dir($charptersDir)) {
                // Obter a lista de arquivos HTML
                $files = glob($charptersDir . '/*.php');

                // Verificar se há capítulos
                if (count($files) > 0) {
                    foreach ($files as $file) {
                        $fileName = basename($file, '.php'); // Nome do capítulo sem extensão
                        $glowing = 'glowing';
                        $capClass = 'cap';
                        echo "<a href='$file' class='$capClass'><li class='$glowing'>$fileName</li></a>";
                    }
                } else {
                    echo "<li>Nenhum capítulo disponível no momento.</li>";
                }
            } else {
                echo "<li>O diretório de capítulos não foi encontrado.</li>";
            }
            ?>
        </ul>
    </main>

    <footer>
        <div class="footer-container">
            <a href="https://instagram.com" target="_blank">
                <img src="assets/images/instagram.svg" alt="Instagram">
            </a>
            <a href="https://github.com" target="_blank">
                <img src="assets/images/github.svg" alt="GitHub">
            </a>
            <a href="https://linkedin.com" target="_blank">
                <img src="assets/images/linkedin.svg" alt="LinkedIn">
            </a>
        </div>
    </footer>
</body>

</html>