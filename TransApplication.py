#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Xmind转换Excel小工具
@author: cathy
'''
import sys
import xmind
import xlwt
import logging
import os
from application import ShowLog
import xlrd
from PySide import QtCore, QtGui
from application.Mainform_ui import Ui_MainWindow
from PySide.QtGui import QWidget
from xmind.core import workbook,saver
from fileinput import filename
from xmind.core.topic import TopicElement

reload(sys) 
sys.setdefaultencoding('utf-8')

class MainForm(QtGui.QMainWindow):
    def __init__(self):
        super(MainForm, self).__init__()
        self.ui = Ui_MainWindow()
        self.initUi()
        self.head_name = ["功能点","用例名称","优先级","步骤","期待结果","用例类型","版本","备注"]
        self.orinFileType = None
        self.orinFile = None
        
    def initUi(self):
        '''初始化UI'''
        self.ui.setupUi(self)
        self.actionInit()
        self.ui.lineEditOrin.setReadOnly(True)
        self.setLog()
            
    def initProgressDialog(self,sheet_num):
        '''初始化转换进度对话框'''
        self.pd =  QtGui.QProgressDialog(u"文件转换中...", "Cancel", 0, sheet_num)
        self.pd.setValue(0)
        self.pd.setAutoClose(False)
        self.pd.setAutoReset(False)
        self.pd.show()           
        
    def updateProgressDialog(self):
        '''更新转换进度对话框中的进度''' 
        current_value = self.pd.value()
        self.pd.setValue(current_value+1)
        if(current_value+1 == self.pd.maximum()):
            self.pd.setCancelButtonText(u"完成")  
            self.pd.setLabelText(u"文件转换已完成")   
        
    def actionInit(self):
        '''初始化action'''    
        self.ui.action_ReadXmind.triggered.connect(self.openXmind)
        self.ui.action_ReadExcel.triggered.connect(self.openExcel)
        self.ui.pBtnTrans.clicked.connect(self.transHandle)
        self.ui.action_exit.triggered.connect(self.close)
    
            
    def transHandle(self):
        """将源文件进行转换"""
        self.ui.textBrowser.setText("")
        if self.orinFileType == None:
            msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Icon.Critical,u"Error",u"源文件为空，转换失败")
            msgBox.exec_() 
            return False
        correctFileType = ["Xmind Files (*.xmind)","Excel Files (*.xlsx *.xls )"]
        if self.orinFileType  not in correctFileType:
            msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Icon.Critical,u"Error",u"源文件格式错误，转换失败")
            msgBox.exec_()
            return False
        if self.orinFileType == correctFileType[0]:
            self.transXmind()
        elif self.orinFileType == correctFileType[1]:
            self.transExcel()
          
        
    def openXmind(self):
        """打开一个Xmind文件"""
        self.orinFile,self.orinFileType = None,None
        self.ui.lineEditOrin.setText("")
        
        file_dialog = QtGui.QFileDialog()
        fileName,filtr = file_dialog.getOpenFileName(self,self.tr(u"打开Xmind文件"), os.getcwd(), self.tr("Xmind Files (*.xmind)"))
        if fileName is None:
            return False
        
        self.ui.lineEditOrin.setText(fileName)
        self.ui.textBrowser.setText("")
        self.orinFile,self.orinFileType = fileName,filtr
        return True
        #self.transXmind(fileName)
    
    def transXmind(self):
        """将Xmind文件转换为Excel表格
        """
        outFileName, outFiltr = QtGui.QFileDialog.getSaveFileName(self,self.tr(u"保存Excel文件"), os.getcwd(), self.tr("Excel Files (*.xls )")) 
        if not outFileName:
            return False
        
        workbook = xmind.load(self.orinFile)
        wbExcel = xlwt.Workbook(encoding='utf-8')
        sheet = workbook.getSheets()[0]
        if self.transSheet2Excel(sheet,wbExcel,outFileName):
            self.initProgressDialog(1) # 暂时只支持单个sheet转换
            self.updateProgressDialog()    
        wbExcel.save(outFileName)
        
    def transSheet2Excel(self,sheet,wbExcel,outFileName):
        """将Xmind的一张sheet转为Excel"""
        cases_table = sheet.transPathToCases()
        if cases_table is False:
            self.ui.textBrowser.insertPlainText(u"Error：转换失败，文件中格式有误\n") 
            msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Icon.Critical,u"Error",u"转换失败")
            msgBox.exec_()
            return False
        module_name = sheet.get_module_name()
        sheetExcel = wbExcel.add_sheet(module_name)
        j=0
        title=xlwt.easyxf(u'font:name 仿宋,height 240 ,colour_index black, bold on, italic off; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_colour light_orange;') #字体黑色加粗，自动换行、垂直居中、水平居中,背景色橙色  
        normal=xlwt.easyxf(u'font:colour_index black, bold off, italic off; align: wrap on, vert centre, horiz left;') #字体黑色不加粗，自动换行、垂直居中、水平居左  
        for property in self.head_name:
            sheetExcel.write(0,j,property.decode('UTF-8'),title)
            j=j+1
        i = 1
        for case in cases_table:
            j=0
            for property in self.head_name:
                sheetExcel.write(i,j,case[property].decode('UTF-8'),normal)
                j=j+1
            i=i+1   
        sheetExcel.col(1).width = 256*40
        sheetExcel.col(3).width = 256*50
        sheetExcel.col(4).width = 256*50
        
        line1 = "转换成功:"+"\n"
        line2 = "需求名称: " +module_name + "\n"
        line3 = "共%d条用例" %(len(cases_table)) + "\n"
        line4 = "输出文件地址：" + outFileName + "\n"
        self.ui.textBrowser.insertPlainText(line1+line2+line3+line4)  
        return True
                    
    def openExcel(self):
        """打开一个Excel文档"""        
        self.ui.lineEditOrin.setText("")
        file_dialog = QtGui.QFileDialog()
        fileName,filtr = file_dialog.getOpenFileName(self,self.tr(u"打开Excel文件"), os.getcwd(), self.tr("Excel Files (*.xlsx *.xls )"))
        if fileName is None:
            return False
        self.ui.lineEditOrin.setText(fileName)
        self.ui.textBrowser.setText("")  
        self.orinFileType = filtr
        self.orinFile = fileName
        return True
    
    def loadExcel(self,fileName):
        workbook = xlrd.open_workbook(fileName)
        table = workbook.sheets()[0]
        sheetName = workbook.sheet_names()[0]
        return table,sheetName
    
    def readSheet(self,sheet):
        '''获取Excel中sheet中的信息，每一行储存为一个字典，将这些字典放在一个list中'''
        if sheet is None :
            logging.error("Excel中信息为空")
            return False
        nrows = sheet.nrows
        ncols = sheet.ncols
        if nrows<2 or ncols != 8:
            logging.error("Excel中行列格式有误")
            return False
        caseList = []
        for i in range(1,nrows):
            dict={"功能点":"","用例名称":"","优先级":"","步骤":"","期待结果":"","用例类型":"","版本":"","备注":""}
            dict["功能点"]   = sheet.cell(i,0).value
            dict["用例名称"] =sheet.cell(i,1).value
            dict["优先级"]=sheet.cell(i,2).value
            dict["步骤"]=sheet.cell(i,3).value
            dict["期待结果"]=sheet.cell(i,4).value
            dict["用例类型"]=sheet.cell(i,5).value
            dict["版本"]=sheet.cell(i,6).value
            dict["备注"]=sheet.cell(i,7).value
            for key in dict:
                if key in ["步骤","备注"]:
                    continue
                if dict[key] is None or str(dict[key]).strip() == "":
                    logging.error("测试用例中存在"+key+"为空，转换失败" )
                    return False
            caseList.append(dict)
        return caseList
    
    def creatTopic(self,title):
        topic = TopicElement()
        topic.setTitle(title)
        return topic
    
    def copyTopic(self,topic):
        """复制生成一个新节点，包括原来节点的标记、备注"""
        newTopic = self.creatTopic(topic.getTitle())
        type,priority = topic.get_type_priority()
        newTopic.setPriorityType(priority, type)
        step,notes = topic.getStepNotes()
        newTopic.setStepsNotes(step,notes)
        return newTopic
    
    def transCaseToTopic(self,caseList,moduleTopic):
        """将excel的一行测试用例，转变为topic节点集合，并将所有行转换后的结果放在topicList中"""
        topicList = []
        for case in caseList:
            topic = []
            startTopic = self.creatTopic(moduleTopic.getTitle())
            functionTopic = self.creatTopic(case["功能点"])
            startTopic.addSubTopic(functionTopic)
            topic.append(functionTopic)
            case["用例名称"] = case["用例名称"].replace(",","，")
            names = case["用例名称"].split("，")
            for i in names:
                if i is None or str(i).strip() =="":
                    logging.error("Excel中用例名称格式存在问题，转换失败")
                    return 
                nameTopic = self.creatTopic(i)
                topic.append(nameTopic)
            resultTopic = self.creatTopic(case["期待结果"])
            topic.append(resultTopic)
            # 倒数第二个节点上标记用例优先级和用例类型
            topic[-2].setPriorityType(str(case["优先级"]),str(case["用例类型"]))
            # 最后一个节点上标记备注
            resultTopic.setStepsNotes(str(case["步骤"]),str(case["备注"]))
            for i in range(0,len(topic)-1):
                topic[i].addSubTopic(topic[i+1]) # 将路径中所有的节点相连接，后续判断两个节点是否在同一路径上用
            topicList.append(topic)    
        return topicList    

    def generateXmind(self,caseList,sheetName):
        """利用caseList中的用例，生成Xmind图"""
        if caseList is None :
            logging.error("Excel转换失败")
            return None
        workbook = xmind.load("NotExist.xmind")
        sheet = workbook.getPrimarySheet()
        sheet.setTitle(sheetName) 
        moduleTopic =sheet.getRootTopic()  
        moduleTopic.setTitle(sheetName)
        moduleTopic.addVersionTopic(caseList[0]["版本"])
        topicList = self.transCaseToTopic(caseList,moduleTopic)
        if topicList is None:
            logging.error("Excel转换失败")
            return None
        for path in topicList:
            parentNode = moduleTopic
            for topic in path:
                sameTopic = self.find_topic_by_title(moduleTopic,topic.getTitle())
                #print sameTopic.getTitle(),topic.getTitle(),self.isSameCase(topic, sameTopic, moduleTopic)
                #找到了相同节点，那么置下一次循环的topic的父节点为已找到的相同节点
                if self.isSameCase(topic, sameTopic, moduleTopic):
                    parentNode = sameTopic          
                # 未找到相同节点，那么在父节点后添加一个"
                else :
                    newTopic = self.copyTopic(topic)
                    parentNode.addSubTopic(newTopic) 
                    parentNode = newTopic                             
        return workbook
       
    def find_topic_by_title(self,root_topic,title):
        '''利用深度优先搜索，查找指定title的topic的集合，有可能不止一个
        '''
        if root_topic == None:
            return None
        if root_topic.getTitle()==title:
            return root_topic
        child_topic = root_topic.getSubTopics()
        if child_topic is not None:
            for i in child_topic:
                #print root_topic.getTitle(),i.getTitle(),title
                if self.find_topic_by_title(i,title) is not None :
                    root_topic = self.find_topic_by_title(i,title)
        return root_topic
    
    def isSameCase(self,topicA,topicB,root):
        """判断某两个主题是否为在同一路径上
        eg:
            1.用例为：打开应用，点击按钮，音乐开启
            2.用例为：打开应用，双击屏幕，音乐开始。
            -由于判断树中是否存在某一相同节点，依据是节点中的文字，所以这里“音乐开启”会被认为是已经出现的同一节点，但是实际上为不同路径中的不同节点。
            -因此这里根据主题节点的父节点中的文字是否一致，来判断两个文字相同的节点是否为同一路径上的同一节点。
        """
        
        if topicA is None or topicB is None:
            return False
        if topicA.getTitle() != topicB.getTitle():
            return False
        parentA = topicA.getParentTopic()
        parentB = topicB.getParentTopic()
        while parentA is not None and parentB is not None:
            if(parentA.getTitle() == parentB.getTitle()):
                parentA = parentA.getParentTopic()
                parentB = parentB.getParentTopic()
            else:
                return False 
        # 遍历到最后parentA 和parentB 应该都为None 这条路径才相同，否则不同 
        if parentA is None and parentB is None:
            return True
        return False
        
    def transExcel(self):
        outFileName, outFiltr = QtGui.QFileDialog.getSaveFileName(self,self.tr(u"保存Xmind文件"), os.getcwd(), self.tr("Xmind Files (*.xmind )")) 
        if not outFileName:
            return False
        
        sheet,sheetName = self.loadExcel(self.orinFile)
        caseList = self.readSheet(sheet)
        if not caseList:
            return False 
        workbook = self.generateXmind(caseList,sheetName)
        if workbook is not None:
            line1 = "转换Excel至Xmind成功:"+"\n"
            line2 = "需求名称: " +sheetName + "\n"
            line3 = "共%d条用例" %(len(caseList)) + "\n"
            line4 = "输出文件地址：" + outFileName + "\n"
            self.ui.textBrowser.insertPlainText(line1+line2+line3+line4)  
            xmind.save(workbook, outFileName)    
            self.initProgressDialog(1)
            self.updateProgressDialog() 
        else:
            return False
        
    def setLog(self):
        logger = logging.getLogger(__name__)
        handler = ShowLog.QtHandler()
        handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        logger.addHandler(handler)         
        ShowLog.XStream.stdout().messageWritten.connect( self.ui.textBrowser.insertPlainText )
        ShowLog.XStream.stderr().messageWritten.connect( self.ui.textBrowser.insertPlainText )
        
if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    mainForm = MainForm()
    mainForm.show()
    sys.exit(app.exec_())
