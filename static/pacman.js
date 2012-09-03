channel = new goog.appengine.Channel(token);

ws = channel.open();

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


function dx(d) {return d.x;}
function dy(d) {return d.y;}

var margin = 10;
var blksz = 20;
var interval = 80;

var vis = d3.select("#chart")
.append("svg:svg")
    .attr("id", "maze")
 .append("svg:g")
 .attr("transform", "translate(" + margin + "," + margin + ")");
                

function translate(d) {
    return 'translate(' + d.x*blksz + "," + d.y*blksz + ")";
}

function translate_and_scale(d) {
    return 'translate(' + d.x*blksz + "," + d.y*blksz + ") scale(" + blksz+")";
}


var button = $("#start") 

function redraw(data) {
    var pac_pos = data.pacman;
    var food_pos = data.food;
    var ghost_pos = data.ghost;
    var maze_pos = data.maze;
    var w = data.width;
    var h = data.height;


    if (data.state=="run") button.attr('disabled', "disabled");
    else if (data.state=="stop") button.removeAttr('disabled');

var maze = vis.selectAll("rect.wall")
            .data(maze_pos)
maze.enter()
            .append("svg:rect")
            .attr("class", "wall")
            .attr("width", blksz)
            .attr("height", blksz)
            .attr("x", function(d) {return blksz*(d.x-0.5);})
            .attr("y", function(d) {return blksz*(d.y-0.5);})
maze.exit().remove()

var pacman = vis.selectAll('g.pacman')
.data(pac_pos, function (d) {return "pacman"+d.id;})

    pacman.enter()
      .append('svg:g')
      .attr('transform', translate_and_scale)
      .attr('class', function (d) {return 'pacman ' + d.team;})
      .append('svg:path')
      .attr('d', "M-0.5 -0.5 L0.5 -0.5 L0 0.5 Z")

    pacman.transition()
      .duration(interval)
      .attr('transform', translate_and_scale)

    pacman.exit()
          .remove()

var food = vis.selectAll('#food')
              .data(food_pos, function (d) {return d.x*w+d.y;})
    food.enter()
        .append('svg:circle')
        .attr('cx', function (d) {return d.x*blksz;})
        .attr('cy', function (d) {return d.y*blksz;})
        .attr('r', blksz/4)
        .attr('id', 'food')

    food.exit().remove()

var ghost = vis.selectAll('g.ghost')
               .data(ghost_pos, function (d) {return "ghost"+d.id;})

ghost.enter()
     .append('svg:g')
     .attr('transform', translate)
     .attr('class', function (d) {return 'ghost ' + d.team;} )
     .attr('id', 'ghost')
     .append('svg:rect')
     .attr('width', blksz*0.8)
     .attr('height', blksz*0.8)
     .attr('x', -blksz*0.8/2)
     .attr('y', -blksz*0.8/2)

ghost.transition()
      .duration(interval)
      .attr('transform', translate )

ghost.exit()
    .remove()
    }


