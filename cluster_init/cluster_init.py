import paramiko 
import threading
import os
import time
from hosts import hosts
from hosts import NodeInfo
import generate_hosts_conf
import exchange_key



if __name__ == '__main__':
    generate_hosts_conf.writeHosts('copyfiles/hosts',hosts)
    generate_hosts_conf.writeConf('copyfiles/tsung_conf.xml',hosts)
    print "\n\ninitMaster........................."
    os.system('fab init_batch')
    exchange_key.ssh_cmd(hosts)
    print "\n\ndownload master key........................"
    os.system('fab downloadMasterKey')
    print "\n\ndistribute master key........................"
    os.system('fab distributeKey')
    print "\n\n.................init finished!........................."
