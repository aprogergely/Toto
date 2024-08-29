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
let y = canvas.height - 40;
let dx = 3;
let dy = -3;
let paddleHeight = 10;
let paddleWidth = 100;
let paddleX = (canvas.width - paddleWidth) / 2;
let rightPressed = false;
let leftPressed = false;
let initialBricksState;
let initialNPCState;

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
let initBrickCount = 0;
let npcs = [];
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
            bricks[c][r] = { x: 0, y: 0, status: 0 };  // Initialize as empty
        }
    }

    // Place bricks directly below each NPC
    npcs.forEach(npc => {
        if (npc.row + 1 < brickRowCount) {
            bricks[npc.col][npc.row + 1] = { x: 0, y: 0, status: 3 };  // Strongest brick
            initBrickCount++;
        }
    });

    // Now place random bricks in other positions, without overwriting bricks below NPCs
    for(let c = 0; c < brickColumnCount; c++) {
        for(let r = 0; r < brickRowCount; r++) {
            // Skip the positions already occupied by NPCs or directly below them
            if (bricks[c][r].status === 0) {
                let isPresent = Math.random() > 0.3;  // 70% chance the brick is present
                if (isPresent) {
                    let brickType = Math.floor(Math.random() * 3) + 1;
                    bricks[c][r] = { x: 0, y: 0, status: brickType };
                    initBrickCount++;
                }
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
function saveInitialStates() {
    initialBricksState = JSON.parse(JSON.stringify(bricks));
    initialNPCState = JSON.parse(JSON.stringify(npcs));
}

function initNPCs() {
    npcs = [];
    let npcCount = Math.floor(Math.random() * 4) + 2; // Randomly select 2 to 5 NPCs
    let npcPositions = [];

    // Randomly select positions for NPCs
    while (npcPositions.length < npcCount) {
        let col = Math.floor(Math.random() * brickColumnCount);
        let row = Math.floor(Math.random() * (brickRowCount - 1));  // Exclude bottom row

        let position = { col, row };
        if (!npcPositions.some(pos => pos.col === col && pos.row === row)) {
            npcPositions.push(position);
            npcs.push({
                x: col * (brickWidth + brickPadding) + brickOffsetLeft,
                y: row * (brickHeight + brickPadding) + brickOffsetTop,
                direction: 1,
                fallSpeed: 0,
                row: row,
                col: col
            });
        }
    }
}

function moveNPCs() {
    npcs.forEach(npc => {
        npc.x += npc.direction * 2; // NPC speed
        npc.y += npc.fallSpeed
        
        // Change direction if NPC hits the edge of its brick area
        if(npc.x <= npc.col * (brickWidth + brickPadding) + brickOffsetLeft || 
           npc.x >= (npc.col + 1) * (brickWidth + brickPadding) - brickPadding + brickOffsetLeft - brickWidth/2) {
            npc.direction *= -1;
        }
    });
}

function drawNPCs() {
    npcs.forEach(npc => {
        ctx.fillStyle = "#FF0000"; // Placeholder NPC color, replace with an image if needed
        ctx.fillRect(npc.x, npc.y, brickWidth/2, brickHeight); // NPC size same as brick
    });
}

function updateNPCs() {
    npcs.forEach(npc => {
        if(bricks[npc.col][npc.row + 1] && bricks[npc.col][npc.row + 1].status === 0) {
            npc.direction = 0;
            npc.fallSpeed = 2; // NPC falling speed
            if(npc.y >= (npc.row + 1) * (brickHeight + brickPadding) + brickOffsetTop) {
                npc.row += 1; // Move NPC to the next row
                npc.fallSpeed = 0;
            }
        } else {
            npc.fallSpeed = 4;
        }
    });
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
    npcs = JSON.parse(JSON.stringify(initialNPCState));
    x = canvas.width / 2;
    y = canvas.height - 40;
    //dx = 3;
    dy = -dy;
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
                        b.status -= 1;
                    } else {
                        b.status = 0;
                        score++;
                    }
                    updateNPCs(); // Check if any NPCs need to fall
                    if(score == initBrickCount) {
                        alert("YOU WIN, CONGRATS!");
                        document.location.reload();
                    }
                }
            }
        }
    }
}

function handlePaddleCollision() {
    // Calculate the impact position 's'
    let relativeImpact = (x - paddleX) / paddleWidth; // s as a percentage (0 to 1)
    
    // Ensure 's' is between 0 and 1 to avoid any out-of-bound issues
    if(relativeImpact < 0) relativeImpact = 0;
    if(relativeImpact > 1) relativeImpact = 1;
    
    // Calculate the new angle 'ß' based on the impact position
    let beta = (178 * relativeImpact) + 1; // ß in degrees
    
    // Convert angle from degrees to radians for use with sin and cos
    let betaRadians = beta * Math.PI / 180;
    
    // Calculate new dx and dy based on the angle
    let speed = Math.sqrt(dx * dx + dy * dy); // Keep the same speed
    dx = speed * Math.cos(betaRadians);
    dy = -speed * Math.sin(betaRadians); // Negative because it should move upward
}

// Modify the game loop where the ball hits the paddle
function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawBricks();
    drawBall();
    drawPaddle();
    drawNPCs(); // Draw NPCs
    drawScore();
    collisionDetection();
    moveNPCs(); // Move NPCs

    if(x + dx > canvas.width - ballRadius || x + dx < ballRadius) {
        dx = -dx;
    }
    if(y + dy < ballRadius) {
        dy = -dy;
    } else if(y + dy > canvas.height - ballRadius) {
        if(x > paddleX && x < paddleX + paddleWidth) {
            handlePaddleCollision(); // Update ball's angle after hitting the paddle
        } else {
            alert("GAME OVER");
            resetGame();
        }
    }

    if(rightPressed && paddleX < canvas.width - paddleWidth) {
        paddleX += 7;
    } else if(leftPressed && paddleX > 0) {
        paddleX -= 7;
    }

    x += dx;
    y += dy;
    requestAnimationFrame(draw);
}


initNPCs();
initBricks();
saveInitialStates();
draw();
