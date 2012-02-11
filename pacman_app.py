#!/usr/bin/env python
#coding=utf-8
import logging

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api.channel import create_channel, send_message

listeners = []
user_id = 0

class ConnectSocket(webapp.RequestHandler):
    def post(self):
        client_id = self.request.get('from')
        listeners.append(client_id)

class DisconnectSocket(webapp.RequestHandler):
    def post(self):
        client_id = self.request.get('from')
        listeners.remove(client_id)

class GetDataFromPelita(webapp.RequestHandler):
    def post(self):
        data = self.request.body
        for client in listeners:
            send_message(client, data)


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
                    <div id="chart"></div>
                    <script type="text/javascript"> var token = "%s"
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
                                      ('/data', GetDataFromPelita)
                                     ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
