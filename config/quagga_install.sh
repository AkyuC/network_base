# 更新apt
apt update
# 安装环境
apt install -y wget net-tools automake autoconf gcc make libtool texinfo gawk libreadline6-dev pkg-config libc-ares2 libc-ares-dev python3.6 telnet inetutils-ping tcpdump traceroute
# 获取Quagga软件源码压缩包
wget https://github.com/Quagga/quagga/releases/download/quagga-1.2.4/quagga-1.2.4.tar.gz
# 解压
tar -xzvf ./quagga-1.2.4.tar.gz
# 进入解压后的文件夹
pushd ./quagga-1.2.4
# 使用automake和autoconf来安装Quagga
# ./configure用于生成Makefile，并且使能vtysh连接路由器脚本，并且设置用户
./configure --enable-vtysh --enable-user=root --enable-group=root --enable-vty-group=root
# 编译
make
# 安装
make install
# 由于是源码安装，还需要进行一些动态链接库文件复制到root用户下的lib
cp ./lib/.libs/libzebra.so.1 /lib
cp ./ospfd/.libs/libospf.so.0 /lib
# 将默认配置复制到运行的文件夹下
cp ./ospfd/ospfd.conf.sample /usr/local/etc/ospfd.conf
cp ./ripd/ripd.conf.sample /usr/local/etc/ripd.conf
cp ./zebra/zebra.conf.sample /usr/local/etc/zebra.conf