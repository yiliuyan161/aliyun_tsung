# -*- coding:utf-8 -*-

from  xml.dom import  minidom
import re


def get_nodevalue(node, index = 0):
    return node.childNodes[index].nodeValue if node else ''

def get_xmlnode(node,name):
    return node.getElementsByTagName(name) if node else []


def get_xml_data(filename='aliyun1.xml'):
    doc = minidom.parse(filename)
    root = doc.documentElement

    user_nodes = get_xmlnode(root,'SMS')
    user_list=[]
    for node in user_nodes:

        node_body = get_xmlnode(node,'Body')

        user_body_str =get_nodevalue(node_body[0]).encode('utf-8','ignore')

        user_list.append(user_body_str)
    return user_list



def test_laod_xml():
    user_list = get_xml_data()
    hostsFile=open("host.txt","w")
    for user in user_list :

        # <![CDATA[尊敬的用户，您的云服务器创建成功，公网IP：115.28.44.179，内网IP：10.144.49.144，初始登陆密码为fb752950。若您需要进行登陆，Linux操作系统的登陆用户名是root，Windows操作系统的登陆用户名是administrator。对云服务器相关详细信息查看及管理操作请登陆阿里云网站“用户中心”中“管理控制台”的“云服务器”。【阿里云计算】]]>
        m = re.match(r".+公网IP：(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})，内网IP：(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})，初始登陆密码为([a-z|0-9]{8}).+", user)
        if m:
            str="hosts.append(NodeInfo('AY130523110327750b02Z','"+m.group(1)+"','"+m.group(2)+"','root','"+m.group(3)+"'))\n";
            hostsFile.write(str)
        else:
            print 'not match'

    hostsFile.close()

if __name__ == "__main__":

    test_laod_xml()