#!/usr/bin/python3
""" a Fabric script that generates a .tgz archive from the contents
    of the web_static folder of your AirBnB Clone repo,
    using the function do_pack"""

from fabric.api import local
import os
from datetime import datetime


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
