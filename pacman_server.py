#!/usr/bin/env python
#coding=utf-8

import tornado.ioloop, tornado.web, tornado.websocket, os.path

import sys
import time


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
