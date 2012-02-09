#!/usr/bin/env python
#coding=utf-8

import tornado.ioloop, tornado.web, tornado.websocket, os.path
import json
import numpy as np
from random import randint, random


import urllib2
import json

import sys
sys.path.append('/Users/bartosz/Downloads/pelita')

import pelita.datamodel


import time

class TornadoViewer():
    def __init__(self):
        self.maze_pos  = []
        self.ghost_pos = []
        self.food_pos  = []
        self.pacman_pos  = []
        self.width     = 0
        self.height    = 0
  
        self.team_names=['teamA', 'teamB']

    def set_initial(self, universe):
        #clear interface
        self.send_data()
        wall = pelita.datamodel.Wall 
        self.maze_pos = [{'x':x, 'y':y} for x,y in
                         universe.maze.pos_of(wall)]
        self.width = universe.maze.width
        self.height = universe.maze.height
        self.send_data()

    
    def observe(self, round_, turn, universe, events):
        self.food_pos = [{'x':x, 'y':y} for x,y in
                         universe.food_list]
        self.pacman_pos = []
        self.ghost_pos = []

        for bot in universe.bots:
            bot_data = {'x':bot.current_pos[0],
                        'y': bot.current_pos[1],
                        'team': self.team_names[bot.team_index],
                        'id': "bot{0}".format(bot.index)
                       }
            if bot.is_harvester:
                self.pacman_pos.append(bot_data)
            elif bot.is_destroyer:
                self.ghost_pos.append(bot_data)

        self.send_data()
        time.sleep(0.1)
    
    def send_data(self):
        data = {'maze': self.maze_pos,
                'ghost':self.ghost_pos,
                'pacman': self.pacman_pos,
                'food':self.food_pos,
                'width':self.width,
                'height':self.height}
        data_json = json.dumps(data)
        host = "http://127.0.0.1:8888/data"
        req = urllib2.Request(host, data_json, {'content-type': 'application/json'})
        response_stream = urllib2.urlopen(req)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("pacman.html")

class ClientSocket(tornado.websocket.WebSocketHandler):
    listeners = []
    def open(self):
        print "Opened: " + str(self)
        ClientSocket.listeners.append(self)
    def on_close(self):
        ClientSocket.listeners.remove(self)

    def on_message(self, point):
        pass

class DataHandler(tornado.web.RequestHandler):
    def post(self):
        data = self.request.body
        for l in ClientSocket.listeners:
            l.write_message(data)

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/socket", ClientSocket),
    (r"/data", DataHandler),
], **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
