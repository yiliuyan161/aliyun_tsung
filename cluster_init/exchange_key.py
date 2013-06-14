import pexpect
from hosts import hosts
from hosts import NodeInfo

def ssh_cmd(hosts):
    master = hosts[0].scpParam();
    user = master[1]
    ip = master[0]
    password = master[2]
    ssh = pexpect.spawn('ssh %s@%s' % (user, ip))
    r = ''
    try:
        # login
        i = ssh.expect(['password: ', 'continue connecting (yes/no)?'])
        if i == 0:
            ssh.sendline(password)
        elif i == 1:
            ssh.sendline('yes')
            ssh.expect('password:')
            ssh.sendline(password)

        print('login success')

        # gen-key
        ssh.sendline('ssh-keygen -t rsa')
        ssh.expect(['Generating.*:'])
        ssh.sendline()
        j=ssh.expect(['Enter.*:', 'Overwrite (y/n)?'])
        if j==0:
            ssh.sendline()
            ssh.expect('Enter.*:')
            ssh.sendline()
        elif j==1:
            ssh.sendline('y')
            ssh.sendline()
            ssh.expect('Enter.*:')
            ssh.sendline()
            ssh.expect('Enter.*:')
            ssh.sendline()
        print("gen_key success")
        ssh.close()
    except pexpect.EOF:
        ssh.close()
    return r

if __name__ == '__main__':
    print ssh_cmd(hosts)

