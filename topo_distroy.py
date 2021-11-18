import os


if __name__ == '__main__' :
    os.system("sudo docker stop $(sudo docker ps -a -q) > /dev/null")
    os.system("sudo docker rm $(sudo docker ps -a -q) > /dev/null; echo end!")