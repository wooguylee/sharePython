# -*- coding: utf-8 -*-
#from tkinter import *
from Tkinter import *
import socket
import time
from threading import Thread

class netClass(Thread):
    def __init__(self, evtcallback, svrport, tmout):
        Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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
    

class tkUdpTester:
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
        
        self.edtIpAddr = Entry(self.root)
        self.edtIpAddr.place(x=0, width=100)
        self.edtIpAddr.insert(0, "192.168.2.255")
        
        self.edtSendStr = Entry(self.root)
        self.edtSendStr.place(x=100, width=300)
        self.edtSendStr.insert(0, "@PING;")
        
        self.btSend = Button(self.root, text="send", command=self.sendData)
        self.btSend.place(x=400, width=50)
        
        self.btClear = Button(self.root, text="clear", command=self.clearLog)
        self.btClear.place(x=450,width=50)
        
        self.logList = Listbox(self.root)
        self.logList.place(x=0, rely=0.2, relheight=0.8, relwidth=1)
        self.addLog("0")
        self.addLog("1")
        self.addLog("2")
        
        self.root.mainloop()
        self.netsock.stop()
        
    def addLog(self, logStr):
        self.logList.insert(self.logList.size(), logStr)
        
    def sendData(self):
        strIp = self.edtIpAddr.get()
        strData = self.edtSendStr.get()
        self.netsock.sendData(strIp, strData)
        #self.addLog("[" + strIp + "]" + strData)
        
    def clearLog(self):
        self.logList.delete(0, self.logList.size())
        
    def net_callback(self, rcvData, rcvIp, rcvPort):
        logStr = "[{}:{}]{}".format(rcvIp, rcvPort, rcvData)
        self.addLog(logStr)
        

if __name__ == "__main__":
    main = tkUdpTester()
    main.start()
    #main.start(100, 100, 500, 300)