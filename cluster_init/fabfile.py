from fabric.api import *
from fabric.context_managers import *
from fabric.operations import *
from hosts import hosts
from hosts import NodeInfo

env.hosts = []
env.user = 'root'
env.passwords = {}
slaveArray=[]


# will be invoked when using fuctions below
def initEnv(hosts):
    for i in range(len(hosts)):
        env.hosts.append(hosts[i].envHost())
        env.passwords.setdefault(hosts[i].envHost(),hosts[i].envPass())
        if i>0:
            slaveArray.append(hosts[i].envHost())
    env.user='root'
    env.roledefs = {'master': [hosts[0].envHost()],'slave':slaveArray}
initEnv(hosts)

@parallel
def init_batch():
    apt_update()
    apt_get_build_essential()
    install_tsung()
    upload_resolve()
    download_tsung()
    unzip_tsung()
    upload_jabber()
    compile_tsung()
    source_install_tsung()
    upload_config_file()
    
	
@parallel
def apt_update():
    run('apt-get update')

@parallel
def apt_get_build_essential():
    run('apt-get -y install build-essential')
    	
@parallel
def install_tsung():
    run('apt-get -y install tsung')

@parallel
def download_tsung():
    run('wget http://tsung.erlang-projects.org/dist/tsung-1.4.2.tar.gz')

@parallel
def upload_resolve():
    put('copyfiles/resolv.conf', '/etc/resolv.conf')

@parallel
def unzip_tsung():
    with cd('/root'):
        run('tar -xvzf tsung-1.4.2.tar.gz')

@parallel
def upload_jabber():
    put('copyfiles/ts_jabber_common.erl', '/root/tsung-1.4.2/src/tsung/ts_jabber_common.erl')

@parallel
def compile_tsung():
    with cd('/root/tsung-1.4.2'):
        run('./configure')

@parallel
def source_install_tsung():
    with cd('/root/tsung-1.4.2'):
        run('make && make install')

@parallel
def create_ssh():
    with cd('/root'):
        run('mkdir .ssh')


@roles('master')
def create_known_hosts():
    with cd('/root/.ssh'):
        run('touch known_hosts')


@roles('master')
def downloadMasterKey():
    get('/root/.ssh/id_rsa.pub','copyfiles/masterkey.pub')


@parallel
@roles('slave')
def distributeKey():
    put('copyfiles/masterkey.pub','/root/.ssh/authorized_keys')

@parallel
def upload_config_file():
    put('copyfiles/common-session', '/etc/pam.d/common-session')
    put('copyfiles/hosts', '/etc/hosts')
    put('copyfiles/sysctl.conf', '/etc/sysctl.conf')
    put('copyfiles/limits.conf', '/etc/security/limits.conf')
    put('copyfiles/ssh_config', '/etc/ssh/ssh_config')	
