import os
from topo import topo


def add_link_R2R(node1, node2):
    # 路由器之间的链路添加
    if node1 > node2:
        p1 = "R{}-R{}".format(node1,node2)
        p2 = "R{}-R{}".format(node2,node1)
        command = "sudo ip link add {} type veth peer name {};".format(p1, p2)
        command += "sudo ip link set dev {} name {} netns $(sudo docker inspect -f '{{{{.State.Pid}}}}' R{});".format(p1, p1, node1)
        command += "sudo ip link set dev {} name {} netns $(sudo docker inspect -f '{{{{.State.Pid}}}}' R{});".format(p2, p2, node2)
        command += "sudo docker exec -it R{} ifconfig {} 117.0.{}.{} netmask 255.255.255.0 up;".format(node1, p1, node1+node2, node1)
        command += "sudo docker exec -it R{} ifconfig {} 117.0.{}.{} netmask 255.255.255.0 up;".format(node2, p2, node1+node2, node2)
        os.system(command)


def add_link_R2H(node1, node2):
    # 路由器之间的链路添加，node1为路由器，node2为host
    p1 = "R{}-h{}".format(node1,node2)
    p2 = "h{}-R{}".format(node2,node1)
    command = "sudo ip link add {} type veth peer name {};".format(p1, p2)
    command += "sudo ip link set dev {} name {} netns $(sudo docker inspect -f '{{{{.State.Pid}}}}' R{});".format(p1, p1, node1)
    command += "sudo ip link set dev {} name {} netns $(sudo docker inspect -f '{{{{.State.Pid}}}}' h{});".format(p2, p2, node2)
    command += "sudo docker exec -it R{} ifconfig {} 154.0.{}.1 netmask 255.255.255.0 up;".format(node1, p1, node1)
    command += "sudo docker exec -it h{} ifconfig {} 154.0.{}.2 netmask 255.255.255.0 up;".format(node2, p2, node2)
    command += "sudo docker exec -it h{} route add default gw 154.0.{}.1 {};".format(node2, node1, p2)  # PC默认路由
    os.system(command)

def add_links(tp: topo):
    # 连接所有的链路
    for rt in tp.tp:
        for rt_adj in tp.tp[rt]:
            add_link_R2R(rt, rt_adj)
    for host_no in tp.host:
        add_link_R2H(host_no, host_no)

