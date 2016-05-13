#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
    xmind.core.topic
    ~~~~~~~~~~~~~~~~

    :copyright:
    :license:

"""
from Queue import PriorityQueue

__author__ = "aiqi@xmind.net <Woody Ai>"

from . import const

from .mixin import WorkbookMixinElement
from .title import TitleElement
from .position import PositionElement
from .notes import NotesElement, PlainNotes
from .markerref import MarkerRefElement
from .markerref import MarkerRefsElement
from .markerref import MarkerId

from .. import utils

import logging

def split_hyperlink(hyperlink):
    colon = hyperlink.find(":")
    if colon < 0:
        protocol = None
    else:
        protocol = hyperlink[:colon]

    hyperlink = hyperlink[colon + 1:]
    while hyperlink.startswith("/"):
        hyperlink = hyperlink[1:]

    return (protocol, hyperlink)


class TopicElement(WorkbookMixinElement):
    TAG_NAME = const.TAG_TOPIC

    def __init__(self, node=None, ownerWorkbook=None):
        super(TopicElement, self).__init__(node, ownerWorkbook)

        self.addIdAttribute(const.ATTR_ID)
        self.parentText = None
        
    def _get_title(self):
        return self.getFirstChildNodeByTagName(const.TAG_TITLE)

    def _get_markerrefs(self):
        return self.getFirstChildNodeByTagName(const.TAG_MARKERREFS)

    def _get_position(self):
        return self.getFirstChildNodeByTagName(const.TAG_POSITION)

    def _get_children(self):
        return self.getFirstChildNodeByTagName(const.TAG_CHILDREN)

    def _set_hyperlink(self, hyperlink):
        self.setAttribute(const.ATTR_HREF, hyperlink)
        #self.updateModifiedTime()

    def getOwnerSheet(self):
        parent = self.getParentNode()

        while parent and parent.tagName != const.TAG_SHEET:
            parent = parent.parentNode

        if not parent:
            return

        owner_workbook = self.getOwnerWorkbook()
        if not owner_workbook:
            return

        for sheet in owner_workbook.getSheets():
            if parent is sheet.getImplementation():
                return sheet

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

        # self.updateModifiedTime()

    def getMarkers(self):
        refs = self._get_markerrefs()
        if not refs:
            return None
        tmp = MarkerRefsElement(refs, self.getOwnerWorkbook())
        markers = tmp.getChildNodesByTagName(const.TAG_MARKERREF)
        marker_list = []
        if markers:
            for i in markers:
                marker_list.append(MarkerRefElement(i, self.getOwnerWorkbook()))
        return marker_list

    def addMarker(self, markerId):

        if not markerId:
            return None
        if type(markerId) == str:
            markerId = MarkerId(markerId)

        refs = self._get_markerrefs()
        if not refs:
            tmp = MarkerRefsElement(None, self.getOwnerWorkbook())
            self.appendChild(tmp)
        else:
            tmp = MarkerRefsElement(refs, self.getOwnerWorkbook())
        markers = tmp.getChildNodesByTagName(const.TAG_MARKERREF)
        if markers:
            for m in markers:
                mre = MarkerRefElement(m, self.getOwnerWorkbook())
                # look for a marker of same familly
                if mre.getMarkerId().getFamilly() == markerId.getFamilly():
                    mre.setMarkerId(markerId)
                    return mre
        # not found so let's append it
        mre = MarkerRefElement(None, self.getOwnerWorkbook())
        mre.setMarkerId(markerId)
        tmp.appendChild(mre)
        return mre

    def setFolded(self):
        self.setAttribute(const.ATTR_BRANCH, const.VAL_FOLDED)

        # self.updateModifiedTime()

    def getPosition(self):
        """ Get a pair of integer located topic position.

        return (x, y) indicate x and y
        """
        position = self._get_position()
        if position is None:
            return

        position = PositionElement(position, self.getOwnerWorkbook())

        x = position.getX()
        y = position.getY()

        if x is None and y is None:
            return

        x = x or 0
        y = y or 0

        return (int(x), int(y))

    def setPosition(self, x, y):
        ownerWorkbook = self.getOwnerWorkbook()
        position = self._get_position()

        if not position:
            position = PositionElement(ownerWorkbook=ownerWorkbook)
            self.appendChild(position)
        else:
            position = PositionElement(position, ownerWorkbook)

        position.setX(x)
        position.setY(y)

        # self.updateModifiedTime()

    def removePosition(self):
        position = self._get_position()
        if position is not None:
            self.getImplementation().removeChild(position)

        # self.updateModifiedTime()

    def getType(self):
        parent = self.getParentNode()
        if not parent:
            return

        if parent.tagName == const.TAG_SHEET:
            return const.TOPIC_ROOT

        if parent.tagName == const.TAG_TOPICS:
            topics = TopicsElement(parent, self.getOwnerWorkbook())
            return topics.getType()
    
    def getTopics(self, topics_type=const.TOPIC_ATTACHED):
        topic_children = self._get_children()

        if topic_children:
            topic_children = ChildrenElement(
                topic_children,
                self.getOwnerWorkbook())

            return topic_children.getTopics(topics_type)

    def getSubTopics(self, topics_type=const.TOPIC_ATTACHED):
        """ List all sub topics under current topic, If not sub topics,
        return None.
        """
        topics = self.getTopics(topics_type)
        if not topics:
            return

        return topics.getSubTopics()
    
    def getSubTopicsWithParent(self, topics_type=const.TOPIC_ATTACHED): 
        topics = self.getTopics(topics_type)
        if not topics:
            return
        parentName = self.getTitle()
        return topics.getSubTopicsWithParent(parentName)   
          
    def getSubTopicByIndex(self, index, topics_type=const.TOPIC_ATTACHED):
        """ Get sub topic by speicifeid index
        """
        sub_topics = self.getSubTopics(topics_type)
        if sub_topics is None:
            return

        if index < 0 or index >= len(sub_topics):
            return sub_topics

        return sub_topics[index]

    def addSubTopic(self, topic=None, index=-1,
                    topics_type=const.TOPIC_ATTACHED):
        """
        Add a sub topic to the current topic and return added sub topic

        :param topic:   `TopicElement` object. If not `TopicElement` object
                        passed then created new one automatically.
        :param index:   if index not given then passed topic will append to
                        sub topics list. Otherwise, index must be less than
                        length of sub topics list and insert passed topic
                        before given index.
        """
        ownerWorkbook = self.getOwnerWorkbook()
        topic = topic or self.__class__(None, ownerWorkbook)

        topic_children = self._get_children()
        if not topic_children:
            topic_children = ChildrenElement(ownerWorkbook=ownerWorkbook)
            self.appendChild(topic_children)
        else:
            topic_children = ChildrenElement(topic_children, ownerWorkbook)

        topics = topic_children.getTopics(topics_type)
        if not topics:
            topics = TopicsElement(ownerWorkbook=ownerWorkbook)
            topics.setAttribute(const.ATTR_TYPE, topics_type)
            topic_children.appendChild(topics)

        topic_list = []
        for i in topics.getChildNodesByTagName(const.TAG_TOPIC):
            topic_list.append(TopicElement(i, ownerWorkbook))

        if index < 0 or len(topic_list) >= index:
            topics.appendChild(topic)
        else:
            topics.insertBefore(topic, topic_list[index])

        return topic

    def getIndex(self):
        parent = self.getParentNode()
        if parent and parent.tagName == const.TAG_TOPICS:
            index = 0
            for child in parent.childNodes:
                if self.getImplementation() == child:
                    return index
                index += 1
        return -1

    def getHyperlink(self):
        return self.getAttribute(const.ATTR_HREF)

    def setFileHyperlink(self, path):
        """
        Set file as topic hyperlink

        :param path: path of specified file

        """
        protocol, content = split_hyperlink(path)
        if not protocol:
            path = const.FILE_PROTOCOL + utils.get_abs_path(path)

        self._set_hyperlink(path)

    def setTopicHyperlink(self, tid):
        """
        Set topic as topic hyperlink

        :param id: given topic's id

        """
        protocol, content = split_hyperlink(tid)
        if not protocol:
            if tid.startswith("#"):
                tid = tid[1:]

            tid = const.TOPIC_PROTOCOL + tid
        self._set_hyperlink(tid)

    def setURLHyperlink(self, url):
        """ Set URL as topic hyperlink

        :param url: HTTP URL to specified website

        """
        protocol, content = split_hyperlink(url)
        if not protocol:
            url = const.HTTP_PROTOCOL + content

        self._set_hyperlink(url)

    def getNotes(self):
        """
        Return `NotesElement` object` and invoke
        `NotesElement.getContent()` to get notes content.
        """

        notes = self.getFirstChildNodeByTagName(const.TAG_NOTES)

        if notes is not None:
            return NotesElement(notes, self)

    def _set_notes(self):
        notes = self.getNotes()

        if notes is None:
            notes = NotesElement(ownerTopic=self)
            self.appendChild(notes)

        return notes

    def setPlainNotes(self, content):
        """ Set plain text notes to topic

        :param content: utf8 plain text

        """
        notes = self._set_notes()
        new = PlainNotes(content, None, self)

        old = notes.getFirstChildNodeByTagName(new.getFormat())
        if old is not None:
            notes.getImplementation().removeChild(old)

        notes.appendChild(new)
        
       
    def get_type_priority(self):
        """通过标记获取节点上的标记优先级和用例类型"""
        marks = self.getMarkers()
        dict_priority = {"priority-1":'P0',"priority-3":'P2'}
        dict_type = {"flag-red":'UI与系统兼容'}
        type = None
        priority = None
        if marks is None:
            return type,priority
        for mark in marks:
            id = str(mark.getMarkerId())
            if dict_priority.has_key(id):
                priority=dict_priority[id]
            elif dict_type.has_key(id):
                type = dict_type[id]
        return type,priority
    
        
    def getStepNotes(self):
        """获取节点备注里的步骤和备注"""
        notes_content = ""
        step,notes= "",""
        if self.getNotes() is not None:
            notes_content = self.getNotes().getContent() 
        else:
            return step,notes
        notes_rows = []
        if not '\n' in notes_content:
            notes_rows.append(notes_content)
        else:
            notes_rows = notes_content.split( '\n') 
        notes_dict={}
        for rows in notes_rows:
            rows = str(rows)
            if rows.strip() == "": # 处理某些行为空行的特殊情况
                continue
            rows = rows.replace(":","：")
            row_split = rows.split( "：",1) # 只分割一次
            notes_dict[row_split[0].encode( 'utf -8')] = row_split[1].encode('utf-8' )
        
        if notes_dict.has_key("步骤"):
            step = notes_dict["步骤"]
        if notes_dict.has_key("备注"):
            notes = notes_dict["备注"]
          
        return step,notes
     
    def getParentTopic(self):
        """获取主题的父主题"""
        parent = self.getParentNode()
        if parent is None:
            return 
        
        while parent and parent.tagName != const.TAG_TOPIC:
            if parent.tagName == const.TAG_SHEET:
                return None
            parent = parent.parentNode   
        parentTopic = TopicElement(parent, self.getOwnerWorkbook()) 
        return parentTopic
    
    def setPriorityType(self,priority=None,type=None):
        """设置topic的优先级和用例类型，用图标标记"""
        dictPriority ={"P0":"priority-1","P1":None,"P2":"priority-3"}
        dictType = {"UI与系统兼容":"flag-red","功能逻辑":None}
        if priority is not None and not (priority in dictPriority.keys()):
            logging.warn("Excel中存在未定义的用例优先级【"+str(priority)+"】，默认置为P0")
        if type is not None and not (type in dictType.keys()):
            logging.warn("Excel中存在未定义的用例类型【"+str(type)+"】默认置为功能逻辑用例")
        if dictPriority.has_key(priority):
            self.addMarker(dictPriority[priority])
        if dictType.has_key(type):
            self.addMarker(dictType[type])
        
    
    def setStepsNotes(self,steps,notes):
        """设置topic的步骤和备注，用Note来存储这些信息"""
        contents = ""
        if steps is not None and steps != "":
            steps = str(steps).replace("\n","；")
            stepText = "步骤："+steps +"\n"
            contents += stepText
        if notes is not None and notes != "":
            notes = str(notes).replace("\n","；")
            noteText = "备注："+notes +"\n"
            contents += noteText
        if contents == "":
            return None
        self.setPlainNotes(contents)
    
    def addVersionTopic(self,verstion):
        """新建一个FloatingTopic，表示版本号"""
        versionTopic = TopicElement()
        versionTopic.setTitle(verstion)
        self.addSubTopic(versionTopic,topics_type ="detached" )
        
class ChildrenElement(WorkbookMixinElement):
    TAG_NAME = const.TAG_CHILDREN

    def __init__(self, node=None, ownerWorkbook=None):
        super(ChildrenElement, self).__init__(node, ownerWorkbook)

    def getTopics(self, topics_type):
        topics = self.iterChildNodesByTagName(const.TAG_TOPICS)
        for i in topics:
            t = TopicsElement(i, self.getOwnerWorkbook())
            if topics_type == t.getType():
                return t


class TopicsElement(WorkbookMixinElement):
    TAG_NAME = const.TAG_TOPICS

    def __init__(self, node=None, ownerWorkbook=None):
        super(TopicsElement, self).__init__(node, ownerWorkbook)

    def getType(self):
        return self.getAttribute(const.ATTR_TYPE)

    def getSubTopics(self):
        """
        List all sub topics on the current topic
        """
        topics = []
        ownerWorkbook = self.getOwnerWorkbook()
        for t in self.getChildNodesByTagName(const.TAG_TOPIC):
            topics.append(TopicElement(t, ownerWorkbook))

        return topics
    
    def getSubTopicsWithParent(self,parentName):
        topics = []
        ownerWorkbook = self.getOwnerWorkbook()
        for t in self.getChildNodesByTagName(const.TAG_TOPIC):
            topicWithParent = TopicElement(t, ownerWorkbook)
            topicWithParent.setParentText(parentName)
            topics.append(topicWithParent)

        return topics

    
    def getSubTopicByIndex(self, index):
        """
        Get specified sub topic by index
        """
        sub_topics = self.getSubTopics()
        if index < 0 or index >= len(sub_topics):
            return sub_topics

        return sub_topics[index]


def main():
    pass

if __name__ == '__main__':
    main()
