#!/usr/bin/env python
#coding=utf-8

import json

import urllib2

import sys

from pelita.datamodel import Wall

import time

class TornadoViewer():
    def __init__(self, url, gameid):
        self.maze_pos  = []
        self.ghost_pos = []
        self.food_pos  = []
        self.pacman_pos  = []
        self.width     = 0
        self.height    = 0
        self.state = 'stop'
        self.url = url
        self.gameid = gameid
  
        self.team_names=['teamA', 'teamB']

    def set_initial(self, universe):
        #clear interface
        self.send_data()
        self.maze_pos = [{'x':x, 'y':y} for x,y in
                         universe.maze.pos_of(Wall)]
        self.width = universe.maze.width
        self.height = universe.maze.height
        self.state = 'run'
        self.send_data()

    
    def observe(self, universe, game_state):
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

        winning_team_idx = game_state.get("team_wins")
        
        if winning_team_idx is not None:
            self.state = 'stop'
        else:
            self.state = 'run'

        self.send_data()
        time.sleep(0.1)
    
    def send_data(self):
        data = {'gameid' : self.gameid,
                'maze': self.maze_pos,
                'ghost':self.ghost_pos,
                'pacman': self.pacman_pos,
                'food':self.food_pos,
                'width':self.width,
                'height':self.height,
                'state': self.state}
        data_json = json.dumps(data)
        host = self.url+"/data"
        req = urllib2.Request(host, data_json, {'content-type': 'application/json'})
        response_stream = urllib2.urlopen(req)


