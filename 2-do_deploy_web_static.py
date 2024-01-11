#!/usr/bin/python3
"""This module contains a Fabric script (based on the file
    1-pack_web_static.py) that distributes an archive to
    your web servers, using the function do_deploy.
    """

from fabric.api import *
import os

env.user = "ubuntu"
env.hosts = ['100.25.205.228', '100.25.211.79']


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
    cmd = 'tar -xzvf {} -C /data/web_static/releases/{} --strip-components=1'
    run(cmd.format(arch_path, arch_filename))
    run(f'rm {arch_path}')
    run('rm /data/web_static/current')
    symb_link = 'ln -s /data/web_static/releases/{} /data/web_static/current'
    cmd = symb_link.format(arch_filename)
    run(cmd)
    return True
