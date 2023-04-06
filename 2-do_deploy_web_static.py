#!/usr/bin/python3
"""
generates a .tgz archive from the contents of the web_static
"""

from fabric.api import *
from datetime import datetime
from os import path

env.hosts = ['35.153.83.180', '18.209.223.169']
env.user = 'ubuntu'
env.key_filename = ['school', '/school', '~/.ssh/school']


def do_pack():
    """
    save a compressed version of web_static
    """
    date = datetime.now()
    date_string = date.strftime('%Y%m%d%H%M%S')
    output = "web_static_{}.tgz".format(date_string)
    local('mkdir -p versions')
    stat = local('tar -cvzf versions/{} web_static'.format(output))
    if stat.succeeded:
        return 'versions/{}'.format(output)
    else:
        return None


def do_deploy(archive_path):
    """
    deploy compressed version of web_static
    """
    basename = path.basename(archive_path)
    filename = basename.split('.')[0]
    if local("file ./{}".format(archive_path)).failed:
        return False
    print("./{}".format(archive_path))
    print( "/tmp/{}".format(basename))
    if put("./{}".format(archive_path), "/tmp/{}".format(basename)).failed:
        return False
    if run("mkdir -p /data/web_static/releases/{}".format(filename)).failed:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}"
           .format(basename, filename)).failed:
        return False
    if run("rm -rf /tmp/{}".format(basename)).failed:
        return False
    if run("rm -rf /data/web_static/current").failed:
        return False
    if run("ln -s /data/web_static/releases/{} /data/web_static/current"
           .format(filename)).failed:
        return False
