/**********************************************************************************
*   This code is based on a program I wrote on Khan Academy.
*   It has been modified to work on your own site.
*   You can see the original at http://www.khanacademy.org/cs/network/1058402007
***********************************************************************************/

// Make sure your code includes this line to setup a 400x400 pixel canvas
void setup() {
    size(400, 400); 
}

var numBalls = 8;
var ballSize = 20;
var ballColour = color(60, 80, 140, 120);
var selectedColour = color(100, 100, 200, 255);

// List of links between balls
var springConnections = [[0, 1], [0,2], [0,3], [0,4], [1,5], [1,6], [2,7]];
var springLength = 35;
var springStrength = 0.05;

// Physical variables to play with
var acceleration = 0.05;    // Force of throw
var drag = 0.97;            // Air resistance
var friction = 0.8;         // Wall bounciness
var repulsion = 8;          // Force of replusion between balls

// Find the distance between two balls (must be > 0)
var distance = function(ball1, ball2) {
    var dx = ball1.x - ball2.x;
    var dy = ball1.y - ball2.y;
    var d = max(1, sqrt(dx*dx + dy*dy) - ball1.r - ball2.r);
    return d;
};

// Find the angle between two balls (relative to x-axis)
var angle = function(ball1, ball2) {
    var dx = ball1.x - ball2.x;
    var dy = ball1.y - ball2.y;
    var theta = atan2(dy, dx);
    return theta;
};

// Ball object with a position, speed and colour
var Ball = function(x, y, r, c) {
    this.x = x;
    this.y = y;
    this.r = r;
    this.c = c;
    
    this.dx = 10 * (random() - 0.5);
    this.dy = 10 * (random() - 0.5);
    
    this.draw =function() {
        fill(this.c);
        ellipse(this.x, this.y, this.r*2, this.r*2);
    };
    
    // Move ball based on its velocity
    this.move = function() {
        this.dx *= drag;
        this.dy *= drag;
        this.x += this.dx;
        this.y += this.dy;
    };
    
    // Bounce off walls
    this.bounce = function(){
        if (this.x < this.r) {
            this.x = this.r;
            this.dx *= -friction;
        }
        if (this.x > 400 - this.r){
            this.x = 400 - this.r;
            this.dx *= -friction;
        }
        if (this.y < this.r) {
            this.y = this.r;
            this.dy *= -friction;
        }
        if (this.y > 400 - this.r){
            this.y = 400 - this.r;
            this.dy *= -friction;
        }
    };
    
    // Test whether mouse is over ball
    this.selected = function() {
        if (abs(mouseX - this.x) < this.r && 
            abs(mouseY - this.y) < this.r) {
                return true;
        }
    };
    
    this.collide = function(that) {
        var dx = this.x - that.x;
        var dy = this.y - that.y;
        var dr = this.r + that.r;
        
        if (dx * dx + dy * dy < dr * dr){
            var theta = atan2(dy, dx);
            var force = (sqrt(dr * dr) - sqrt(dx*dx + dy*dy));
            this.dx += force * cos(theta);
            that.dx -= force * cos(theta);
            this.dy += force * sin(theta);
            that.dy -= force * sin(theta);
        }
    };
    
    this.repel = function(that) {
        var d = distance(this, that);
        var theta = angle(this, that);
        var force = repulsion / d;
        
        this.dx += force * cos(theta);
        that.dx -= force * cos(theta);
        this.dy += force * sin(theta);
        that.dy -= force * sin(theta);
    };
    
    this.repelFromSides = function() {
        this.dx += (200 - this.x) / 400;
        this.dy += (200 - this.y) / 400;
    };
};

// A spring between ball1 and ball2 of a given length and strength
var Spring = function(ball1, ball2, length, strength) {
    this.ball1 = ball1;
    this.ball2 = ball2;
    this.length = length;
    this.strength = strength;
    
    this.draw = function() {
        var theta = angle(this.ball1, this.ball2);
        var x1 = this.ball1.x - this.ball1.r * cos(theta);
        var y1 = this.ball1.y - this.ball1.r * sin(theta);
        var x2 = this.ball2.x + this.ball2.r * cos(theta);
        var y2 = this.ball2.y + this.ball2.r * sin(theta);
        line(x1, y1, x2, y2);
    };
    
    this.contract = function() {
        var delta = distance(this.ball1, this.ball2) - this.length;
        var theta = angle(this.ball1, this.ball2);
        var force = delta * strength;
        
        this.ball1.dx -= force * cos(theta);
        this.ball2.dx += force * cos(theta);
        this.ball1.dy -= force * sin(theta);
        this.ball2.dy += force * sin(theta);
    };
};

// Create an array of balls
var balls = [];
for (var i = 0; i < numBalls; i++) {
    var r = ballSize;
    var x = r + round(random() * (400 - 2 * r));
    var y = r + round(random() * (400 - 2 * r));
    var c = ballColour;
    balls.push(new Ball(x, y, r, c));
}

// Create an array of springs between balls
var springs = [];
for (var i = 0; i < springConnections.length; i++){
    var b1 = balls[springConnections[i][0]];
    var b2 = balls[springConnections[i][1]];
    springs.push(new Spring(b1, b2, springLength, springStrength));    
}

strokeWeight(2);
var selected = false;
var i, j;

// Note that this is not the same draw function as normal
void draw() { 
    // Clear everything
    background(255, 255, 255);

    // Draw springs and calculate contraction
    for (i=0; i<springs.length; i++) {
        springs[i].draw();
        springs[i].contract();
    }

    // Draw balls and calculate repulsion
    for (i=0; i<numBalls; i++) {
        balls[i].draw();
        balls[i].repelFromSides();
        for (j=i; j<numBalls; j++){
            balls[i].repel(balls[j]);
        }
    }
    
    // Work out if any ball is dragged
    if (mousePressed) {
        if (!selected) {
            for (i=0; i<numBalls; i++) {
                if (balls[i].selected()) {
                    selected = balls[i];
                    selected.c = selectedColour;
                    break;
                }
            }
        } else {
            // Throw ball
            selected.dx += (mouseX - selected.x) * acceleration;
            selected.dy += (mouseY - selected.y) * acceleration;
        }
    } else { 
        if (selected) {
            selected.c = ballColour;
            selected = false;
        }
    }
    
    // Move balls
    for (i=0; i<numBalls; i++) {
        balls[i].bounce();
        balls[i].move();
    }
};

// Let go when mouse leaves canvas
var mouseOut = function(){
    mousePressed = false;
};