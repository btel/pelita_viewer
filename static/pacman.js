ws = new MozWebSocket("ws://"+ document.location.hostname +":8888/socket");

ws.onopen = function() {
};

ws.onmessage = function(event) {
data = $.parseJSON(event.data)
redraw(data)
};

ws.onerror = function(event) {
return $('body').append('<div>Error:' + event + ' ' + '</div>');
};

ws.onclose = function(event) {
return $('body').append('<div>Close:' + event.reason + '</div>');
};

function P(x,y) {
    var obj = {};
    obj.x = x
    obj.y = y
    return obj
        
}

var maze_walls = [[P(0  , 0  ),   P(250, 0  )], 
            [P(250, 0  ),   P(250, 250)],
            [P(250, 250),   P(0  , 250)],
            [P(0  , 250),   P(0  , 0  )]]

function dx(d) {return d.x;}
function dy(d) {return d.y;}

var w = 250;
var h = 250;
var margin = 10;
var blksz = 10;
var interval = 80;

var vis = d3.select("#chart")
.append("svg:svg")
.attr('width', w+2*margin)
.attr('height', h+2*margin)
 .append("svg:g")
 .attr("transform", "translate(" + margin + "," + margin + ")");
                

function translate(d) {
    return 'translate(' + d.x*blksz + "," + d.y*blksz + ")";
}


function redraw(data) {
    var pac_pos = data.pacman;
    var food_pos = data.food;
    var ghost_pos = data.ghost;
    var maze_pos = data.maze;

var maze = vis.selectAll("rect")
            .data(maze_pos)
            .enter()
            .append("svg:rect")
            .attr("class", "wall")
            .attr("width", blksz)
            .attr("height", blksz)
            .attr("x", function(d) {return blksz*(d.x-0.5);})
            .attr("y", function(d) {return blksz*(d.y-0.5);})

var pacman = vis.selectAll('g.pacman')
    .data(pac_pos)

    console.log(pac_pos)
    pacman.enter()
      .append('svg:g')
      .attr('transform', translate)
      .attr('class', function (d) {return 'pacman ' + d['team'];})
      .append('svg:path')
      .attr('d', "M-5 -5 L5 -5 L0 5 Z")

      pacman.transition()
      .duration(interval)
      .attr('transform', translate )

var food = vis.selectAll('#food')
              .data(food_pos, function (d) {return d.x*w+d.y;})
    food.enter()
        .append('svg:circle')
        .attr('cx', function (d) {return d.x*blksz;})
        .attr('cy', function (d) {return d.y*blksz;})
        .attr('r', 3)
        .attr('id', 'food')

    food.exit().remove()

var ghost = vis.selectAll('#ghost')
              .data(ghost_pos)

ghost.enter()
     .append('svg:g')
     .attr('transform', translate)
     .attr('id', 'ghost')
     .append('svg:rect')
     .attr('width', blksz*0.8)
     .attr('height', blksz*0.8)

ghost.transition()
      .duration(interval)
      .attr('transform', translate )
    }

function random_move(pos)
{
    if (Math.random()>0.5)
    {
        pos.x += Math.round(Math.random()*20-10)
    }
    else
    {
        pos.y += Math.round(Math.random()*20-10)
    }
}
function move_pacman() {
    random_move(pac_pos)
    for (i=0; i<ghost_pos.length; i+=1) {
        random_move(ghost_pos[i])
    }
    redraw()
}

//setInterval(move_pacman, 1000);
