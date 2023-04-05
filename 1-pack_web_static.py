#!/usr/bin/python3
"""
generates a .tgz archive from the contents of the web_static
"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """
    save a compressed version of web_static
    """
    date = datetime.now()
    date_string = date.strftime('%Y%m%d%H%M%S')
    output = "web_static_{}.tgz".format(date_string)
    local('mkdir -p versions')
    stat = local('tar -cvzf versions/{} web_static'.format(output))
    if stat.success:
        return 'versions_{}'.format(output)
    else:
        return None
