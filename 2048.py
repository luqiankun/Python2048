'''
@Author: lqk
@Email: lqkisme@163.com
@Date: 2018-12-05 14:51:48
@LastEditTime: 2018-12-06 12:54:51
@Description: write a 2048 game
'''
import random


class Game(object):
    '''
    游戏类
    '''

    def __init__(self):
        '''
        初始化分数、添加棋子标志位、棋盘、提示和空位存储列表
        '''
        self.scroe = 0
        self.ADD = False  # 是否添加棋子标志位
        self.BoardList = [['', '', '', ''],
                          ['', '', '', ''],
                          ['', '', '', ''], ['', '', '', '']]
        self.Tips = '暂无'
        self.Empty = []  # 存储空位位置（x，y）

    def PrintList(self):
        '''
        打印棋盘
        '''
        print('''
        .—————.—————.—————.—————.
        |{:^5}|{:^5}|{:^5}|{:^5}|
        .—————.—————.—————.—————.
        |{:^5}|{:^5}|{:^5}|{:^5}|
        .—————.—————.—————.—————.
        |{:^5}|{:^5}|{:^5}|{:^5}|
        .—————.—————.—————.—————.
        |{:^5}|{:^5}|{:^5}|{:^5}|
        .—————.—————.—————.—————.
        w(上)，a(左),s(下),d(右)
        r(复位),q(退出)
        分数：{}
        提示：{}
        '''.format(*self.BoardList[0],
                   *self.BoardList[1], *self.BoardList[2], *self.BoardList[3],
                   self.scroe, self.Tips))
        self.Tips = '暂无'

    def AddBoard(self):
        '''
        添加棋子
        '''
        choice = [4, 2, 2, 2, 2, 2, 2, 2]  # 调节随机出现2和4的概率
        t = random.choice(choice)
        if self.Empty:
            p = self.Empty.pop(random.randrange(len(self.Empty)))
            self.BoardList[p[0]][p[1]] = t
        self.ADD = False

    def Input(self):
        '''
        获取按键指令输入，输入后执行操作，判断输赢
        '''
        k = input('请输入指令=>')
        if k == 'w':
            self.Up()
        elif k == 's':
            self.Down()
        elif k == 'a':
            self.Left()
        elif k == 'd':
            self.Right()
        elif k == 'r':
            self.Restart()
        elif k == 'q':
            return True
        else:
            self.Tips = '输入错误'
        if self.JuiceWin():
            print('win!!!')
            return True
        if self.JuiceDefeat():
            print('defeat!!!')
            return True
        if self.ADD:
            self.AddBoard()

    def TranLine(self, line):
        '''
        一行数据的向左操作，例如【2,0,4,4】——》【2,8,0,0】
        思路：【2,0,4,4】——》【2,4,4】——》【2,8】——》【2,8,0，0】
               源列表  ——》  临时列表1 ——》临时列表1——》最终
        '''
        Temp1 = []  # 临时列表1
        Temp2 = []  # 临时列表2
        k = 0  # 源列表最后一个不为0的数据位置
        Flg = True
        for j in line:
            if j:
                Temp1.append(j)
                k = k+1
        # 如果临时列表1不为空，而原列表第一个元素是空或者临时列表1的长度小于源列表最后一个不为0的元素位置，说明发生元素移动
        if Temp1:
            if line[0] == '':
                self.ADD = True
            elif len(Temp1) < k:
                self.ADD = True
        for i in range(len(Temp1)):  # 合并操作
            if Flg:
                if i+1 < len(Temp1) and Temp1[i] == Temp1[i+1]:
                    Temp2.append(Temp1[i]*2)
                    self.scroe = self.scroe+Temp1[i]
                    self.ADD = True
                    Flg = False
                else:
                    Temp2.append(Temp1[i])
                    Flg = True
        for i_3 in range(len(line)-len(Temp2)):  # 补全 0
            Temp2.append('')
        return Temp2

    def Up(self):
        '''
        向上：等价于逆时针90°，执行向左，顺时针复原
        '''
        self.BoardList = self.RotateInv(self.BoardList)
        self.Left()
        self.BoardList = self.Rotate(self.BoardList)

    def Down(self):
        '''
        向下：等价于顺时针90°，执行向左，逆时针复原
        '''
        self.BoardList = self.Rotate(self.BoardList)
        self.Left()
        self.BoardList = self.RotateInv(self.BoardList)

    def Left(self):
        '''
        向左：把每行执行一次向左函数
        '''
        self.ADD = False
        for i in range(len(self.BoardList)):
            self.BoardList[i] = self.TranLine(self.BoardList[i])

    def Right(self):
        '''
        向右：等价于顺时针90°两次，执行向左，逆时针两次复原
        '''
        self.BoardList = self.Rotate(self.BoardList)
        self.BoardList = self.Rotate(self.BoardList)
        self.Left()
        self.BoardList = self.RotateInv(self.BoardList)
        self.BoardList = self.RotateInv(self.BoardList)

    def JuiceWin(self):
        '''
         判断是否赢，列表中出现2048表示胜利，然后刷新空位列表
        '''
        self.Empty = []
        for i in range(len(self.BoardList)):
            for j in range(len(self.BoardList[i])):
                if self.BoardList[i][j] == 2048:
                    return True
                # 如果是空的，添加到空位列表中
                if self.BoardList[i][j] == '':
                    self.Empty.append((i, j))

    def JuiceDefeat(self):
        '''
         列表满了，没有相邻元素相等，则失败，否则返回假
        '''
        if not self.Empty:
            # 每行
            for i in range(len(self.BoardList)):
                for j in range(len(self.BoardList[i])-1):
                    if self.BoardList[i][j] == self.BoardList[i][j+1]:
                        return False
            # 每列
            self.BoardList = self.Rotate(self.BoardList)
            for i in range(len(self.BoardList)):
                for j in range(len(self.BoardList[i])-1):
                    if self.BoardList[i][j] == self.BoardList[i][j+1]:
                        return False
            self.BoardList = self.RotateInv(self.BoardList)
            return True
        return False

    def Rotate(self, mat):
        '''
         顺时针90°旋转二维列表
        '''
        mat[:] = map(list, zip(*mat[::-1]))
        return mat

    def RotateInv(self, mat):
        '''
         逆时针90°旋转二维列表
        '''
        mat[:] = map(list, zip(*mat))
        mat = mat[::-1]
        return mat

    def Restart(self):
        '''
        复位，初始化，随机两个位置添加2或4
        '''
        self.__init__()
        choice = [4, 2, 2]
        while True:
            t1 = (random.randrange(len(self.BoardList)),
                  random.randrange(len(self.BoardList[0])))
            t2 = (random.randrange(len(self.BoardList)),
                  random.randrange(len(self.BoardList[0])))
            if t1 != t2:
                break
        print(t1)
        print(t2)
        self.BoardList[t1[0]][t1[1]] = random.choice(choice)
        self.BoardList[t2[0]][t2[1]] = random.choice(choice)

    def Run(self):
        '''
         运行，先复位后进入循环
        '''
        self.Restart()
        while True:
            self.PrintList()
            if self.Input():
                break


if __name__ == "__main__":
    a = Game()
    a.Run()
