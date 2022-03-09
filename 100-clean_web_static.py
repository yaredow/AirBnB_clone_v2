#!/usr/bin/python3
"""Fabric script that deletes out-of-date archives"""
from fabric.api import local, run, env, lcd, cd


env.hosts = ['104.196.15.117', '52.200.30.119']
env.user = 'ubuntu'


def do_clean(number=0):
    """Clean """
    number = int(number)
    number = 2 if number == 0 else number + 1
    with lcd('versions'):
        local('ls -t | tail -n +{} | xargs rm -rf'.format(number))
    with cd('/data/web_static/releases'):
        run('ls -t | tail -n +{} | xargs rm -rf'.format(number))