def gen_config_rt(node, filename, tp: topo):
    # 生成路由器配置命令脚本
    with open(filename, "w+") as file:
        command = "zebra -d;"       # Zebra是守护进程，用来更新内核的路由表    
        if node in tp.rip_list:     # 是否需要开启rip
            command += "ripd -d;"
        if node in tp.ospf_list:    # 是否需要开启ospf
            command += "ospfd -d;"

        file.write("import telnetlib, os\n\n\n")
        file.write("os.system(\"{}\")\n".format(command))   # 开启rip进程或者ospf进程


        if node in tp.rip_list:     
            file.write("tn = telnetlib.Telnet(host=\"127.0.0.1\", port=2602)\n")    # 使用telnet连接到路由器,2602为rip的进程

            file.write("tn.read_until(\": \".encode('ascii'))\n")
            file.write("tn.write(\"zebra\\n\".encode('ascii'))\n")                  # telnet密码输入

            file.write("tn.read_until(\"> \".encode('ascii'))\n")
            file.write("tn.write(\"en\\n\".encode('ascii'))\n")                     # 进入特权模式

            file.write("tn.read_until(\"# \".encode('ascii'))\n")
            file.write("tn.write(\"config t\\n\".encode('ascii'))\n")               # 进入配置模式

            file.write("tn.read_until(\"# \".encode('ascii'))\n")
            file.write("tn.write(\"router rip\\n\".encode('ascii'))\n")             # 进入rip

            for node_adj in tp.tp[node]:
                file.write("tn.read_until(\"# \".encode('ascii'))\n")
                file.write("tn.write(\"network 117.0.{}.0/24\\n\".encode('ascii'))\n".format(node+node_adj))    # 通告路由器之间的网络
            if node in tp.host:
                file.write("tn.read_until(\"# \".encode('ascii'))\n")
                file.write("tn.write(\"network 154.0.{}.0/24\\n\".encode('ascii'))\n".format(node))           # 通告路由器和主机之间的网络
            if node in tp.re_rt_list:   
                file.write("tn.read_until(\"# \".encode('ascii'))\n")
                file.write("tn.write(\"redistribute ospf metric 1\\n\".encode('ascii'))\n")                     # 在RIP中进行ospf的路由重分发
            
            file.write("tn.read_until(\"# \".encode('ascii'))\n")
            file.write("tn.write(\"end\\n\".encode('ascii'))\n")                    # 退到特权模式

            file.write("tn.read_until(\"# \".encode('ascii'))\n")
            file.write("tn.write(\"copy running-config startup-config\\n\".encode('ascii'))\n")                 # 保存配置

            file.write("tn.close()\n")         # 关闭telnet

        if node in tp.ospf_list: 
            file.write("tn = telnetlib.Telnet(host=\"127.0.0.1\", port=2604)\n")    # 使用telnet连接到路由器,2602为rip的进程

            file.write("tn.read_until(\": \".encode('ascii'))\n")
            file.write("tn.write(\"zebra\\n\".encode('ascii'))\n")                  # telnet密码输入

            file.write("tn.read_until(\"> \".encode('ascii'))\n")
            file.write("tn.write(\"en\\n\".encode('ascii'))\n")                     # 进入特权模式

            file.write("tn.read_until(\"# \".encode('ascii'))\n")
            file.write("tn.write(\"config t\\n\".encode('ascii'))\n")               # 进入配置模式

            file.write("tn.read_until(\"# \".encode('ascii'))\n")
            file.write("tn.write(\"router rip\\n\".encode('ascii'))\n")             # 进入rip

            file.write("tn.read_until(\"# \".encode('ascii'))\n")
            file.write("tn.write(\"router ospf\\n\".encode('ascii'))\n")            # 进入ospf

            for node_adj in tp.tp[node]:
                file.write("tn.read_until(\"# \".encode('ascii'))\n")
                file.write("tn.write(\"network 117.0.{}.0/24 area 0\\n\".encode('ascii'))\n".format(node+node_adj))     # 通告路由器之间的网络
            if node in tp.host:
                file.write("tn.read_until(\"# \".encode('ascii'))\n")
                file.write("tn.write(\"network 154.0.{}.0/24 area 0\\n\".encode('ascii'))\n".format(node))            # 通告路由器和主机之间的网络
            if node in tp.re_rt_list: 
                file.write("tn.read_until(\"# \".encode('ascii'))\n")
                file.write("tn.write(\"redistribute rip metric 1\\n\".encode('ascii'))\n")                              # 在ospf中进行rip的路由重分发
            
            file.write("tn.read_until(\"# \".encode('ascii'))\n")
            file.write("tn.write(\"end\\n\".encode('ascii'))\n")                    # 退到特权模式

            file.write("tn.read_until(\"# \".encode('ascii'))\n")
            file.write("tn.write(\"copy running-config startup-config\\n\".encode('ascii'))\n")                 # 保存配置

            file.write("tn.close()\n")         # 关闭telnet

    
    os.system("sudo docker cp {f} $(sudo docker ps -aqf\"name=^R{n}$\"):/home\n".format(f=filename, n=node))


if __name__ == '__main__' :
    tp = topo()

    # 创建容器
    for rt_no in range(tp.rt_num):
        os.system("sudo docker create -it --name=R{no} --net=none --privileged -v /etc/localtime:/etc/localtime:ro ruchuer/u20_quagga:latest /bin/bash > /dev/null;\
            sudo docker start R{no} > /dev/null;".format(no=rt_no+1))
    for host_no in tp.host:
        os.system("sudo docker create -it --name=h{no} --net=none --privileged -v /etc/localtime:/etc/localtime:ro ruchuer/u20_quagga:latest /bin/bash > /dev/null;\
            sudo docker start h{no} > /dev/null;".format(no=host_no))

    # 链路添加到对应的容器当中
    add_links(tp)

    # 生存路由器的配置文件，并且复制到对应的docker容器当中
    filePath = os.path.dirname(__file__)    #获取当前路径
    for rt_no in range(tp.rt_num):
        gen_config_rt(rt_no+1, "{}/config/R{}.py".format(filePath, rt_no+1), tp)
    
    # 运行配置文件
    for rt_no in range(tp.rt_num):
        os.system("sudo docker exec -it R{n} python3.6 /home/R{n}.py".format(n=rt_no+1))
