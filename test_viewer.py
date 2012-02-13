#!/usr/bin/python

import cloud
from pelita.game_master import GameMaster
from pelita.player import BFSPlayer, RandomPlayer, NQRandomPlayer, SimpleTeam
from pelita.viewer import AbstractViewer
import sys

from pacman_viewer import TornadoViewer

from pelita.layout import get_random_layout


def main(url='http://127.0.0.1:8080'):
    layout = (
        """ ##################
            #0#.  .  # .     #
            #2#####    #####1#
            #     . #  .  .#3#
            ################## """)
    #layout = get_random_layout()
    gm = GameMaster(layout, 4, 200)
    gm.register_team(SimpleTeam(BFSPlayer(), NQRandomPlayer()))
    gm.register_team(SimpleTeam(NQRandomPlayer(), BFSPlayer()))
    gm.register_viewer(TornadoViewer(url))
    gm.play()

def set_cloud_rest():
    cloud.setkey(1785, 'cc8dc0f89a677a8aeb45e2d0a4351b765d684f68')
    func_id = cloud.rest.publish(main, "main_func")
    print func_id

if __name__ == "__main__":
    #set_cloud_rest()
    main(url='http://pelitaapp.appspot.com')
