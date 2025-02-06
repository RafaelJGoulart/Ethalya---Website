
// Configurações para ajustar a repetição vertical
const corpo = document.querySelector(".corpo");
const repeater = document.querySelector(".repeater");
const texto = document.querySelector(".texto");

// Altura fixa da imagem de fundo
const imageHeight = 300; // Altura da imagem em pixels

// Obtenha a altura do texto
const textHeight = texto.offsetHeight;

// Calcule o número inteiro de repetições necessárias
const repeatCount = Math.ceil(textHeight / imageHeight);

// Ajuste a altura do repeater para garantir múltiplos inteiros
const totalHeight = repeatCount * imageHeight;

// Ajuste a altura do repeater e da div "corpo"
repeater.style.height = `${totalHeight}px`;
corpo.style.height = `${totalHeight}px`;
