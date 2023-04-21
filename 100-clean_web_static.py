#!/usr/bin/python3
"""
generates a .tgz archive from the contents of the web_static
"""

from fabric.api import local, put, run, cd, env
from datetime import datetime
from os import path
from io import StringIO

env.hosts = ['35.153.83.180', '18.209.223.169']


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
    if put("{}".format(archive_path), "/tmp/", use_sudo=True).failed:
        return False
    if run("mkdir -p /data/web_static/releases/{}".format(filename)).failed:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}"
           .format(basename, filename)).failed:
        return False
    if run("rm /tmp/{}".format(basename)).failed:
        return False
    if run(
        "mv /data/web_static/releases/{}/web_static/* \
        /data/web_static/releases/{}/".format(filename, filename)
    ).failed:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static"
           .format(filename)).failed:
        return False
    if run("rm -rf /data/web_static/current").failed:
        return False
    if run("ln -s /data/web_static/releases/{} /data/web_static/current"
           .format(filename)).failed:
        return False


def deploy():
    """creates and distributes an archive to your web servers"""
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)


def do_clean(number=0):
    """ 
    deletes out-of-date archives.
    number is the number of the archives, including the most recent, to keep.
     - If number is 0 or 1, keep only the most recent version of your archive.
     - if number is 2, keep the most recent, and second most recent versions of your archive.
     - etc.
    """
    file_count = 0
    stdout = StringIO()
    with cd("/data/web_static/releases"):
        run("ls -1 | wc -l", stdout=stdout)
        output = stdout.getvalue()
        for index, letter in enumerate(output):
            if letter == ':':
                file_count = number(output[index+2:])

    print("file count:", type(file_count), file_count)

                
