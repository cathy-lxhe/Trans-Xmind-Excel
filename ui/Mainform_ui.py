# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Mainform-ui.ui'
#
# Created: Fri Apr 22 16:38:36 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(902, 647)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.verticalLayout_2.setStretch(0, 5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 902, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtGui.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.action_2 = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_2.setIcon(icon)
        self.action_2.setObjectName("action_2")
        self.action_3 = QtGui.QAction(MainWindow)
        self.action_3.setObjectName("action_3")
        self.action_5 = QtGui.QAction(MainWindow)
        self.action_5.setObjectName("action_5")
        self.actionXmind_Excel = QtGui.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/img/new_branding_new_logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionXmind_Excel.setIcon(icon1)
        self.actionXmind_Excel.setObjectName("actionXmind_Excel")
        self.actionExcel_Xmind = QtGui.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/img/647702-excel-512.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExcel_Xmind.setIcon(icon2)
        self.actionExcel_Xmind.setObjectName("actionExcel_Xmind")
        self.action_6 = QtGui.QAction(MainWindow)
        self.action_6.setObjectName("action_6")
        self.action_8 = QtGui.QAction(MainWindow)
        self.action_8.setObjectName("action_8")
        self.menu.addAction(self.action_2)
        self.menu.addAction(self.action_3)
        self.menu.addAction(self.action_6)
        self.menu.addSeparator()
        self.menu.addAction(self.action_8)
        self.menu_2.addAction(self.actionXmind_Excel)
        self.menu_2.addAction(self.actionExcel_Xmind)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.toolBar.addAction(self.action_2)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionXmind_Excel)
        self.toolBar.addAction(self.actionExcel_Xmind)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Xmind转换工具箱", None, QtGui.QApplication.UnicodeUTF8))
        self.menu.setTitle(QtGui.QApplication.translate("MainWindow", "文件", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_2.setTitle(QtGui.QApplication.translate("MainWindow", "转换", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.action_2.setText(QtGui.QApplication.translate("MainWindow", "保存", None, QtGui.QApplication.UnicodeUTF8))
        self.action_3.setText(QtGui.QApplication.translate("MainWindow", "保存为...", None, QtGui.QApplication.UnicodeUTF8))
        self.action_5.setText(QtGui.QApplication.translate("MainWindow", "退出", None, QtGui.QApplication.UnicodeUTF8))
        self.actionXmind_Excel.setText(QtGui.QApplication.translate("MainWindow", "Xmind转为Excel", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExcel_Xmind.setText(QtGui.QApplication.translate("MainWindow", "Excel转为Xmind", None, QtGui.QApplication.UnicodeUTF8))
        self.action_6.setText(QtGui.QApplication.translate("MainWindow", "保存所有", None, QtGui.QApplication.UnicodeUTF8))
        self.action_8.setText(QtGui.QApplication.translate("MainWindow", "退出", None, QtGui.QApplication.UnicodeUTF8))

import img_rc
