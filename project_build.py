import os


if __name__ == '__main__' :
    # 安装docker
    os.system("curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun")

    # 拉取镜像
    os.system("docker pull ubuntu:18.04")

    # 运行一个容器，用于配置
    os.system("sudo docker create -it --name=R{no} --privileged -v /etc/localtime:/etc/localtime:ro ubuntu:18.04 /bin/bash > /dev/null;\
            sudo docker start R{no} > /dev/null;".format(no=1))

    # 运行配置
    filePath = os.path.dirname(__file__)    #获取当前路径
    filename = filePath + "/config/quagga_install.sh"
    os.system("sudo chmod {f}; sudo docker cp {f} $(sudo docker ps -aqf\"name=^R{n}$\"):/home; sudo docker exec -it R{n} /bin/bash /home/quagga_install.sh"\
        .format(f=filename, n=1))

    # 生成docker镜像
    os.system("sudo docker stop R1; sudo docker export R1 > node.tar; sudo docker import node.tar node; sudo docker rm R1")