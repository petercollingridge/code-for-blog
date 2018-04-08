var Sugarscape = (function() {
    var SCREEN_WIDTH = window.innerWidth;
    var SCREEN_HEIGHT = window.innerHeight;
    var screenX = window.screenX;
    var screenY = window.screenY;
    var canvas, context;

    var FPS = 10;
    var my_world;
    var grid_width = 50;
    var grid_height = 50;
    var grid_size = 5;
    var agent_size = 3;
    var initial_agents = 200;

    // Add play/pause button
  
    return {
        init: function() {  
            canvas = document.getElementById( 'sugarscape-grid' );

            if (canvas && canvas.getContext) {
                context = canvas.getContext('2d');
                document.getElementById( 'sugar-growback-slider' ).addEventListener('mouseup', sliderHandler, false);
            
                grid_size = Math.floor((canvas.width-10)/grid_width)
                my_world = new World({ width: grid_width, height: grid_height});
            
                my_world.buildGrid();
                my_world.addAgents(initial_agents);
                
                context.strokeStyle = "#000";
                context.lineWidth = "2";
                context.strokeRect(1, 1, grid_width*grid_size+2, grid_height*grid_size+2)
                setInterval( loop, 1000 / FPS );
            };
        },
        loop: function() {
            my_world.update();
            displayWorld();
            // document.getElementById( 'dead-agent-counter' ).innerHTML = my_world.deadAgents.length
            my_world.deadAgents = [];
        },
        displayWorld: function () {
            // Display Grid
            for (var x=0; x < my_world.width; x++) {
                for (var y=0; y < my_world.height; y++) {
                    colour = 255 - my_world.sectors[x][y].sugar * 63;
                    context.fillStyle = "rgb(" +colour+ ", 255, " +colour+ ")";
                    context.fillRect(2 + x * grid_size, 2 + y * grid_size, grid_size, grid_size);
                };
            };
            
            // Display Agents
            context.fillStyle = "#f12";
            for (var n = 0; n < my_world.agents.length; n++) {
                context.beginPath();
                x = 3 + my_world.agents[n].x*grid_size + agent_size;
                y = 3 + my_world.agents[n].y*grid_size + agent_size;
                context.arc(x, y, agent_size, 0, Math.PI*2, true); 
                context.closePath();
                context.fill();
            };
        },
        sliderHandler: function(evt) {
            my_world.regenerate_amount = parseInt(evt.target.value);
        }
    };
})();

function World(size) {
    this.width = size.width;
    this.height = size.height;
    this.sectors = new Array();
    
    this.agents = new Array();
    this.deadAgents = new Array();
    
    //  Simulation Parameters
    this.regenerate_amount = 1;
    this.replace_dead_agents = true;
  
    this.buildGrid = function() {
        var x1 = 13;
        var y1 = 35;
        var x2 = 35;
        var y2 = 15;
        
        for (var x = 0; x < this.width; x++) {
            row = new Array(this.height)
            for (var y = 0; y < this.height; y++) {
                var sugar  = 4 * (40/(Math.pow(distanceBetween(x,y,x1,y1), 1.6) + 40))
                    sugar += 4 * (30/(Math.pow(distanceBetween(x,y,x2,y2), 1.6) + 30))
                row[y] = new Sector(parseInt(sugar));
            }
            this.sectors.push(row)
        }
    }
    
    this.addAgents = function(num_agents) {
        for (var n = 0; n < num_agents; n++) {
            var x, y;
            
            // Find an empty space
            while (true) {
                x = parseInt(Math.random() * this.width);
                y = parseInt(Math.random() * this.height);
                if (!this.sectors[x][y].occupant){break;}
            }

            vision = parseInt(Math.random() * 6) + 1;
            metabolism = parseInt(Math.random() * 4) + 1;
            
            agent = new Agent(this, {x: x, y: y}, {vision: vision, metabolism: metabolism})
            agent.sugar = parseInt(Math.random() * 20) + 5;
            this.agents.push(agent)
            this.sectors[x][y].occupant = agent;
        }
    }
    
    this.update = function() {
        for (var n = 0; n < this.agents.length; n++) {
            this.agents[n].look();
            this.agents[n].eat();
        }
        
        for(var n = 0; n < this.deadAgents.length; n++) {
            var i = this.agents.indexOf(this.deadAgents[n]);
            if (i !== -1) { this.agents.splice(i, 1); }
        }
        
        if (this.replace_dead_agents) { this.addAgents(this.deadAgents.length); }
        //this.deadAgents = [];
        
        for (var x = 0; x < this.width; x++) {
            for (var y = 0; y < this.height; y++) {
                this.sectors[x][y].regenerate(this.regenerate_amount);
            }
        }
    }
    
    // World is a torus, so wrap values that are off the grid
    this.wrapWorld = function(x, y) {
        if (x < 0) { x = this.width + x; }
        else if (x >= this.width) { x = x - this.width; }
        if (y < 0) { y = this.height + y; }
        else if (y >= this.height) { y = y - this.height; }
        return {x: x, y: y};
    }
}

function Sector(sugarMax) {
    this.sugar = 0;
    this.sugarMax = sugarMax;
    this.occupant = false;
    
    this.regenerate = function(amount) {
        this.sugar += amount;
        if (this.sugar > this.sugarMax) {
            this.sugar = this.sugarMax
        }
    }
}

function Agent(world, position, gene) {
    this.world = world;
    this.x = position.x;
    this.y = position.y;
    this.vision = gene.vision;
    this.metabolism = gene.metabolism;
    this.directions = [{x: 1, y: 0}, {x: 0, y: 1}, {x: -1, y: 0}, {x: 0, y: -1}];
    this.sugar = 0;
    
    this.look = function() {
        var max_sugar = this.world.sectors[this.x][this.y].sugar + 1;
        var move_to = false;
        
        this.directions = shuffleArray(this.directions);
        
        for (var d = this.vision; d>0; d--) {
            for (var n = 0; n < 4; n++) {
                var direction = this.directions[n];
                var position = this.world.wrapWorld(this.x + d * direction.x, this.y + d * direction.y);
                
                if (this.world.sectors[position.x][position.y].occupant) {continue;}
                var found_sugar = this.world.sectors[position.x][position.y].sugar;
                
                if (found_sugar >= max_sugar) {
                    max_sugar = found_sugar;
                    move_to = position;
                }
            }
        }
        if (move_to) {this.moveTo(move_to);}
    }
    
    this.eat = function() {
        var sector = this.world.sectors[this.x][this.y];
        collect = sector.sugar;
        sector.sugar -= collect;

        this.sugar += collect-this.metabolism;
        if (this.sugar < 0) { this.world.deadAgents.push(this); }
    }
    
    this.moveTo = function(position) {
        this.world.sectors[this.x][this.y].occupant = false;
        this.x = position.x;
        this.y = position.y;
        this.world.sectors[this.x][this.y].occupant = this;
    }
}

function distanceBetween(x1, y1, x2, y2) {
    var dx = x1 - x2;
    var dy = y1 - y2;
    return Math.sqrt(dx * dx + dy * dy);
}

function shuffleArray(arr) {
    for (var n = arr.length - 1; n > 0; n--) {
        var i = parseInt(Math.random() * n);
        var tmp  = arr[n];
        arr[n] = arr[i];
        arr[i] = tmp;
    }
    return arr;
}

function showRangeValue(newValue) {
	document.getElementById("sugar-growback-rate").innerHTML=newValue;
}

Sugarscape.init();