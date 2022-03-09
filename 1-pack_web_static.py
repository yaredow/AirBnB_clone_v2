#!/usr/bin/python3
"""Script that generates a .tgz archive"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """Tar archive"""
    try:
        file = "versions/web_static_{}.tgz".format(
                datetime.now().strftime("%Y%m%d%H%M%S"))
        local('mkdir -p versions')
        local('tar -cvzf {} web_static'.format(file))
        return file
    except:
        return None