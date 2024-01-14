#!/usr/bin/python3
""" a Fabric script that deletes out-of-date archives
    from local and remote servers """

from fabric.api import run, env, put
import os


env.hosts = ['ubuntu@100.25.151.250', 'ubuntu@35.174.211.176']
env.sudo_user = "root"
env.sudo_password = "12345sw48o"


