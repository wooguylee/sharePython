# -*- coding: utf-8 -*-
#from tkinter import *
from Tkinter import *
import socket
from threading import Thread

class netClass(Thread):
    def __init__(self, evtcallback, svrport, tmout):
        Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind(('', svrport))
        self.sock.settimeout(tmout)
        self.evtcallback = evtcallback
        self.isRun = True
        
    def run(self):
        while self.isRun:
            try:
                data, addr = self.sock.recvfrom(200)                
                rcvdata = data.decode()
                #self.sock.sendto(rcvdata.encode(), (addr[0], addr[1]))                
                self.evtcallback(rcvdata, addr[0], addr[1])
            
            except socket.timeout:
                print("Timeout Exception")
        
        self.sock.close()
        
    def sendData(self, targetIp, sendData):
        self.sock.sendto(sendData.encode(), (targetIp, 8989))
        
    def stop(self):
        self.isRun = False
    

class tkColControl:
    def __init__(self):
        print("__init__")
        self.root = Tk()
        
    def start(self, x=0, y=0, w=0, h=0):
        print("start")
        if (x == 0) | (y == 0) :
            self.root.attributes("-fullscreen", True)
        else:
            geostr = "{}x{}+{}+{}".format(w, h, x, y)
            print(geostr)
            self.root.geometry(geostr)

        self.netsock = netClass(self.net_callback, 8989, 0.5)
        self.netsock.start()
        
        wVal = 80
        mwVal = 20
        
        self.scaleVol1 = Scale(self.root, command=self.chg1, from_=0, to=-64)
        self.scaleVol2 = Scale(self.root, command=self.chg2, from_=0, to=-64)
        self.scaleVol3 = Scale(self.root, command=self.chg3, from_=0, to=-64)
        self.scaleVol4 = Scale(self.root, command=self.chg4, from_=0, to=-64)
        self.scaleVol5 = Scale(self.root, command=self.chg5, from_=0, to=-64)
        self.scaleVol6 = Scale(self.root, command=self.chg6, from_=0, to=-64)
        self.scaleVol7 = Scale(self.root, command=self.chg7, from_=0, to=-64)
        self.scaleVol8 = Scale(self.root, command=self.chg8, from_=0, to=-64)

        self.scaleVol1.place(x=10 + (wVal + mwVal) * 0, y=10, width=wVal, height=400)
        self.scaleVol2.place(x=10 + (wVal + mwVal) * 1, y=10, width=wVal, height=400)
        self.scaleVol3.place(x=10 + (wVal + mwVal) * 2, y=10, width=wVal, height=400)
        self.scaleVol4.place(x=10 + (wVal + mwVal) * 3, y=10, width=wVal, height=400)
        self.scaleVol5.place(x=10 + (wVal + mwVal) * 4, y=10, width=wVal, height=400)
        self.scaleVol6.place(x=10 + (wVal + mwVal) * 5, y=10, width=wVal, height=400)
        self.scaleVol7.place(x=10 + (wVal + mwVal) * 6, y=10, width=wVal, height=400)
        self.scaleVol8.place(x=10 + (wVal + mwVal) * 7, y=10, width=wVal, height=400)
        
        self.btExit = Button(self.root, text="Exit", command=self.exitProgram)
        self.btExit.place(x=700, y=410, width=100, height=70)

        self.root.mainloop()
        self.netsock.stop()

    def net_callback(self, rcvData, rcvIp, rcvPort):
        logStr = "[{}:{}]{}".format(rcvIp, rcvPort, rcvData)
        print(logStr)

    def scaleValueChange(self, idx, value):
        val = int("{}".format(value)) + 64
        sendData = "@SETPREGAIN:5,{},{};".format(idx, val)
        print(sendData)
        self.netsock.sendData("192.168.2.255", sendData)
        
    def chg1(self, value):
        self.scaleValueChange(1, value)

    def chg2(self, value):
        self.scaleValueChange(2, value)

    def chg3(self, value):
        self.scaleValueChange(3, value)

    def chg4(self, value):
        self.scaleValueChange(4, value)

    def chg5(self, value):
        self.scaleValueChange(5, value)

    def chg6(self, value):
        self.scaleValueChange(6, value)

    def chg7(self, value):
        self.scaleValueChange(7, value)

    def chg8(self, value):
        self.scaleValueChange(8, value)
        
    def exitProgram(self):
        self.root.close()

if __name__ == "__main__":
    main = tkColControl()
    main.start()
    #main.start(100, 100, 800, 480)