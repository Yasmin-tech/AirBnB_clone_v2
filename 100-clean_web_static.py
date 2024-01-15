#!/usr/bin/python3
""" a Fabric script that deletes out-of-date archives
    from local and remote servers """

from fabric.api import run, env, put, local
# from fabric import Connection
import os


env.hosts = ['ubuntu@100.25.151.250', 'ubuntu@35.174.211.176']
env.sudo_user = "root"
env.sudo_password = "12345sw48o"
flag = False
archives_to_delete_copy = []
def do_clean(number=0):
    """Delete out-of-date archives.

    Args:
        number (int): The number of archives to keep.

    If number is 0 or 1, keeps only the most recent archive. If
    number is 2, keeps the most and second-most recent archives,
    etc.
    """
    global flag
    global archives_to_delete_copy
    number = 1 if int(number) == 0 else int(number)

    all_archives = sorted(os.listdir("versions"))
    archives_to_delete = []

    for i in range(len(all_archives) - number):
        archives_to_delete.append(all_archives[i])

    for ar in archives_to_delete:
        local("rm versions/{}".format(ar))
    
    if not flag:
        archives_to_delete_copy = archives_to_delete.copy()  # create a copy of the list
    
    dir_server = run('ls /data/web_static/releases')
    dir_server = dir_server.split()
    
    archives_to_delete_in_server = []
    for ar in archives_to_delete_copy:
        ar_in_server = ar.split(".")[0]
        archives_to_delete_in_server.append(ar_in_server)

    print("Archives to delete:", archives_to_delete_in_server)
    print("Directories on server:", dir_server)
    for i in range(len(dir_server)):
        if dir_server[i] in archives_to_delete_in_server:
            run("sudo rm -rf /data/web_static/releases/{}".format(dir_server[i]))
        else:
            continue
    flag = True
