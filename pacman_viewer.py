#!/usr/bin/env python
#coding=utf-8

import tornado.ioloop, tornado.web, tornado.websocket, os.path
import json
import numpy as np
from random import randint, random

listeners = []

import urllib2
import json

import sys
sys.path.append('/Users/bartosz/Downloads/pelita')

import pelita.datamodel

wall = pelita.datamodel.Wall 

import time

class TornadoViewer():
    def __init__(self):
        self.maze_pos  = []
        self.ghost_pos = []
        self.food_pos  = []
        self.pacman_pos  = []
        self.width     = 1
        self.height    = 1

    def set_initial(self, universe):
         pass
    
    def observe(self, round_, turn, universe, events):
        self.maze_pos = [{'x':x, 'y':y} for x,y in
                         universe.maze.pos_of(wall)]
        self.pacman_pos = [{'x':x, 'y':y} for x,y in
                         universe.bot_positions]
        self.food_pos = [{'x':x, 'y':y} for x,y in
                         universe.food_list]
        for i in universe.teams[0].bots:
            self.pacman_pos[i].update({'team': 'teamA'})
        for i in universe.teams[1].bots:
            self.pacman_pos[i].update({'team': 'teamB'})
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
    def open(self):
        print "Opened: " + str(self)
        listeners.append(self)
    def on_close(self):
        listeners.remove(self)

    def on_message(self, point):
        pass

class DataHandler(tornado.web.RequestHandler):
    def post(self):
        data = self.request.body
        for l in listeners:
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
