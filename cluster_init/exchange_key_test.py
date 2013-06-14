import pexpect
from hosts import hosts
from hosts import NodeInfo

def ssh_cmd(hosts):
    master = hosts[0].scpParam();
    user = master[1]
    ip = master[0]
    password = master[2]
    ssh = pexpect.spawn('ssh root@uyhx000049:/root/.ssh/id_rsa.pub  /home/c/masterkey.pub')
    r = ''
    try:
        print('login success')
        # gen-key
        print(ssh.before)
        ssh.expect(['.*'])
        # copy keys
        # scp_key(ssh, hosts[1:])
        ssh.close()
    except pexpect.EOF:
        ssh.close()
    return r
def scp_key(ssh,hosts):
    for host in hosts:
        param=host.innerScpParam()
        print(param[1]+'@'+param[0])
        # ssh.sendline('scp '+'install.log'+param[1]+'@'+param[0]+':'+'/root/tmp')
        ssh.sendline('scp image.conf root@uyhx000050:/root/tmp/')
        print(ssh.after)
        i= ssh.expect(['connecting (yes/no)?','password:','.*'])
        if i==0:
            ssh.sendline('yes')
            ssh.expect('password:')
            ssh.sendline(param[2])
            print('add known host')
        elif i==1:
            ssh.sendline(param[2])
            print('known host')
        elif i==2:
            print('haskey')
        print('cp master key to '+param[0])
    return

if __name__ == '__main__':
    hosts=[]
    hosts.append(NodeInfo('uyhx000049','42.96.188.120','10.129.84.235','root','123!@#qweQWE'))
    hosts.append(NodeInfo('uyhx000050','42.96.188.123','10.129.90.188','root','123!@#qweQWE'))
    # hosts.append(NodeInfo('AY1305151050358162e3Z','42.96.188.122','10.129.91.231','root','2fa5abb9'))
    # hosts.append(NodeInfo('10.144.46.118','115.28.42.115','10.144.46.118','root','fb752950'))
    # hosts.append(NodeInfo('10.144.46.118','115.28.42.115','10.144.46.118','root','fb752950'))
    # hosts.append(NodeInfo('10.144.46.118','115.28.42.115','10.144.46.118','root','fb752950'))
    print ssh_cmd(hosts)

