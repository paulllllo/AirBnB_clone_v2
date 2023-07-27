from fabric.api import *

env.hosts = ['ubuntu@3.84.255.71', 'ubuntu@54.236.48.24']

def copy():
    put('0-setup_web_static.sh', '~/')
