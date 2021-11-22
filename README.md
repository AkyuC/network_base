### 环境搭建
    在neteork_base的文件夹下，用命令行运行“sudo python3 ./project_build.py”
    在project_build.py文件当中，会安装docker和~~拉取ubuntu:20.04的镜像~~(上传了docker镜像到docker hub，从docker hub拉取)，如果宿主机已经有这两项了，请注释掉！

### 拓扑设置
    请查看topo.py文件，有基本的设置，最初的拓扑如下(使用packet tracer画的)
![image](https://github.com/ruchuer/network_base/blob/main/topo.png)

    接口和ip的设置查看topo_build.py文件，有关veth-pair的创建等等

### 运行
    在当前目录下，在终端执行“sudo python3 ./cli.py”，显示如下：
![image](https://github.com/ruchuer/network_base/blob/main/cli.png)
