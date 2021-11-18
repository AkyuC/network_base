apt update 
apt install -y wget net-tools automake autoconf gcc make libtool texinfo gawk libreadline6-dev pkg-config libc-ares2 libc-ares-dev python3.6 telnet inetutils-ping tcpdump traceroute
wget https://github.com/Quagga/quagga/releases/download/quagga-1.2.4/quagga-1.2.4.tar.gz
tar -xzvf ./quagga-1.2.4.tar.gz
pushd ./quagga-1.2.4
./configure --enable-vtysh --enable-user=root --enable-group=root --enable-vty-group=root
make
make install
cp ./lib/.libs/libzebra.so.1 /lib
cp ./ospfd/.libs/libospf.so.0 /lib
cp ./ospfd/ospfd.conf.sample /usr/local/etc/ospfd.conf
cp ./ripd/ripd.conf.sample /usr/local/etc/ripd.conf
cp ./zebra/zebra.conf.sample /usr/local/etc/zebra.conf