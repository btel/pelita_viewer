#!/usr/bin/python

import cloud
from pelita.game_master import GameMaster
from pelita.player import BFSPlayer, RandomPlayer, NQRandomPlayer, SimpleTeam
from pelita.viewer import AbstractViewer
import sys

from pacman_viewer import TornadoViewer

from pelita.layout import get_random_layout

from picloud_conf import *

def main(url='http://127.0.0.1:8080'):
    #layout = (
    #    """ ##################
    #        #0#.  .  # .     #
    #        #2#####    #####1#
    #        #     . #  .  .#3#
    #        ################## """)
    name, layout = get_random_layout()
    gm = GameMaster(layout, 4, 200)
    gm.register_team(SimpleTeam(BFSPlayer(), NQRandomPlayer()))
    gm.register_team(SimpleTeam(NQRandomPlayer(), BFSPlayer()))
    gm.register_viewer(TornadoViewer(url))
    gm.play()

def set_cloud_rest():
    cloud.setkey(key, secret_key)
    func_id = cloud.rest.publish(main, "main_func")
    print func_id

if __name__ == "__main__":
    try:
        _, mode = sys.argv
    except ValueError:
        print('Run: python backend.py MODE')
        sys.exit(0)

    if mode == 'local':
        main(url='http://127.0.0.1:8080')
    elif mode == 'picloud':
        set_cloud_rest()
    else:
        print('Mode can be either local or picloud')
