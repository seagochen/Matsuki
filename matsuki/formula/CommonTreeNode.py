# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Mar 03, 2020
# LastChg: Apr 07, 2020

from typing import TypeVar

CommonTreeNode = TypeVar('CommonTreeNode')

class CommonTreeNode(object):

    def __init__(self, item_id, item_name, item_groupid):
        self.item_id = item_id
        self.item_name = item_name
        self.item_groupid =item_groupid
        self.children = []
    



    def __str__(self):
        return str(self.generate_tree())




    def generate_tree(self):
        output = {
            "id": self.item_id,
            "name": self.item_name,
            "gid": self.item_groupid
        }

        if len(self.children) <= 0:
            return output

        else:
            subtrees = []
            for child in self.children:
                subtrees.append(child.generate_tree())
            
            output["children"] = subtrees
            return output        



    
    def search_append(self, node: CommonTreeNode):
        """
        将一个node加入到树中，使操作成立的唯一条件是，给定的
        node.item_gid == self.item_id
        即当前的node是给定的node的父节点，当然，如果当前根节点无法比对，
        会查找其所拥有的子节点，并且采用递归进行调用
        """

        if node.item_groupid == self.item_id: # self是node的父节点
            self.children.append(node)
            return True
        
        else: # self不是node的父节点，进行递归调用
            if len(self.children) > 0: # 有可用的子节点，对子节点进行递归调用
                for sub_root in self.children:
                    if sub_root.search_append(node): # 插入了正确的子节点中
                        return True
                    
                    else: # 该子节点不是目标节点
                        continue

                # 查找结束，没有可供插入的节点
                return False
            
            else: # 没有可用子节点，直接返回False
                return False




    def search_subtree(self, nodeid):
        """
        从生成的树中，找出需要的子节点，nodeid的类型必须与树的id类型一致
        """
        if self.item_id == nodeid: # self是需要找的节点
            return self

        else: # self不是要找的节点
            if len(self.children) > 0: # 递归查找子节点
                for sub_root in self.children:
                    if sub_root.item_id == nodeid: # 找到该子节点
                        return sub_root
                    
                    elif len(sub_root.children) > 0: # 该节点不是，但有子节点
                        node = sub_root.search_subtree(nodeid)
                        if node: # 深度搜索找到了该子节点
                            return node
                        
                        # 深度搜索未找到该子节点，查找下一个节点
                        continue

                # 查找结束，没有可供返回的节点
                return None
            else:
                return None # 没有可用的节点

    
    def traversal(self):
        """
        将树结构重新转换为列表结构，便于进行一些类似SQL的操作
        """
        from siki.dstruct import ListExtern

        token = {
            "id": self.item_id,
            "name": self.item_name,
            "gid": self.item_groupid
        }

        the_list = []
        the_list.append(token)

        # 不包含子数据的时候
        if len(self.children) <= 0:
            return the_list
        
        # 包含多条子数据的时候
        for child in self.children:
            sub_list = child.traversal()
            the_list = ListExtern.union(the_list, sub_list)

        # 返回
        return the_list


    def all_leaves(self):
        """
        遍历一遍树，把其中的叶节点全部找出来

        @Returns:
        * [list], 叶节点列表
        """
        from siki.dstruct import ListExtern

        token = {
            "id": self.item_id,
            "name": self.item_name,
            "gid": self.item_groupid
        }

        the_list = []

        # 不包含子节点，即叶节点
        if len(self.children) <= 0:
            the_list.append(token)
            return the_list
        
        # 包含多条子数据的时候
        for child in self.children:
            sub_list = child.all_leaves()
            the_list = ListExtern.union(the_list, sub_list)
            
        # 返回
        return the_list


if __name__ == "__main__":
    # root
    n1 = CommonTreeNode("10", "root", "0")
    
    # level 1
    n2 = CommonTreeNode("11", "leaf1-1", "10")
    n3 = CommonTreeNode("12", "leaf1-2", "10")
    n4 = CommonTreeNode("13", "leaf1-3", "10")
    
    # level 2
    n5 = CommonTreeNode("14", "leaf2-1", "11")
    n6 = CommonTreeNode("15", "leaf2-2", "11")
    n7 = CommonTreeNode("16", "leaf2-3", "13")

    # level 3
    n8 = CommonTreeNode("17", "leaf3-1", "16")

    nodes = [n1, n2, n3, n4, n5, n6, n7, n8]
    
    # generate tree
    for i in range(1, 8):
        n1.search_append(nodes[i])

    #print(n1)

    n = n1.search_subtree("15")
    #print(n)

    #print(n1.traversal())
    print(n1.all_leaves())