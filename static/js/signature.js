const canvas = document.getElementById('signature-canvas');
const ctx = canvas.getContext('2d');
let drawing = false;

// Fonction pour démarrer le dessin
function startDrawing(e) {
    drawing = true;
    const { offsetX, offsetY } = getPosition(e);
    ctx.beginPath();
    ctx.moveTo(offsetX, offsetY);
}

// Fonction pour dessiner
function draw(e) {
    if (!drawing) return;
    const { offsetX, offsetY } = getPosition(e);
    ctx.lineTo(offsetX, offsetY);
    ctx.stroke();
}

// Fonction pour arrêter le dessin
function stopDrawing() {
    drawing = false;
    ctx.closePath();
}

// Fonction pour obtenir la position en tenant compte des événements
function getPosition(e) {
    if (e.touches) {
        const rect = canvas.getBoundingClientRect();
        return {
            offsetX: e.touches[0].clientX - rect.left,
            offsetY: e.touches[0].clientY - rect.top
        };
    } else {
        return {
            offsetX: e.offsetX,
            offsetY: e.offsetY
        };
    }
}

// Événements pour les appareils non tactiles
canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseup', stopDrawing);

// Événements pour les appareils tactiles
canvas.addEventListener('touchstart', (e) => {
    e.preventDefault(); // Empêche le défilement de la page
    startDrawing(e);
});
canvas.addEventListener('touchmove', (e) => {
    e.preventDefault(); // Empêche le défilement de la page
    draw(e);
});
canvas.addEventListener('touchend', stopDrawing);

// Fonction pour effacer la signature
document.getElementById('clear-signature').addEventListener('click', () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
});

// Fonction pour sauvegarder la signature et soumettre le formulaire
document.querySelector('form').addEventListener('submit', function (e) {
    // Convertir le canevas en image base64
    const dataURL = canvas.toDataURL();
    
    // Mettre à jour l'input caché avec les données de la signature
    document.getElementById('signature-data').value = dataURL;

    // Si vous souhaitez vérifier que la signature est présente avant la soumission
    if (!dataURL) {
        e.preventDefault(); // Empêche la soumission si la signature est vide
        alert("Veuillez signer avant de soumettre le formulaire.");
    }
});
