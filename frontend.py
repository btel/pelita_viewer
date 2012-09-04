#!/usr/bin/env python
#coding=utf-8


import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api.channel import create_channel, send_message

import base64
import urllib2

from picloud_conf import *

listeners = []
user_id = 0
game_id = 0
last_msg = '{"ghost": [], "food": [], "pacman": [], "height": [], "width": [], "state": "stop", "maze": []}'

class StartGame(webapp.RequestHandler):
    def post(self):
        global game_id
        game_id+=1
        base64string = base64.encodestring('%s:%s' % (key, secret_key))[:-1]
        http_headers = {'Authorization' : 'Basic %s' % base64string}
        request =urllib2.Request(main_url,
                                 data='url="%s";gameid=%d' % (frontend_url, game_id),
                          headers=http_headers)

        response = urllib2.urlopen(request)
        self.redirect('/game?gameid=%d' % game_id)


class ConnectSocket(webapp.RequestHandler):
    def post(self):
        client_id = self.request.get('from')
        send_message(client_id, last_msg)
        listeners.append(client_id)

class DisconnectSocket(webapp.RequestHandler):
    def post(self):
        client_id = self.request.get('from')
        listeners.remove(client_id)

class GetDataFromPelita(webapp.RequestHandler):
    def post(self):
        msg = self.request.body
        global last_msg
        last_msg = msg
        for client in listeners:
            send_message(client, msg)


class MainPage(webapp.RequestHandler):
    
    def get(self):
        template_path = os.path.dirname(__file__)
        with file(os.path.join(template_path, 'templates/main.html')) as page:
            self.response.out.write(page.read())


class GamePage(webapp.RequestHandler):

    def get(self):
        global user_id
        game_id = int(self.request.get('gameid'))
        socket_token = create_channel(str(user_id))
        user_id+=1
        template_path = os.path.dirname(__file__)
        with file(os.path.join(template_path, 'templates/game.html')) as page:
            self.response.out.write(page.read() % (game_id, socket_token ))



application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/game', GamePage),
                                      ('/_ah/channel/connected/',
                                       ConnectSocket),

                                      ('/_ah/channel/disconnected/',
                                       DisconnectSocket),
                                      ('/data', GetDataFromPelita),
                                      ('/start', StartGame)
                                     ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
