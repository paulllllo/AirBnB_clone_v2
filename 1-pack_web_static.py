#!/usr/bin/python3
# Fabric script that generates a .tgz archive from the content of webstatic
# folder of the AirBnB clone repo using do_pack

from fabric.api import local
from datetime import datetime
import os.path

date = datetime.now().strftime("%Y%m%d%H%M%S")
file_path = "versions/web_static_{}.tgz".format(date)


def do_pack():
    """generates .tgz archive from a folder"""
    if os.path.isdir('versions') is False:
        local('mkdir versions')

    local('tar -cvzf ' + file_path + ' web_static')

    if os.path.exists(file_path):
        return file_path
    return None
