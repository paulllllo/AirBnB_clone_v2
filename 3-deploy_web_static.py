#!/usr/bin/python3
# Fabric script that does the full deployment to both servers using deploy()

from fabric.api import local, put, env, run
from datetime import datetime
import os.path

env.user = 'ubuntu'
env.hosts = ['3.84.255.71', '54.236.48.24']

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


def do_deploy(archive_path):
    """Distribute archive to servers"""
    if os.path.exists(archive_path) is False:
        return False

    name = archive_path.split('/')
    n_name = name[1]
    m_name = n_name.split('.')
    new_name = m_name[0]

    upload = "/tmp/" + n_name
    arch_fold = "/data/web_static/release/" + new_name

    put(archive_path, upload)

    run('mkdir -p ' + arch_fold)
    run('tar -xzf /tmp/{} -C {}/'.format(n_name, arch_fold))
    run('rm {}'.format(upload))

    move = 'mv ' + arch_fold + '/web_static/* ' + arch_fold + '/'
    run(move)

    run('rm -fr ' + arch_fold + '/web_static')
    run('rm -fr /data/web_static/current')
    run('ln -s ' + arch_fold + ' /data/web_static/current')
    return True


def deploy():
    """Does the full deploy by calling the above functions"""
    path = do_pack()
    if path is None:
        return False

    deploy = do_deploy(path)
    if deploy is False:
        return False

    return deploy
