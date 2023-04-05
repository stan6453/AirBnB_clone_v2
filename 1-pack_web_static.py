#!/usr/bin/python3
"""
generates a .tgz archive from the contents of the web_static
"""

from fabric.api import local, lcd
from datetime import datetime


def do_pack():
    """
    save a compressed version of web_static
    """
    date = datetime.now()
    date_string = date.strftime('%Y%m%d%H%M%S')
    output = f"web_static_{date_string}.tgz"
    local('mkdir -p versions')
    local(f'tar -cvzf versions/{output} web_static')
