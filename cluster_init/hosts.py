#!/usr/bin/python
class NodeInfo:
    def __init__(self,hostName,outIp,innerIp,username,password):
        self.hostName=hostName
        self.outIp=outIp
        self.innerIp=innerIp
        self.username=username
        self.password=password

    def hostsItemStr(self):
        return self.innerIp+" "+self.hostName

    def scpParam(self):
        return [self.outIp,self.username,self.password]

    def innerScpParam(self):
        return [self.hostName,self.username,self.password]
    def known_host(self):
        return [self.hostName,self.innerIp]
    def envHost(self):
        return self.username+'@'+self.outIp+':22'
    def envPass(self):
        return self.password
    def confStrHostName(self):
        return self.hostName 
    def confStrInnerIP(self):
        return self.innerIp




hosts=[]
hosts.append(NodeInfo('AY130521150737091046Z','115.28.36.74','10.144.53.202','root','dc96ba5b'))
hosts.append(NodeInfo('AY130521150737838051Z','115.28.36.78','10.144.53.203','root','86af94f3'))


