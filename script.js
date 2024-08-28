const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// Load Images
const ballImage = new Image();
ballImage.src = 'images/ball.png';

const paddleImage = new Image();
paddleImage.src = 'images/paddle.png';

const brickImage = new Image();
brickImage.src = 'images/brick.png';

// Game Variables
let ballRadius = 10;
let x = canvas.width / 2;
let y = canvas.height - 30;
let dx = 4;
let dy = -4;
let paddleHeight = 10;
let paddleWidth = 100;
let paddleX = (canvas.width - paddleWidth) / 2;
let rightPressed = false;
let leftPressed = false;
let initialBricksState;

const brickRowCount = 6;
const brickColumnCount = 8;
const brickWidth = 80;
const brickHeight = 40;
const brickPadding = 10;
const brickOffsetTop = 30;
const brickOffsetLeft = 30;

const brickImage1 = new Image();
brickImage1.src = 'images/brick_1.png';

const brickImage2 = new Image();
brickImage2.src = 'images/brick_2.png';

const brickImage3 = new Image();
brickImage3.src = 'images/brick_3.png';

let bricks = [];
let score = 0;

// Event Listeners for paddle movement
document.addEventListener("keydown", keyDownHandler, false);
document.addEventListener("keyup", keyUpHandler, false);

function keyDownHandler(e) {
    if(e.key == "Right" || e.key == "ArrowRight") {
        rightPressed = true;
    } else if(e.key == "Left" || e.key == "ArrowLeft") {
        leftPressed = true;
    }
}

function keyUpHandler(e) {
    if(e.key == "Right" || e.key == "ArrowRight") {
        rightPressed = false;
    } else if(e.key == "Left" || e.key == "ArrowLeft") {
        leftPressed = false;
    }
}

// Draw Ball
function drawBall() {
    ctx.drawImage(ballImage, x - ballRadius, y - ballRadius, ballRadius * 2, ballRadius * 2);
}

// Draw Paddle
function drawPaddle() {
    ctx.drawImage(paddleImage, paddleX, canvas.height - paddleHeight, paddleWidth, paddleHeight);
}

function initBricks() {
    for(let c = 0; c < brickColumnCount; c++) {
        bricks[c] = [];
        for(let r = 0; r < brickRowCount; r++) {
            let isPresent = Math.random() > 0.3; // 70% chance the brick is present
            if (isPresent) {
                // Randomly assign a type to the brick (3, 2, or 1)
                let brickType = Math.floor(Math.random() * 3) + 1;
                bricks[c][r] = { x: 0, y: 0, status: brickType };
            } else {
                bricks[c][r] = { x: 0, y: 0, status: 0 }; // No brick
            }
        }
    }
}

function drawBricks() {
    for(let c = 0; c < brickColumnCount; c++) {
        for(let r = 0; r < brickRowCount; r++) {
            let b = bricks[c][r];
            if(b.status > 0) {
                let brickX = (c * (brickWidth + brickPadding)) + brickOffsetLeft;
                let brickY = (r * (brickHeight + brickPadding)) + brickOffsetTop;
                b.x = brickX;
                b.y = brickY;
                
                let brickImage;
                if(b.status === 3) {
                    brickImage = brickImage3;
                } else if(b.status === 2) {
                    brickImage = brickImage2;
                } else if(b.status === 1) {
                    brickImage = brickImage1;
                }

                ctx.drawImage(brickImage, brickX, brickY, brickWidth, brickHeight);
            }
        }
    }
}

// Capture the initial brick layout
function saveInitialBricksState() {
    initialBricksState = JSON.parse(JSON.stringify(bricks));
}

// Draw Score
function drawScore() {
    ctx.font = "16px Arial";
    ctx.fillStyle = "#0095DD";
    ctx.fillText("Score: " + score, 8, 20);
}

// Reset the game state using the saved brick layout
function resetGame() {
    bricks = JSON.parse(JSON.stringify(initialBricksState));
    x = canvas.width / 2;
    y = canvas.height - 30;
    dx = 4;
    dy = -4;
    paddleX = (canvas.width - paddleWidth) / 2;
    score = 0;
}

// Modify the game over logic
function gameOver() {
    alert("GAME OVER");
    resetGame();
    draw();
}

// Collision Detection
function collisionDetection() {
    for(let c = 0; c < brickColumnCount; c++) {
        for(let r = 0; r < brickRowCount; r++) {
            let b = bricks[c][r];
            if(b.status > 0) {
                if(x > b.x && x < b.x + brickWidth && y > b.y && y < b.y + brickHeight) {
                    dy = -dy;
                    if(b.status > 1) {
                        b.status -= 1; // Move to the next lower brick type
                    } else {
                        b.status = 0; // Brick disappears
                    }
                    score++;
                    if(score == brickRowCount * brickColumnCount) {
                        alert("YOU WIN, CONGRATS!");
                        document.location.reload();
                    }
                }
            }
        }
    }
}

// Game Loop
function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawBricks();
    drawBall();
    drawPaddle();
    drawScore();
    collisionDetection();

    // Ball Movement
    if(x + dx > canvas.width - ballRadius || x + dx < ballRadius) {
        dx = -dx;
    }
    if(y + dy < ballRadius) {
        dy = -dy;
    } else if(y + dy > canvas.height - ballRadius) {
        if(x > paddleX && x < paddleX + paddleWidth) {
            dy = -dy;
        } else {
            gameOver()
        }
    }

    // Paddle Movement
    if(rightPressed && paddleX < canvas.width - paddleWidth) {
        paddleX += 7;
    } else if(leftPressed && paddleX > 0) {
        paddleX -= 7;
    }

    x += dx;
    y += dy;
    requestAnimationFrame(draw);
}

initBricks();
saveInitialBricksState();
draw();
