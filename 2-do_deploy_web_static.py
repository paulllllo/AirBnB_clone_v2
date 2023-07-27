#!/usr/bin/python3
# Fabric script that distributes an archive to my web servers using do_deploy

from fabric.api import put, env, run
import os.path

env.user = 'ubuntu'
env.hosts = ['3.84.255.71', '54.236.48.24']


def do_deploy(archive_path):
    """Distribute archive to servers"""
    if os.path.exists(archive_path) is False:
        return False

    name = archive_path.split('/')
    n_name = name[1]
    m_name = n_name.split('.')
    new_name = m_name[0]

    upload = "/tmp/" + n_name
    arch_fold = "/data/web_static/releases/" + new_name

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
