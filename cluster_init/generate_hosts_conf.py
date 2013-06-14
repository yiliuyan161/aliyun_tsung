#!/usr/bin/python
from hosts import NodeInfo
from hosts import hosts
def writeHosts(hostPath, hosts):
        hostsFile=open(hostPath,"w")
        hostsFile.write("127.0.0.1  localhost\n")
        for host in hosts:
            hostsFile.write(host.hostsItemStr()+"\n")
        hostsFile.write('\n')
        ipv6text=["# The following lines are desirable for IPv6 capable hosts\n",
                    "::1     ip6-localhost ip6-loopback\n",
                    "fe00::0 ip6-localnet\n",
                    "ff00::0 ip6-mcastprefix\n",
                    "ff02::1 ip6-allnodes\n",
                    "ff02::2 ip6-allrouters\n"
                    ]
        hostsFile.writelines(ipv6text)
        hostsFile.close()
        print("hosts updates")

def writeConf(confPath, hosts):
    tsungConfFile = open(confPath, "w")
    tsungConfFile.write("<?xml version=\"1.0\"?>\n")
    tsungConfFile.write("<!DOCTYPE tsung SYSTEM '/usr/local/share/tsung/tsung-1.0.dtd'>\n")
    tsungConfFile.write("<tsung loglevel=\"notice\" dumptraffic=\"false\" version=\"1.0\">\n\n\n\n")
    tsungConfFile.write("<clients>\n")
    for host in hosts:
        tsungConfFile.write("<client host=\"")
        tsungConfFile.write(host.confStrHostName())
        tsungConfFile.write("\" maxusers=\"60000\">" + "\n")
        tsungConfFile.write("<ip  value=\"")
        tsungConfFile.write(host.confStrInnerIP())
        tsungConfFile.write("\"/>" + "\n")
        tsungConfFile.write("</client>" + "\n")
    tsungConfFile.write("</clients>\n\n\n\n")

    tsungConfFile.close()
    print "write clients success"


if __name__ == '__main__':
    writeHosts('copyfiles/hosts',hosts)
    writeConf('copyfiles/tsung_conf.xml',hosts)
