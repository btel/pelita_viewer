
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

var food_pos = [P(5, 10), P(100, 50), P(50, 200)]

function dx(d) {return d.x;}
function dy(d) {return d.y;}

var pac_pos = P(10,10)
var ghost_pos = [P(100,100), P(200, 90)]
pac_pos.id = 1;

w = 280
h = 280
margin = 10

var vis = d3.select("#chart")
.append("svg:svg")
.attr('width', w+2*margin)
.attr('height', h+2*margin)
 .append("svg:g")
 .attr("transform", "translate(" + margin + "," + margin + ")");
console.log(vis)

                
var maze = vis.selectAll("line")
            .data(maze_walls)
            .enter()
            .append("svg:line")
            .attr("x1", function(d) {return d[0].x;})
            .attr("x2", function(d) {return d[1].x;})
            .attr("y1", function(d) {return d[0].y;})
            .attr("y2", function(d) {return d[1].y;})
            .style("stroke", "rgb(255,0,0)")
            .style("stroke-width", 2)

function translate(d) {
    return 'translate(' + d.x + "," + d.y + ")";
}

function redraw() {
var pacman = vis.selectAll('#pacman')
    .data([pac_pos])

    console.log(pacman)

    
    pacman.enter()
      .append('svg:g')
      .attr('transform', function (d) {return "translate(" + d.x + "," + d.y + ")";})
      .attr('id', 'pacman')
      .append('svg:path')
      .attr('d', "M0 0 L20 0 L10 15 Z")

      pacman.transition()
      .duration(800)
      .attr('transform', translate )

var food = vis.selectAll('#food')
               .data(food_pos)
    food.enter()
        .append('svg:circle')
        .attr('cx', function (d) {return d.x;})
        .attr('cy', function (d) {return d.y;})
        .attr('r', 3)
        .attr('id', 'food')

var ghost = vis.selectAll('#ghost')
              .data(ghost_pos)

ghost.enter()
     .append('svg:g')
     .attr('transform', translate)
     .attr('id', 'ghost')
     .append('svg:rect')
     .attr('width', 10)
     .attr('height', 10)

ghost.transition()
      .duration(800)
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

setInterval(move_pacman, 1000);
