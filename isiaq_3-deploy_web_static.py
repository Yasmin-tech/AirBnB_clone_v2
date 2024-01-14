#!/usr/bin/python3
"""This module contains a Fabric script (based on the file
    1-pack_web_static.py) that distributes an archive to
    your web servers, using the function do_deploy.
    """

from fabric.api import *
import datetime
import os

env.user = "ubuntu"
env.hosts = ['100.25.205.228', '100.25.211.79']
path_to_archive = None


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


def do_deploy(archive_path):
    """uncompress an archive file into a remote server directory
    """
    if not os.path.exists(archive_path):
        return False
    put(archive_path, "/tmp/")
    archive_name = os.path.basename(archive_path)
    arch_filename = os.path.splitext(archive_name)[0]
    arch_path = f'/tmp/{archive_name}'
    run(f'mkdir -p /data/web_static/releases/{arch_filename}')
    cmd = 'tar -xzf {} -C /data/web_static/releases/{} --strip-components=1'
    run(cmd.format(arch_path, arch_filename))
    run(f'rm {arch_path}')
    run('rm /data/web_static/current')
    symb_link = 'ln -s /data/web_static/releases/{} /data/web_static/current'
    cmd = symb_link.format(arch_filename)
    run(cmd)
    print('New version deployed!')
    return True


def deploy():
    """full deployment, i.e, the combination of do_pack and do_deploy
    """
    global path_to_archive
    if path_to_archive is None:
        path_to_archive = do_pack()
        if not path_to_archive:
            return False
    result = do_deploy(path_to_archive)
    return result
