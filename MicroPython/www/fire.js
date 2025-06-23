const FIRE_WIDTH = 80;
const FIRE_HEIGHT = 60;
const PIXEL_SIZE = 10;
const MAX_INTENSITY = 36;
const T_MIN = 10;
const T_MAX = 50;
const INTENSITY_MIN = 5;
const INTENSITY_MAX = 36;

const palette = [
    [7, 7, 7], [31, 7, 7], [47, 15, 7], [71, 15, 7], [87, 23, 7], [103, 31, 7],
    [119, 31, 7], [143, 39, 7], [159, 47, 7], [175, 63, 7], [191, 71, 7], [199, 71, 7],
    [223, 79, 7], [223, 87, 7], [223, 87, 7], [215, 95, 7], [215, 95, 7], [215, 103, 15],
    [207, 111, 15], [207, 119, 15], [207, 127, 15], [207, 135, 23], [199, 135, 23],
    [199, 143, 23], [199, 151, 31], [191, 159, 31], [191, 159, 31], [191, 167, 39],
    [191, 167, 39], [191, 175, 47], [183, 175, 47], [183, 183, 47], [183, 183, 55],
    [207, 207, 111], [223, 223, 159], [239, 239, 199], [255, 255, 255]
];

let firePixels = [];
let canvas, ctx, imageData;
let currentTempC = 27; // Celsius from /info
let currentTempF = 80.6; // Fahrenheit, converted
let fireSourceIntensity = INTENSITY_MIN;
let isCelsius = true; // Display unit

function start() {
    canvas = document.getElementById('fire');
    ctx = canvas.getContext('2d');
    defineCanvasSize();
    createFireDataStructure();
    createFireSource();
    setInterval(calculateFirePropagation, 50);
    setInterval(updateTemp, 2000);
    canvas.addEventListener('click', toggleUnit);
}

function defineCanvasSize() {
    canvas.width = FIRE_WIDTH * PIXEL_SIZE;
    canvas.height = FIRE_HEIGHT * PIXEL_SIZE;
    imageData = ctx.createImageData(FIRE_WIDTH * PIXEL_SIZE, FIRE_HEIGHT * PIXEL_SIZE);
}

function createFireDataStructure() {
    for (let i = 0; i < FIRE_WIDTH * FIRE_HEIGHT; i++) {
        firePixels[i] = 0;
    }
}

function createFireSource() {
    for (let x = 0; x < FIRE_WIDTH; x++) {
        firePixels[(FIRE_HEIGHT - 1) * FIRE_WIDTH + x] = fireSourceIntensity;
    }
}

function updateTemp() {
    fetch('/info')
        .then(response => response.json())
        .then(data => {
            currentTempC = data.temp;
            currentTempF = currentTempC * 9 / 5 + 32;
            const intensity = INTENSITY_MIN + (currentTempC - T_MIN) / (T_MAX - T_MIN) * (INTENSITY_MAX - INTENSITY_MIN);
            fireSourceIntensity = Math.round(Math.max(INTENSITY_MIN, Math.min(INTENSITY_MAX, intensity)));
            console.log(`Updated temp: ${currentTempC}°C (${currentTempF.toFixed(1)}°F), intensity: ${fireSourceIntensity}`);
        })
        .catch(error => console.error('Error fetching temp:', error));
}

function toggleUnit() {
    isCelsius = !isCelsius;
}

function calculateFirePropagation() {
    createFireSource();
    for (let x = 0; x < FIRE_WIDTH; x++) {
        for (let y = 1; y < FIRE_HEIGHT; y++) {
            const src = y * FIRE_WIDTH + x;
            const decay = Math.floor(Math.random() * 3);
            const wind = Math.floor(Math.random() * 2);
            const newIntensity = firePixels[src] - decay;
            const dstX = x - wind + 1;
            if (dstX >= 0 && dstX < FIRE_WIDTH && newIntensity >= 0) {
                firePixels[(y - 1) * FIRE_WIDTH + dstX] = newIntensity;
            }
        }
    }
    renderFire();
}

function renderFire() {
    // Draw fire pixels
    for (let y = 0; y < FIRE_HEIGHT; y++) {
        for (let x = 0; x < FIRE_WIDTH; x++) {
            const index = y * FIRE_WIDTH + x;
            const intensity = firePixels[index];
            const color = palette[intensity];
            for (let py = 0; py < PIXEL_SIZE; py++) {
                for (let px = 0; px < PIXEL_SIZE; px++) {
                    const imgIndex = ((y * PIXEL_SIZE + py) * FIRE_WIDTH * PIXEL_SIZE + (x * PIXEL_SIZE + px)) * 4;
                    imageData.data[imgIndex] = color[0];
                    imageData.data[imgIndex + 1] = color[1];
                    imageData.data[imgIndex + 2] = color[2];
                    imageData.data[imgIndex + 3] = 255;
                }
            }
        }
    }
    ctx.putImageData(imageData, 0, 0);

    // Draw temperature text
    const temp = isCelsius ? currentTempC : currentTempF.toFixed(0);
    const unit = isCelsius ? 'c' : 'f';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;

    // Black outline
    ctx.font = 'bold 100px Arial';
    ctx.fillStyle = '#000';
    ctx.fillText(temp, centerX + 2, centerY + 2);
    ctx.font = 'bold 50px Arial';
    ctx.fillText(unit, centerX + ctx.measureText(temp).width / 2 + 50, centerY - 30 + 2);

    // White text
    ctx.font = 'bold 100px Arial';
    ctx.fillStyle = '#fff';
    ctx.fillText(temp, centerX, centerY);
    ctx.font = 'bold 50px Arial';
    ctx.fillText(unit, centerX + ctx.measureText(temp).width / 2 + 50, centerY - 30);
}

window.onload = start;