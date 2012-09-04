#!/usr/bin/python

import cloud
from pelita.game_master import GameMaster
from pelita.player import BFSPlayer, RandomPlayer, NQRandomPlayer, SimpleTeam
from pelita.viewer import AbstractViewer
import sys
import zipfile

from pacman_viewer import TornadoViewer

from pelita.layout import get_random_layout

from picloud_conf import *

def main(url='http://127.0.0.1:8080', gameid=0):
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
    gm.register_viewer(TornadoViewer(url, int(gameid)))
    gm.play()

def play_with_teams(team_name, url='http://127.0.0.1:8080'):

    sys.path.append('.')
    zip_fname = team_name + '.zip'
    cloud.files.get(zip_fname)
    zip_file = zipfile.ZipFile(zip_fname)
    zip_file.extractall()
    mod = __import__(team_name)
    team = mod.factory()

    name, layout = get_random_layout()
    gm = GameMaster(layout, 4, 200)
    gm.register_team(team)
    gm.register_team(SimpleTeam(NQRandomPlayer(), BFSPlayer()))
    gm.register_viewer(TornadoViewer(url))
    gm.play()

def upload_team(pkg_path):
    """upload team to cloud. pkg_path should be a compressed zip file"""
    cloud.setkey(key, secret_key)
    cloud.files.put(pkg_path)

def set_cloud_rest():
    cloud.setkey(key, secret_key)
    func_id = cloud.rest.publish(main, "main_func")
    print func_id

if __name__ == "__main__":
    try:
        _, mode = sys.argv[:2]
    except ValueError:
        print('Run: python backend.py MODE')
        sys.exit(0)

    if mode == 'local':
        main('http://127.0.0.1:8080', 0)
    elif mode == 'picloud':
        set_cloud_rest()
    elif mode == 'upload':
        upload_team(sys.argv[2])
    else:
        print('Mode is not available')
