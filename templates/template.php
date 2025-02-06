<!DOCTYPE html>
<html lang="pt-br">

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{{charpter}} - {{Title}}</title>
  <link rel="shortcut icon" href="../assets/images/sparkle.png" type="image/x-icon">
  <link rel="stylesheet" href="../css/page.css">
  <link rel="stylesheet" href="../css/components.css">
  <link rel="stylesheet" href="../css/animation.css">
</head>

<body>
  <?php include '../components/header.php'; ?>

  <main>
    <div class="folha">
      <div class="topo"></div>
      <div class="corpo">
        <div class="repeater"></div>
        <div class="texto">
          <h1>{{Title}}</h1>
          {{content}}
        </div>
      </div>
      <div class="fundo"></div>
    </div>
  </main>

  <?php include '../components/footer.php'; ?>

  <script src="../js/page.js"></script>
</body>

</html>