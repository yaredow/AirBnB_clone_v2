#!/usr/bin/python3
"""Script that distributes an archive to your web servers"""
from fabric.api import local, run, put, env
from datetime import datetime
from os import path


env.hosts = ['104.196.15.117', '52.200.30.119']
env.user = 'ubuntu'


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


def do_deploy(archive_path):
    """Deploy"""
    if not path.exists(archive_path):
        return False
    try:
        file = archive_path.split("/")[-1]
        dir = "/data/web_static/releases/" + file.split(".")[0]
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(dir))
        run("sudo tar -xzf /tmp/{} -C {}".format(file, dir))
        run("sudo rm /tmp/{}".format(file))
        run("sudo mv {}/web_static/* {}/".format(dir, dir))
        run("sudo rm -rf {}/web_static".format(dir))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -sf {} /data/web_static/current".format(dir))
        print("New version deployed!")
        return True
    except:
        return False


def deploy():
    """Pack and Deploy all"""
    try:
        tar = do_pack()
        return do_deploy(tar)
    except:
        return False