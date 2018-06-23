# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 15:24:14 2018

@author: xin.men
"""
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QAction, QMessageBox,QTextEdit,QLineEdit,QLabel,QFrame,QGridLayout,QVBoxLayout,QLayout 
import time  
from socket import *
from argparse import ArgumentParser
import sys 
import threading  

class MyWidget(QWidget):  
    def __init__(self, parent=None):  
        super(MyWidget, self).__init__(parent)  
        self.setWindowTitle('USER BLINKS DATA')  
        self.timer = QtCore.QTimer()  
        self.ip = QLineEdit()  
        self.time = QLineEdit()  
        self.num = QLineEdit()  
        self.label4 = QLabel("")
        
        label1 = QLabel("User Count: :")  
        label2 = QLabel("User IP：")  
        label3 = QLabel("Receive Time: ")
        label5 = QLabel("Blinks Number: ") 
  
        labelCol = 0  
        contentCol = 1  
  
        leftLayout = QGridLayout()  
        leftLayout.addWidget(label1, 0, labelCol)
        leftLayout.addWidget(self.label4, 0, contentCol, 1, 25)  
        leftLayout.addWidget(label2, 1, labelCol)  
        leftLayout.addWidget(self.ip, 1, contentCol, 1, 25)  
        leftLayout.addWidget(label3, 2, labelCol)  
        leftLayout.addWidget(self.time, 2, contentCol, 1, 25) 
        leftLayout.addWidget(label5, 3, labelCol)  
        leftLayout.addWidget(self.num, 3, contentCol, 1, 25) 
  
        self.ok_button = QPushButton("Read", self)  
        self.tip_button = QPushButton("New msg", self)  
  
        rightLayout = QVBoxLayout()  
         
        rightLayout.addWidget(self.tip_button) 
        rightLayout.addWidget(self.ok_button) 
  
        mainLayout = QGridLayout(self)  
        #mainLayout.setMargin(15)  
        mainLayout.setSpacing(15)  
        mainLayout.addLayout(leftLayout, 0, 0)  
        mainLayout.addLayout(rightLayout, 0, 1)  
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)  
 
        self.ok_button.clicked.connect(self.on_ok_button_clicked)

    @QtCore.pyqtSlot()  
    def on_ok_button_clicked(self):  
        #color = self.ok_button.palette().button().color()
        
        self.tip_button.setStyleSheet('''color: black;
                        background-color: gray+;''')
        QApplication.processEvents()
        time.sleep(1)
        return 0
      
ap = ArgumentParser()
ap.add_argument("-p", "--port", type = int, default=8080,
  help="the sending port")
args = vars(ap.parse_args()) 
flag = True 
clients = set()

def myquit():
    '''
    release resources when quit the window
    '''
    global flag
    flag = False
    time.sleep(1)
    udpServer.close()
    app.deleteLater()
    
def udp():
    '''
    Thread of udp server
    receive msg and show them
    '''
    host = '' #监听所有的ip
    port = args['port'] 
    bufsize = 1024
    addr = (host,port) 
    udpServer.bind(addr) #开始监听
    global flag
    udpServer.setblocking(0)# unblocking
    while flag :
        try :
            data,addr = udpServer.recvfrom(bufsize)  #接收数据和返回地址
            clients.add(addr)
            data = data.decode(encoding='utf-8')
            w.tip_button.setStyleSheet('''color: black;
                        background-color: red''')
            w.ip.setText(str(addr))
            w.num.setText(data)
            w.time.setText(str(time.ctime()))
            w.label4.setText(str(len(clients)))
            QApplication.processEvents()
            time.sleep(1)
        except Exception :
            pass
            #QApplication.processEvents()
        
udpServer = socket(AF_INET,SOCK_DGRAM)
t = threading.Thread(target = udp)
app = QApplication(sys.argv) 
w = MyWidget()

def main():  
    app.aboutToQuit.connect(myquit)  
    w.label4.setText("0") 
    w.show() 
    t.start()
    app.exec_()
    
if __name__ == "__main__":
    main()