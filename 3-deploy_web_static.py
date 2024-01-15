#!/usr/bin/python3
""" a Fabric script that creates and distributes an archive to my web servers,
    using the function deploy"""


from fabric.api import local, put, run, env
import os
from datetime import datetime

env.hosts = ['ubuntu@100.25.151.250', 'ubuntu@35.174.211.176']
env.sudo_user = "root"
env.sudo_password = "12345sw48o"
flag = False
file = ""


def do_pack():
    """ A function that generates .tgz file using Fabric """
    # local("mkdir -p ")
    # local("tar -czvf ")
    time_now = datetime.now().strftime("%Y%m%d%H%M%S")
    archived_name = "web_static_" + time_now + ".tgz"
    dir_save = "versions/" + archived_name

    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    print("Packing web_static to {}".format(dir_save))
    result = local("tar czvf {} web_static".format(dir_save))

    if result.failed:
        return None
    else:
        print("web_static packed: {} -> {}Bytes".format(
            dir_save, os.path.getsize(dir_save)))
        return dir_save


def do_deploy(archive_path):
    """ the function that will run remotly ont the servers
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


def deploy():
    """" create the archive file from web_static by calling do_pack
            deployto to the remote servers using do_deploy"""

    global flag
    global file
    if not flag:
        file = do_pack()
        flag = True
    if file is None:
        return False
    return do_deploy(file)
