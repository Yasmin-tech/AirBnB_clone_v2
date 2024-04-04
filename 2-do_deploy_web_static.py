#!/usr/bin/python3
""" a Fabric script that distributes an archive
    to my web servers, using the function do_deploy """
from fabric.api import run, env, put
import os


env.hosts = ['ubuntu@54.160.73.119', 'ubuntu@54.234.68.76']
env.sudo_user = "root"
env.sudo_password = "12345sw48o"


def do_deploy(archive_path):
    """ the function that will run remotly on the servers
        to deploy the archived files """
    if os.path.isfile(archive_path) is False:
        return False

    if put(archive_path, remote_path="/tmp/").failed is True:
        return False

    paths = archive_path.split("/")
    # the file without .tgz
    paths = paths[-1].split(".")

    file_to_uncompress = "/tmp/" + paths[0] + ".tgz"
    if run("sudo mkdir -p /data/web_static/releases/{}/".format(
            paths[0])).failed is True:
        return False

    new_dir = "/data/web_static/releases/{}/".format(paths[0])
    if run("sudo tar -xzf {} -C {}".format(
            file_to_uncompress, new_dir)).failed is True:
        return False

    if run("sudo rm {}".format(file_to_uncompress)).failed is True:
        return False

    if run("sudo mv {}web_static/* {}".format(
            new_dir, new_dir)).failed is True:
        return False

    if run("sudo rm -rf {}web_static".format(new_dir)).failed is True:
        return False

    if run("sudo rm -rf /data/web_static/current").failed is True:
        return False

    if run("sudo ln -s {} /data/web_static/current".format(
            new_dir)).failed is True:
        return False

    print("New version deployed!")

    return True
