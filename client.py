from tkinter import *
import socket, threading
class Client():
    # 画棋子
    def callback(self, event):
        if self.te:
            color = ["black", "black"]
            data = str(event.x) + ":" + str(event.y)
            self.client.send(data.encode("utf-8"))
            x = round(event.x / self.mesh) - 1
            y = round(event.y / self.mesh) - 1
            errorX = self.mesh * (x + 1) - event.x
            errorY = self.mesh * (y + 1) - event.y
            dis = (errorX ** 2 + errorY ** 2) ** 0.5
            if self.QP[x][y] == -1 and dis < self.K / 2 * self.mesh and self.stop == 0:
                self.a.config(text=self.key[(self.tag + 1) % 2], fg=color[(self.tag + 1) % 2])
                self.QP[x][y] = self.tag
                self.canvas.create_oval(self.mesh * (x + 1) - self.Qr, self.mesh * (y + 1) - self.Qr,
                                        self.mesh * (x + 1) + self.Qr, self.mesh * (y + 1) + self.Qr,
                                        fill=self.color[self.tag])
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
    def callbackServer(self, eventx, eventy):
        # global tag, tagx, tagy, a
        color = ["white", "white"]
        x = round(eventx / self.mesh) - 1
        y = round(eventy / self.mesh) - 1
        errorX = self.mesh * (x + 1) - eventx
        errorY = self.mesh * (y + 1) - eventy
        dis = (errorX ** 2 + errorY ** 2) ** 0.5
        if self.QP[x][y] == -1 and dis < self.K / 2 * self.mesh and self.stop == 0:
            self.a.config(text=self.key[(self.tag + 1) % 2], fg=color[(self.tag + 1) % 2])
            self.QP[x][y] = self.tag
            self.canvas.create_oval(self.mesh * (x + 1) - self.Qr, self.mesh * (y + 1) - self.Qr,
                                    self.mesh * (x + 1) + self.Qr, self.mesh * (y + 1) + self.Qr,
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
    # 胜利
    def win(self, ):
        global stop
        self.a.config(text=self.key[self.tag], fg=self.color[self.tag])
        self.b.config(text="获胜", fg='red')
        self.stop = 1
    def connectServer(self):
        address = self.entry.get()
        print(address)
        self.client.connect((address, 8080))
        t1 = threading.Thread(target=self.acceptMessage, args=(self.client, self))
        t1.start()
    def acceptMessage(self, client, th):
        print(2)
        while True:
            x, y = client.recv(1024).decode("gbk").split(":")
            eventx = int(x)
            eventy = int(y)
            self.callbackServer(eventx, eventy)
            print(x, y)
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.te = 1 # 标记黑方已走
        self.tag = 0  # tag标记该轮哪家走，0代表黑方，1代表白方
        self.stop = 0  # 标记是否允许下子
        self.num = 18  # 棋盘网格数量
        self.K = 0.9  # 点击的灵敏度 0~1 之间
        self.Qr = 7  # 棋子的大小，前面的系数在0~0.5之间选取
        self.px = 5
        self.py = 5
        self.wide = 60
        self.high = 30
        self.mesh = round(400 / self.num)
        self.key = ["黑方", "白方"]
        self.color = ["black", "black"]
        root = Tk()
        root.resizable(0, 0)
        root.title("局域网五子棋对战")
        root.geometry()
        frame1 = Frame(root, width=450, height=470, padx=10, pady=10)
        frame2 = Frame(root, width=150, height=470,  padx=10, pady=10)
        frame3 = Frame(frame1, width=450, height=20,  padx=15, pady=5)
        frame4 = Frame(frame1, width=450, height=450, padx=5, pady=5)
        frame5 = Frame(frame2, width=150, height=235,  padx=5, pady=5)
        frame6 = Frame(frame2, width=150, height=235, padx=5, pady=5)
        label1 = Label(frame3, text="五子棋大战", font=("宋体", 30), padx=10, pady=10)
        label1.pack()
        # 界面右面设计
        label2 = Label(frame5, text="目标主机", bg="white", padx=5, pady=5)
        self.entry = Entry(frame5)
        button = Button(frame5, text="连接", command=self.connectServer)
        label2.grid(row=0, column=0)
        self.entry.grid(row=0, column=1)
        button.grid(row=1, column=0)
        # 初始化棋盘
        self.QP = []
        for i in range(self.num):
            self.QP.append([-1] * self.num)
            # 构造棋盘界面
        self.asdf = Canvas(frame4, width=(self.num + 1) * self.mesh + 2 * self.px,
                           height=(self.num + 1) * self.mesh + self.py + self.px)
        self.asdf.place(x=0, y=0)
        self.asdf.create_rectangle(0, 0, (self.num + 1) * self.mesh + 2 * self.px,
                                   (self.num + 1) * self.mesh + self.py + self.px, fill="#d7a65b")
        self.canvas = Canvas(frame4, width=str((self.num + 1) * self.mesh), height=str((self.num + 1) * self.mesh))
        self.canvas.place(x=self.px, y=self.py)
        self.canvas.create_rectangle(self.mesh - 20, self.mesh - 20, self.mesh * self.num + 20,
                                     self.mesh * self.num + 20, fill="#d7a65b")
        for i in range(self.num):
            self.canvas.create_line(self.mesh, self.mesh * (i + 1), self.mesh * self.num, self.mesh * (i + 1))
            self.canvas.create_line(self.mesh * (i + 1), self.mesh, self.mesh * (i + 1), self.mesh * self.num)
            self.canvas.bind("<Button-1>", self.callback)
        # 中间的文字
        self.a = Label(frame4, text=self.key[self.tag], fg=self.color[self.tag], bg='#d7a65b',
                       font=("Times", "14", "bold"))
        self.b = Label(frame4, text="走棋", fg=self.color[self.tag], bg='#d7a65b', font=("Times", "14", "bold"))
        self.a.place(x=2 * self.px + 60 + 10 + 90, y=(self.py - self.high) / 2 + 4)
        self.b.place(x=(self.num + 1) * self.mesh + self.px - self.wide - self.px - 10 - 42 - 90,
                     y=(self.py - self.high) / 2 + 4)
        frame3.pack(side=TOP)
        frame4.pack(side=BOTTOM)
        frame5.pack(side=TOP)
        frame6.pack(side=BOTTOM)
        frame1.pack(side=LEFT)
        frame2.pack(side=RIGHT)
        root.mainloop()


Client()



