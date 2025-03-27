const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const scoreElement = document.getElementById('score');
const gameOverElement = document.getElementById('gameOver');
const finalScoreElement = document.getElementById('finalScore');

const gridSize = 20;
const tileCount = canvas.width / gridSize;

let snake = [];
let food = {};
let direction = 'right';
let score = 0;
let gameLoop;
let gameSpeed = 100;
let isGameOver = false;

function initGame() {
    // Initialize snake
    snake = [
        { x: 5, y: 5 },
        { x: 4, y: 5 },
        { x: 3, y: 5 }
    ];
    
    // Initialize food
    generateFood();
    
    // Reset score and direction
    score = 0;
    direction = 'right';
    isGameOver = false;
    
    // Update score display
    scoreElement.textContent = `Score: ${score}`;
    
    // Hide game over screen
    gameOverElement.style.display = 'none';
    
    // Start game loop
    if (gameLoop) clearInterval(gameLoop);
    gameLoop = setInterval(gameStep, gameSpeed);
}

function generateFood() {
    food = {
        x: Math.floor(Math.random() * tileCount),
        y: Math.floor(Math.random() * tileCount)
    };
    
    // Make sure food doesn't spawn on snake
    for (let segment of snake) {
        if (segment.x === food.x && segment.y === food.y) {
            generateFood();
            break;
        }
    }
}

function gameStep() {
    if (isGameOver) return;
    
    // Move snake
    const head = { x: snake[0].x, y: snake[0].y };
    
    switch (direction) {
        case 'up': head.y--; break;
        case 'down': head.y++; break;
        case 'left': head.x--; break;
        case 'right': head.x++; break;
    }
    
    // Check for collisions
    if (head.x < 0 || head.x >= tileCount || 
        head.y < 0 || head.y >= tileCount ||
        snake.some(segment => segment.x === head.x && segment.y === head.y)) {
        gameOver();
        return;
    }
    
    snake.unshift(head);
    
    // Check if snake ate food
    if (head.x === food.x && head.y === food.y) {
        score += 10;
        scoreElement.textContent = `Score: ${score}`;
        generateFood();
        
        // Increase speed every 50 points
        if (score % 50 === 0) {
            gameSpeed = Math.max(50, gameSpeed - 10);
            clearInterval(gameLoop);
            gameLoop = setInterval(gameStep, gameSpeed);
        }
    } else {
        snake.pop();
    }
    
    // Draw everything
    draw();
}

function draw() {
    // Clear canvas
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw grid
    ctx.strokeStyle = '#333';
    ctx.lineWidth = 1;
    for (let i = 0; i < tileCount; i++) {
        ctx.beginPath();
        ctx.moveTo(i * gridSize, 0);
        ctx.lineTo(i * gridSize, canvas.height);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(0, i * gridSize);
        ctx.lineTo(canvas.width, i * gridSize);
        ctx.stroke();
    }
    
    // Draw snake
    snake.forEach((segment, index) => {
        ctx.fillStyle = index === 0 ? '#4CAF50' : '#45a049';
        ctx.fillRect(segment.x * gridSize, segment.y * gridSize, gridSize - 2, gridSize - 2);
    });
    
    // Draw food
    ctx.fillStyle = '#ff0000';
    ctx.fillRect(food.x * gridSize, food.y * gridSize, gridSize - 2, gridSize - 2);
}

function gameOver() {
    isGameOver = true;
    clearInterval(gameLoop);
    finalScoreElement.textContent = score;
    gameOverElement.style.display = 'block';
}

function restartGame() {
    initGame();
}

// Handle keyboard input
document.addEventListener('keydown', (event) => {
    switch (event.key) {
        case 'ArrowUp':
            if (direction !== 'down') direction = 'up';
            break;
        case 'ArrowDown':
            if (direction !== 'up') direction = 'down';
            break;
        case 'ArrowLeft':
            if (direction !== 'right') direction = 'left';
            break;
        case 'ArrowRight':
            if (direction !== 'left') direction = 'right';
            break;
    }
});

// Start the game
initGame(); 