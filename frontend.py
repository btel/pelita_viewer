#!/usr/bin/env python
#coding=utf-8


import logging

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api.channel import create_channel, send_message

import base64
import urllib2

from picloud_conf import *

listeners = []
user_id = 0
last_msg = '{"ghost": [], "food": [], "pacman": [], "height": [], "width": [], "state": "stop", "maze": []}'

class StartGame(webapp.RequestHandler):
    def post(self):

        base64string = base64.encodestring('%s:%s' % (key, secret_key))[:-1]
        http_headers = {'Authorization' : 'Basic %s' % base64string}
        request =urllib2.Request(main_url,
                                 data='url="%s"' % frontend_url,
                          headers=http_headers)
        response = urllib2.urlopen(request)


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
        global user_id
        socket_token = create_channel(str(user_id))
        user_id+=1
        self.response.out.write('''
            <html>
                <head>
                <meta content="text/html;charset=utf-8" http-equiv="content-type">
                <script type="text/javascript" src="static/d3/d3.js"></script>
                <script type="text/javascript" src="static/jquery.js"></script>
                <script type="text/javascript" src="/_ah/channel/jsapi"></script>
                <link type="text/css" rel="stylesheet" href="static/pacman.css"/>
                </head>
              <body>
                    Hello Pelita!
                    <form action="start" method="POST">
                    <input type="button" id="start" value="New game"
                                onClick="post()" disabled="disabled" />
                    </form>
                    
                    <div id="chart"></div>
                    <script type="text/javascript">
                                
                       var token = "%s";
                       function post() {
                                $.post('/start')
                                $('#start').attr('disabled', 'disabled')
                               }
                    </script>
                    <script type="text/javascript" src="static/pacman.js"></script>
              </body>
            </html>
                                ''' % socket_token)

application = webapp.WSGIApplication(
                                     [('/', MainPage),
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
