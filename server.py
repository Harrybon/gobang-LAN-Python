# coding=gbk
from tkinter import *
import socket,threading
# 等待连接
#用数组定义一个棋盘，棋盘大小为 15×15
#数组索引代表位置
#元素值代表该位置的状态：-1代表没有棋子，0代表有黑棋，1代表有白棋。
class Server():
    def acceptMessage(self,server, x, y, theSystem):
        sock, addr = server.accept()
        theSystem.sock = sock
        while True:
            x, y = sock.recv(1024).decode("gbk").split(":")
            eventx = int(x)
            eventy = int(y)
            self.callbackServer(eventx, eventy)
    def callback(self,event):
        if self.te:
            data = str(event.x)+":"+str(event.y)
            self.sock.send(data.encode("utf-8"))
            color = ["white", "white"]
            x = round(event.x / self.mesh) - 1
            y = round(event.y / self.mesh) - 1
            errorX = self.mesh * (x + 1) - event.x
            errorY = self.mesh * (y + 1) - event.y
            dis = (errorX ** 2 + errorY ** 2) ** 0.5
            if self.QP[x][y] == -1 and dis < self.K / 2 * self.mesh and self.stop == 0:
                self.a.config(text=self.key[(self.tag + 1) % 2], fg=color[(self.tag + 1) % 2])
                self.QP[x][y] = self.tag
                self.canvas.create_oval(self.mesh * (x + 1) - self.Qr, self.mesh * (y + 1) - self.Qr, self.mesh * (x + 1) + self.Qr, self.mesh * (y + 1) + self.Qr,
                                   fill=color[self.tag])
                v = [[0, 1], [1, 0], [1, 1], [1, -1]]
                for i in v:
                    x1, y1 = x, y
                    while x1 < self.num - 1 and x1 > 0 and y1 > 0 and y1 < self.num - 1:
                        x1 += i[0]
                        y1 += i[1]
                    count = 0
                    while x1 <= self.num - 1 and x1 >= 0 and y1 >= 0 and y1 <= self.num - 1:
                        if self.QP[x1][y1] == self.tag:
                            count += 1
                            if count == 5:
                                self.win()
                        else:
                            count = 0
                        x1 -= i[0]
                        y1 -= i[1]
                self.tag = (self.tag + 1) % 2
                self.tagx, self.tagy = x, y
                self.te = 0
    def callbackServer(self,eventx,eventy):
        #global tag, tagx, tagy, a
        color = ["black", "black"]
        x = round(eventx / self.mesh) - 1
        y = round(eventy / self.mesh) - 1
        errorX = self.mesh * (x + 1) - eventx
        errorY = self.mesh * (y + 1) - eventy
        dis = (errorX ** 2 + errorY ** 2) ** 0.5
        if self.QP[x][y] == -1 and dis < self.K / 2 * self.mesh and self.stop == 0:
            self.a.config(text=self.key[(self.tag + 1) % 2], fg=color[(self.tag + 1) % 2])
            self.QP[x][y] = self.tag
            self.canvas.create_oval(self.mesh * (x + 1) - self.Qr, self.mesh * (y + 1) - self.Qr, self.mesh * (x + 1) + self.Qr, self.mesh * (y + 1) + self.Qr,
                               fill=color[self.tag])
            v = [[0, 1], [1, 0], [1, 1], [1, -1]]
            for i in v:
                x1, y1 = x, y
                while x1 < self.num - 1 and x1 > 0 and y1 > 0 and y1 < self.num - 1:
                    x1 += i[0]
                    y1 += i[1]
                count = 0
                while x1 <= self.num - 1 and x1 >= 0 and y1 >= 0 and y1 <= self.num - 1:
                    if self.QP[x1][y1] == self.tag:
                        count += 1
                        if count == 5:
                            self.win()
                    else:
                        count = 0
                    x1 -= i[0]
                    y1 -= i[1]
            self.tag = (self.tag + 1) % 2
            self.tagx, self.tagy = x, y
            self.te = 1
    def lose(self):
        global stop
        self.a.config(text=self.key[tag], fg=self.color[self.tag])
        self.b.config(text="认输", fg='black')
        stop = 1  # stop = 1时不能再放棋子了
    def win(self):
        global stop
        self.a.config(text=self.key[self.tag], fg=self.color[self.tag])
        self.b.config(text="获胜", fg='red')
        stop = 1
    def __init__(self):
        self.x,self.y ='',''
        # 创建一个socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 绑定IP端口
        self.server.bind(('127.0.0.1', 8080))
        # 监听
        self.server.listen(5)
        self.te = 0 #标记白方已走
        self.tag = 0  # tag标记该轮哪家走，0代表黑方，1代表白方
        self.stop = 0    #标记是否允许下子
        self.num = 18  # 棋盘网格数量
        self.K = 0.9  # 点击的灵敏度 0~1 之间
        self.Qr = 7  # 棋子的大小，前面的系数在0~0.5之间选取
        self.px = 5
        self.py = 50
        self.wide = 60
        self.high = 30
        self.mesh = round(400 / self.num)
        self.key = ["黑方", "白方"]
        self.color = ["black", "white"]
        # 初始化棋盘
        self.QP = []
        for i in range(self.num):
            self.QP.append([-1] * self.num)
        tk = Tk()
        tk.geometry(str((self.num + 1) * self.mesh + 2 * self.px) + 'x' + str((self.num + 1) * self.mesh + self.py + self.px))
        tk.title('五子棋')
        # 构造棋盘界面
        self.asdf = Canvas(tk, width=(self.num + 1) * self.mesh + 2 * self.px, height=(self.num + 1) * self.mesh + self.py + self.px)
        self.asdf.place(x=0, y=0)
        self.asdf.create_rectangle(0, 0, (self.num + 1) * self.mesh + 2 * self.px, (self.num + 1) * self.mesh + self.py + self.px, fill="#d7a605")
        self.canvas = Canvas(tk, width=str((self.num + 1) * self.mesh), height=str((self.num + 1) * self.mesh))
        self.canvas.place(x=self.px, y=self.py)
        self.canvas.create_rectangle(self.mesh - 20, self.mesh - 20, self.mesh * self.num + 20, self.mesh * self.num + 20, fill="#d7a65b")
        for i in range(self.num):
            self.canvas.create_line(self.mesh, self.mesh * (i + 1), self.mesh * self.num, self.mesh * (i + 1))
            self.canvas.create_line(self.mesh * (i + 1), self.mesh, self.mesh * (i + 1), self.mesh * self.num)
            self.canvas.bind("<Button-1>", self.callback)
        # 中间的文字
        self.a = Label(tk, text=self.key[self.tag], fg=self.color[self.tag], bg='green', font=("Times", "14", "bold"))
        self.b = Label(tk, text="走棋", fg=self.color[self.tag], bg='green', font=("Times", "14", "bold"))
        self.a.place(x=2 * self.px + 60 + 10 + 90, y=(self.py - self.high) / 2 + 4)
        self.b.place(x=(self.num + 1) * self.mesh + self.px - self.wide - self.px - 10 - 42 - 90, y=(self.py - self.high) / 2 + 4)
        t1 = threading.Thread(target=self.acceptMessage, args=(self.server,self.x,self.y,self))
        t1.start()
        tk.mainloop()
Server()