#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
    xmind.core.sheet
    ~~~~~~~~~~~~~~~~

    :mod:``xmind.core.sheet` command XMind sheets manipulation

    :copytright:
    :license:
"""
from comtypes.client._generate import PATH

__author__ = "aiqi@xmind.net <Woody Ai>"

from . import const

from .mixin import WorkbookMixinElement
from .topic import TopicElement
from .title import TitleElement
from .relationship import RelationshipElement, RelationshipsElement

import logging

class SheetElement(WorkbookMixinElement):
    TAG_NAME = const.TAG_SHEET

    def __init__(self, node=None, ownerWorkbook=None):
        super(SheetElement, self).__init__(node, ownerWorkbook)

        self.addIdAttribute(const.ATTR_ID)
        self._root_topic = self._get_root_topic()

    def _get_root_topic(self):
        # This method initialize root topic, if not root topic
        # DOM implementation, then create one
        topics = self.getChildNodesByTagName(const.TAG_TOPIC)
        owner_workbook = self.getOwnerWorkbook()
        if len(topics) >= 1:
            root_topic = topics[0]
            root_topic = TopicElement(root_topic, owner_workbook)
        else:
            root_topic = TopicElement(ownerWorkbook=owner_workbook)
            self.appendChild(root_topic)

        return root_topic

    def createRelationship(self, end1, end2, title=None):
        """
        Create a relationship between two different topics and return the
        created rel. Please notice that the created rel will not be added to
        sheet. Call `addRelationship()` to add rel to sheet.

        :param end1:    topic ID
        :param end2:    topic ID
        :param title:   relationship title, default by None

        """
        rel = RelationshipElement(ownerWorkbook=self.getOwnerWorkbook())
        rel.setEnd1ID(end1)
        rel.setEnd2ID(end2)

        if title is not None:
            rel.setTitle(title)

        return rel

    def _getRelationships(self):
        return self.getFirstChildNodeByTagName(const.TAG_RELATIONSHIPS)

    def addRelationship(self, rel):
        """
        Add relationship to sheet
        """
        _rels = self._getRelationships()
        owner_workbook = self.getOwnerWorkbook()

        rels = RelationshipsElement(_rels, owner_workbook)

        if not _rels:
            self.appendChild(rels)

        rels.appendChild(rel)

    def removeRelationship(self, rel):
        """
        Remove a relationship between two different topics
        """
        rels = self._getRelationships()

        if not rels:
            return

        rel = rel.getImplementation()
        rels.removeChild(rel)
        if not rels.hasChildNodes():
            self.getImplementation().removeChild(rels)

        self.updateModifiedTime()

    def getRootTopic(self):
        return self._root_topic

    def _get_title(self):
        return self.getFirstChildNodeByTagName(const.TAG_TITLE)

    # FIXME: convert to getter/setter
    def getTitle(self):
        title = self._get_title()
        if title:
            title = TitleElement(title, self.getOwnerWorkbook())
            return title.getTextContent()

    def setTitle(self, text):
        _title = self._get_title()
        title = TitleElement(_title, self.getOwnerWorkbook())
        title.setTextContent(text)

        if _title is None:
            self.appendChild(title)

        self.updateModifiedTime()

    def getParent(self):
        workbook = self.getOwnerWorkbook()
        if workbook:
            parent = self.getParentNode()

            if (parent == workbook.getWorkbookElement().getImplementation()):
                return workbook

    def updateModifiedTime(self):
        super(SheetElement, self).updateModifiedTime()

        workbook = self.getParent()
        if workbook:
            workbook.updateModifiedTime() 
    
    def get_module_name(self):
        """获取该sheet中需求的名称
        @author: cathy
        @return: 需求的名称
        """
        return self.getRootTopic().getTitle()
    
    def getAllleafNodes(self):
        """获取sheet中所有的末节点"""
        nodeStack = []
        leafNodes = []
        rootTopic = self.getRootTopic()
        nodeStack.append(rootTopic)
        print rootTopic
        while(len(nodeStack)>0):
            node = nodeStack.pop(0)
            subTopics = node.getSubTopics()
            if subTopics is None:
                leafNodes.append(node)
            else:
                for subTopic in subTopics:
                    nodeStack.append(subTopic)
        return leafNodes
    
    def transLeafNodes(self):
        """将所有末节点转变为测试用例，并存储在AllCases中"""
        leafNodes = self.getAllleafNodes()
        AllCases = []
        for leaf in leafNodes:
            AllCases.append(leaf.transLeafNode2Case())
        return AllCases
    
    def getAllPath(self):
        """获取从根节点开始到末节点的所有路径"""
        rootTopic = self.getRootTopic()
        allPath = []
        onePath = []
        self.FindPath(rootTopic, onePath, allPath)   
        return allPath
    
    def FindPath(self,topic,onePath,allPath):
        """递归获取一条从根节点到末节点的路径"""
        onePath.append(topic)
        subTopics = topic.getSubTopics()
        if subTopics is None:
            path = onePath[:] # python 的列表为浅拷贝，因此这里要复制新生成一个list
            allPath.append(path)
        else:
            for subTopic in subTopics:
                self.FindPath(subTopic, onePath, allPath)
        onePath.pop(-1)
    
    def transPathToCases(self):
        """将所有的路径转变为用例，返回用例的列表"""
        allPath = self.getAllPath()
        allCases = []
        for path in allPath:
            testcase = TestCase(path)
            if testcase.getCase() is None:
                return False    
            allCases.append(testcase.getCase())
        return allCases
    
class TestCase():
    def __init__(self,path):
        self.path = path
        self.dict = None
        if path is None or len(path)<4:
            logging.error("思维导图中存在层级小于4的用例，转换失败")
            return 
        dict={"需求名称":"","功能点":"","用例名称":"","优先级":"","步骤":"","期待结果":"","用例类型":"","版本":"","备注":""}
        dict["功能点"]= path[1].getTitle()
        dict["需求名称"] = path[0].getTitle()
        dict["用例类型"],dict["优先级"] = self.getTypePriority()
        dict["步骤"],dict["备注"] = path[-1].getStepNotes()
        dict["期待结果"]=path[-1].getTitle()
        dict["版本"] = self.getVersion(path[0])
        dict["用例名称"] =""
        for i in path[2:-1]:
            if i.getTitle() is None or str(i.getTitle()).strip() == "":
                logging.error("测试用例中存在用例名称为空，转换失败" )
                return
            dict["用例名称"] += i.getTitle()
            if i != path[-2]:
                dict["用例名称"] +="，"
        for key in dict:
            if key in ["步骤","备注"]:
                continue
            if dict[key] is None or str(dict[key]).strip() == "":
                logging.error("测试用例中存在"+key+"为空，转换失败" )
                return
        self.dict = dict
        
    def getTypePriority(self):
        """获取该路径上的标记：用例类型和优先级"""
        typeList = []
        priorityList = []
        type,priority = "",""
        for topic in self.path:
            if topic.getSubTopics() is None or len(topic.getSubTopics())>1:
                #若节点有超过一个孩子节点，那么在该节点上标记用例类型和优先级作废对应不明确，那么不取这些标记
                continue
            else: 
                type,priority = topic.get_type_priority()
                if type is not None:
                    typeList.append(type)
                if priority is not None:
                    priorityList.append(priority)
        if len(typeList)>1:
            logging.error("【"+topic.getTitle() + "】上标记用例类型有多个，转换失败")
            return False
        if len(priorityList)>1:
            logging.error("【"+topic.getTitle() + "】上标记用例优先级有多个，转换失败")
            return False
        if len(typeList) == 0:
            type = "功能逻辑"
        else:
            type = typeList[0]
        if len(priorityList) == 0:
            priority = "P1"
        else:
            priority = priorityList[0]
        return type,priority
    
    def getVersion(self,rootTopic):
        """获取该用例的版本号"""
        floatTopic = rootTopic.getSubTopics(topics_type="detached")
        if floatTopic is None or len(floatTopic) > 1:
            logging.error("测试用例格式中floating topic（版本号）数量不为1，转换失败")
            return 
        text = floatTopic[0].getTitle()
        text = str(text).strip()
        if text is None or text == "":
            logging.error("测试用例格式中版本号为空，转换失败")
            return 
        return text       
             
    def getCase(self):
        if self.dict is None:
            return None
        return self.dict        
    
def main():
    pass


if __name__ == '__main__':
    main()
