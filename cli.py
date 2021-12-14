import os
from threading import Thread


class cli:
    def __init__(self) -> None:
        # 初始化
        self.is_bulid = False
        self.start()

    def __do_start(self):
        # cli界面线程
        os.system("clear")
        while True:
            try:
                print("\n>-- Available commands:\n"
                    ">-- 1.run topo\n"
                    ">-- 2.ping test, example： 2 1 7 mean h1 ping -c 5 h7\n"
                    ">-- 3.stop all and exit\n"
                    )

                command = input(">-- Input commands: ").strip().split()
                command = list(map(int, command))
                if len(command) == 0:
                    print("请正确输入！\n")
                    continue
                print(">-- loading!")

                if(int(command[0]) == 1):
                    if(self.is_bulid):
                        print(">-- had built!\n")
                    else:
                        os.system("sudo python3 ./topo_build.py")
                        self.is_bulid = True
                        print(">-- built!\n")

                if(int(command[0]) == 2):
                    if(len(command) != 3):
                        print(">-- 请正确输入！\n")
                    else:
                        os.system("sudo docker exec -it h{} ping -c 5 154.0.{}.2".format(int(command[1]), int(command[2])))

                if(int(command[0]) == 3):
                    if(self.is_bulid):
                        os.system("sudo python3 ./topo_distroy.py")
                    break
                
            except KeyboardInterrupt:
                # 键盘输入错误，关闭所有的设备，退出
                print(">-- Error input! Exit！\n")
                break
    
    def start(self):
        # 开启线程
        Thread(target=self.__do_start).start()


if __name__ == '__main__' :
    # cli加载
    user_cli = cli()