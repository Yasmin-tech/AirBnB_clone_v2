#!/usr/bin/python3
""" This module contains a script that generates a .tgz archive from the
    contents of the web_static folder of your AirBnB Clone repo, using
    the function do_pack
    """

from fabric.api import local
import datetime


def do_pack():
    """ Create a archive from the content of a directory
        and return the path to the archive
    """
    NOW = datetime.datetime.now()
    y = NOW.year
    mon = NOW.month
    d = NOW.day
    hr = NOW.hour
    m = NOW.minute
    sec = NOW.second

    archv_name = 'web_static_{:02d}{:02d}{:02d}{:02d}{:02d}{:02d}.tgz'.format(
            y, mon, d, hr, m, sec)
    local('mkdir -p versions')
    local(f'tar -czvf versions/{archv_name} web_static/')
    return f'versions/{archv_name}'
