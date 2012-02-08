#!/usr/bin/env python
#coding=utf-8

import tornado.ioloop, tornado.web, tornado.websocket, os.path
import json
import numpy as np
from random import randint, random

maze = """############
          #          #
          #    #     #
          #    #     #
          ############
       """

def maze_coord(maze):
    stripped = "\n".join([line.strip() for line in maze.splitlines()])
    lines = stripped.splitlines()
    height, width = len(lines), len(lines[0])
    
    layout = []
    for i, line in enumerate(lines):
        for j, ch in enumerate(line):
            if ch=='#':
                layout.append({'x':j, 'y':i})

    return layout, width, height 





def get_data(maze):
    layout, width, height = maze_coord(maze)
    d = {}
    ghost_pos = [{'x': randint(0,width),
                  'y': randint(0,height)} for i in xrange(2)]
    pacman_pos = [{'x': randint(0, width), 'y': randint(0, height)} ] 
    food_pos = [{'x': randint(0, width),
                  'y': randint(0, height)} for i in xrange(10)]

    d = {'ghost': ghost_pos,
         'pacman': pacman_pos,
         'food': food_pos,
         'maze': layout,
         'width': width,
         'height': height}

    return d

def random_move(pos,size, width, height):
    if random() > 0.5:
        pos['x'] += (random()-0.5)*size
        pos['x'] = max([min([pos['x'], width]), 0])
    else:
        pos['y'] += (random()-0.5)*size
        pos['y'] = max([min([pos['y'], height]), 0])
    return pos


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("pacman.html")

class ClientSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print "Opened: " + str(self)
        self.positions = get_data(maze)
        self.timer = tornado.ioloop.PeriodicCallback(self.movearound, 1000)
        self.timer.start()
    def on_close(self):
        print "Closed: " + str(self)
        self.timer.stop()
     
    def movearound(self):
        for obj_class in ['ghost', 'pacman']:
            for obj in self.positions[obj_class]:
                random_move(obj, 4, self.positions['width'],
                            self.positions['height'])
        print self.positions['maze']
        self.write_message(json.dumps(self.positions))

    def on_message(self, point):
        pass

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/socket", ClientSocket),
], **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

