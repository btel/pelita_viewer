#!/usr/bin/python
from pelita.game_master import GameMaster
from pelita.player import BFSPlayer, RandomPlayer, NQRandomPlayer, SimpleTeam
from pelita.viewer import AbstractViewer
import sys

from pacman_viewer import TornadoViewer

from pelita.layout import get_random_layout

if __name__ == '__main__':
    layout = (
        """ ##################
            #0#.  .  # .     #
            #2#####    #####1#
            #     . #  .  .#3#
            ################## """)
    layout = get_random_layout()
    gm = GameMaster(layout, 4, 200)
    gm.register_team(SimpleTeam(BFSPlayer(), NQRandomPlayer()))
    gm.register_team(SimpleTeam(NQRandomPlayer(), BFSPlayer()))
    gm.register_viewer(TornadoViewer())
    gm.play()
