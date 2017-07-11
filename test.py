#coding=utf-8  
  
import sys  
  
from PyQt4 import QtGui  
from PyQt4.QtCore import Qt  
  
class MainWindow(QtGui.QMainWindow):  
    def __init__(self):  
        super(MainWindow, self).__init__()  
        self.createContextMenu()  
  
  
    def createContextMenu(self):  
        ''''' 
        创建右键菜单 
        '''  
        # 必须将ContextMenuPolicy设置为Qt.CustomContextMenu  
        # 否则无法使用customContextMenuRequested信号  
        self.setContextMenuPolicy(Qt.CustomContextMenu)  
        self.customContextMenuRequested.connect(self.showContextMenu)  
  
        # 创建QMenu  
        self.contextMenu = QtGui.QMenu(self)  
        self.actionA = self.contextMenu.addAction(u'动作A')  
        self.actionB = self.contextMenu.addAction(u'动作B')  
        self.actionC = self.contextMenu.addAction(u'动作C')  
        # 将动作与处理函数相关联  
        # 这里为了简单，将所有action与同一个处理函数相关联，  
        # 当然也可以将他们分别与不同函数关联，实现不同的功能  
        self.actionA.triggered.connect(self.actionHandler)  
        self.actionB.triggered.connect(self.actionHandler)  
        self.actionB.triggered.connect(self.actionHandler)  
  
  
    def showContextMenu(self, pos):  
        ''''' 
        右键点击时调用的函数 
        '''  
        # 菜单显示前，将它移动到鼠标点击的位置  
        self.contextMenu.move(self.pos() + pos)  
        self.contextMenu.show()  
  
  
    def actionHandler(self):  
        ''''' 
        菜单中的具体action调用的函数 
        '''  
        print('action handler'  )
  
  
if __name__=='__main__':  
    app = QtGui.QApplication(sys.argv)  
    window = MainWindow()  
    window.show()  
    sys.exit(app.exec_()) 