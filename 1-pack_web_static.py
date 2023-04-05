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
    stat = local(f'tar -cvzf versions/{output} web_static')
    if stat.success:
        return f'versions_{output}'
    else:
        return None
