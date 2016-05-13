# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Mainform-ui.ui'
#
# Created: Thu May 12 19:16:28 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(556, 318)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.labelOrinFile = QtGui.QLabel(self.centralwidget)
        self.labelOrinFile.setObjectName("labelOrinFile")
        self.gridLayout.addWidget(self.labelOrinFile, 0, 0, 1, 1)
        self.lineEditOrin = QtGui.QLineEdit(self.centralwidget)
        self.lineEditOrin.setObjectName("lineEditOrin")
        self.gridLayout.addWidget(self.lineEditOrin, 0, 1, 1, 1)
        self.pBtnTrans = QtGui.QPushButton(self.centralwidget)
        self.pBtnTrans.setObjectName("pBtnTrans")
        self.gridLayout.addWidget(self.pBtnTrans, 0, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.textBrowser = QtGui.QTextBrowser(self.centralwidget)
        self.textBrowser.setOpenExternalLinks(True)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 556, 23))
        self.menubar.setObjectName("menubar")
        self.menu_2 = QtGui.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.action_ReadXmind = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/new_branding_new_logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_ReadXmind.setIcon(icon)
        self.action_ReadXmind.setObjectName("action_ReadXmind")
        self.action_ReadExcel = QtGui.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/img/647702-excel-512.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_ReadExcel.setIcon(icon1)
        self.action_ReadExcel.setObjectName("action_ReadExcel")
        self.action_exit = QtGui.QAction(MainWindow)
        self.action_exit.setObjectName("action_exit")
        self.action_3 = QtGui.QAction(MainWindow)
        self.action_3.setObjectName("action_3")
        self.menu_2.addAction(self.action_ReadXmind)
        self.menu_2.addAction(self.action_ReadExcel)
        self.menu_2.addSeparator()
        self.menu_2.addAction(self.action_exit)
        self.menubar.addAction(self.menu_2.menuAction())
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_ReadXmind)
        self.toolBar.addAction(self.action_ReadExcel)
        self.toolBar.addSeparator()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Xmind转换工具箱", None, QtGui.QApplication.UnicodeUTF8))
        self.labelOrinFile.setText(QtGui.QApplication.translate("MainWindow", "源文件  ：", None, QtGui.QApplication.UnicodeUTF8))
        self.pBtnTrans.setText(QtGui.QApplication.translate("MainWindow", "选择输出文件地址并转换", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_2.setTitle(QtGui.QApplication.translate("MainWindow", "文件", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.action_ReadXmind.setText(QtGui.QApplication.translate("MainWindow", "读取Xmind文件", None, QtGui.QApplication.UnicodeUTF8))
        self.action_ReadExcel.setText(QtGui.QApplication.translate("MainWindow", "读取Excel文件", None, QtGui.QApplication.UnicodeUTF8))
        self.action_exit.setText(QtGui.QApplication.translate("MainWindow", "退出", None, QtGui.QApplication.UnicodeUTF8))
        self.action_3.setText(QtGui.QApplication.translate("MainWindow", "转换", None, QtGui.QApplication.UnicodeUTF8))

import img_rc
