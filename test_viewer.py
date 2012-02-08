#!/usr/bin/python
from pelita.game_master import GameMaster
from pelita.player import StoppingPlayer, RandomPlayer, NQRandomPlayer, SimpleTeam
from pelita.viewer import AbstractViewer
import sys
sys.path.append('/Users/bartosz/work/d3-pacman')

import pdb

from pacman_viewer import TornadoViewer

class MyViewer(AbstractViewer):
    def observe(self, round, turn, universe, events):
        print universe.bot_positions
        

if __name__ == '__main__':
    layout = (
        """ ##################
            #0#.  .  # .     #
            #2#####    #####1#
            #     . #  .  .#3#
            ################## """)
    gm = GameMaster(layout, 4, 200)
    gm.register_team(SimpleTeam(StoppingPlayer(), NQRandomPlayer()))
    gm.register_team(SimpleTeam(NQRandomPlayer(), NQRandomPlayer()))
    gm.register_viewer(TornadoViewer())
    gm.play()
