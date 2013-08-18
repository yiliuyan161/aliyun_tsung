aliyun_tsung
============

利用阿里云按小时付费的云主机，快速部署搭建云测试平台。

云主机配置4 核CPU、4GB内存、0G数据盘、5M带宽（追求并发数可以选择不限带宽流量计费）

 一小时费用1.51元一台可以创造65,000左右的连接数，请求数要看带宽和请求体的长度。
 
 有英文资料使用亚马逊的12台云主机相同的测试软件，跑出过每秒过百万的请求数，阿里云应该也可以。
 
 我实际使用10台云主机大概可以创建65万连接。再高连接数受限于阿里云一个账号只能开10台的限制，需要多个账号，部署多个集群。

目前github存放的是集群部署的1.0版本，操作比较繁琐，适合对python有一定了解的人使用

也怪我没有仔细看ECS的api接口，2.0版本会在各个方面有很大的改观


第一步会利用ECS的api制作桌面客户端，大大简化初始化过程

第二步会改进tsung测试过程的易用性，提供web界面，选择测试文件，启动/停止测试，刷新展示测试进度

以下为1.0版本的使用说明，注意事项，请完整阅读。

建议linux环境下运行脚本，windows下需要手动配置环境变量，将%python_home%\Scripts添加到环境变量中，%python_home%是你的python安装路径

requirements：
python 安装 pexpect2.4和fabric1.6.1 高版本应该也没问题（使用setuptools安装，具体参见https://pypi.python.org/pypi/setuptools/0.7.2#installation-instructions）



使用说明：
开通云主机后，主机密码会短信通知，可以用360手机助手导出短信（注意用记事本另存为utf-8，直接导出是gbk的，xml头却写着utf-8，坑爹啊），使用sms_read中的python脚本，提取出来，输出到host.txt了。然后对照阿里云控制台，复制粘贴一下主机名。
之后修改hosts.py
	添加主机列表 NodeInfo（主机名，外网ip，内网ip，用户名，密码）
	hosts.append(NodeInfo('AY13051510503503557fZ','42.96.188.120','10.129.84.235','root','7d6d336f'))
	hosts.append(NodeInfo('AY130515105037225ac8Z','42.96.188.123','10.129.90.188','root','8c32a4d6'))
	hosts.append(NodeInfo('AY1305151050358162e3Z','42.96.188.122','10.129.91.231','root','2fa5abb9'))

然后执行 cluster_init.py 

	会首先 更新copyfiles/hosts文件
	
	然后各主机安装,修改，配置tsung
	
	拷贝配置文件
	
	生成.ssh目录
	
	hosts第一台作为控制节点，生成密钥
	
	下载控制节点的公钥/root/.ssh/id_rsa.pub本地 ，然后上传到其他节点的/root/.ssh/authorized_keys
配置完成

faq：
如果中途有步骤失败了怎么办？
cluster_init目录，再次执行相应的步骤
eg：终端输入命令 fab upload_config_file 重新执行上传配置文件 
fabric会从当前目录查找fabfile.py中查找对应方法名（windows注意配置环境变量，否则可能提示fab找不到）。

注意：
做集群的云主机必须在一个网段，但是阿里云虚拟机创建，不能保证开通的云主机在一个网段（截止到2013/6/14），建议使用青岛主机，杭州会有不在一个网段情况。青岛可能是用的人少的缘故。

各文件功能说明：
cluster_init.py 主文件，执行所有命令

exchange_key.py 生成密钥并分发

fabfile.py 安装配置tsung

generate_hosts.py 更新hosts文件

hosts.py 主机信息


拷贝的文件说明：

copyfiles/tsung-1.4.2        tsung1.4.2 测试jabber有bug，需修改 源码 src/tsung/ts_jabber_common.erl  272行 去掉 version='1.0'

copyfiles/common-session     ulimit相关

copyfiles/hosts              tsung按主机名访问，所有云主机的主机名内部ip映射都要有

copyfiles/limits.conf        ulimit相关 

copyfiles/resolv.conf        更新解决下载地址找不到timeout的问题

copyfiles/sysctl.conf        修改应用端口范围限制 1025-65535

copyfiles/ssh_config         修改ssh默认配置，建立ssh通信之前不检查目标主机是否可信
