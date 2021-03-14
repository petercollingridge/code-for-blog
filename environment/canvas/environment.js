// Number atoms each section starts with
const ATOMS = 1000;
// Starting energy of water
const WATER_TEMPERATURE = 20;


function getEnvironment(width, height) {
    // Create array of chunks of atoms
    const arr = [];
    const n = width * height;
    for (let i = 0; i < n; i++) {
        arr.push({
            atoms: ATOMS,
            temperature: WATER_TEMPERATURE,

        });
    }
}

function createEnvironment(width, height, size=20) {
    const id = 'environment'
    const container = document.getElementById('environment');
    if (!container) {
        console.error('No element found with id ' + id);
        return;
    }

    const ctx = canvas.getContext('2d');
    const canvas = document.createElement('canvas');
    canvas.setAttribute('width', width);
    canvas.setAttribute('height', height);
    canvas.style.cssText = "border:1px solid #ddd";
    container.appendChild(canvas);

    const environment = getEnvironment(width, height);

    const canvasWidth = size * width;
    const canvasHeight = size * width;

    function draw() {
        ctx.clearRect(0, 0, canvasWidth, canvasHeight);

        let i = 0;
        for (let x = 0; x < width; x++) {
            for (let y = 0; y < height; y++) {
                ctx.beginPath();
                ctx.rect(x * size, y * size, size, size);
                ctx.fill();
                i++;
            }
        }
    }

}
