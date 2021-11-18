import os


class topo:
    def __init__(self) -> None:
        # 邻接矩阵
        self.tp = {
            1: {2, 3},
            2: {1, 3},
            3: {1, 2, 4},
            4: {3, 5},
            5: {4, 6, 7},
            6: {5, 7},
            7: {5, 6},
        }
        self.host = [1, 2, 6, 7]    # 主机的节点
        self.rt_num = 7 # 路由器个数
        # 运行RIP的路由器
        self.rip_list = [1,2,3,4]
        # 运行ospf的路由器
        self.ospf_list = [4,5,6,7]
        # 路由重分发的路由器
        self.re_rt_list = [4]