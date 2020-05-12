# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Mar 25, 2020
# LastChg: May 11, 2020
#
# 由多个表创建复合表
# 
# 需要假定用户输入的全部数据正确


from siki.dstruct import DictExtern
from siki.basics import Exceptions


def pick_items_from_list(comparing_value, target_table, target_key_name, default_blank=True):
    """
    某个值，需要从目标表中查找出来，如果未找到对应的项，默认留空，设置为False，则返回None
    """
    if not isinstance(target_table, list): # 不是给定的数据结构，target table必须是list类型
        raise Exceptions.InvalidParamException("target_table is not list type")

    feedback = []

    for item in target_table:

        if not isinstance(item, dict): # item必须是可查找的dict类型
            raise Exceptions.InvalidParamException("items in target_table is not dict type")

        if target_key_name not in item.keys(): # 给定的目标建名不在item中
            raise Exceptions.InvalidParamException("target_key_name is not contained in item")

        if comparing_value == item[target_key_name]: # 找到了给定的项目
            feedback.append(item)

    # 有数据, 返回数据
    if len(feedback) > 0:
        return feedback

    # 没有找到给定的项目
    if default_blank: # 需要留白
        return [ DictExtern.create_dict_from_keylist(target_table[0].keys()) ]
    else:
        return None


def concatenate_two_items(name_a: str, dict_a: dict, name_b: str, dict_b: dict, auto_rename=True):
    """
    合并两个item，但是可能存在着a和b之间有重复命名的类型，出现了重复命名时，默认把两个重复名称各自按照name_key的形式重新命名
    修改为False，则a的值会覆盖b的值，如果希望b的值覆盖a的值，需要调整顺序
    """

    # 重复检测
    keys_in_a = dict_a.keys()
    renamed_keys = []
    for key in keys_in_a:
        if key in dict_b.keys(): # 发现重复
            renamed_keys.append(key) 

    if auto_rename:
        for key in renamed_keys:
            # 修改a
            temp_a = dict_a.pop(key)
            dict_a["{}_{}".format(name_a, key)] = temp_a

            #修改b
            temp_b = dict_b.pop(key)
            dict_b["{}_{}".format(name_b, key)] = temp_b
    
    else: # 覆盖
        for key in renamed_keys:
            dict_b.pop(key)

    # 合并
    return DictExtern.union(dict_a, dict_b)


def rename_table_rows(table: list, row_name: str, renamed_name: str):
    """
    批量的把列表名字全部重新命名
    """
    for row in table:
        row[renamed_name] = row[row_name]
        del row[row_name]
    
    return table


def basic_left_join(left_table_name: str, left_table: list, left_key_name: str,
    right_table_name:str, right_table: list, right_key_name: str,
    default_blank=True, auto_rename=True):
    """
    左表(m)与右表(n)进行组合，生成中间表(m:n)，左表存在的项目，而右表不存在的项目，空缺项目默认以空表示，
    设置为False后，则跳过

    如果要进行右连接，调整相关参数位置即可
    """
    if not isinstance(left_table, list) or not isinstance(right_table, list):
        raise Exceptions.InvalidParamException("table should be list")

    # auto_rename 为True, 进行左链接前,进行key检测
    if auto_rename:
        dump_names = []
        for name in left_table[0].keys():
            if name in right_table[0].keys():
                dump_names.append(name)
        
        for name in dump_names:

            # 对数据中出现的重复名字进行重命名,以防出现赋值错误
            if left_key_name == name:
                left_key_name = "{}_{}".format(left_table_name, name)
            if right_key_name == name:
                right_key_name = "{}_{}".format(right_table_name, name)

            # 重命名出现重复的column
            left_table = rename_table_rows(left_table, name, "{}_{}".format(left_table_name, name))
            right_table = rename_table_rows(right_table, name, "{}_{}".format(right_table_name, name))


    # 最终数据存储
    concatenate_table = []

    # 链接前检查
    if left_key_name not in left_table[0].keys(): # 需要链接的字不存在数据中
        raise Exceptions.InvalidParamException(
            "key name: {} should be exists in table {}, table with keys: {}"
            .format( left_key_name, left_table_name, left_table[0].keys() ) )
        
    if right_key_name not in right_table[0].keys():
        raise Exceptions.InvalidParamException(
            "key name: {} should be exists in table {}, table with keys: {}"
            .format( right_key_name, right_table_name, right_table[0].keys() ) )
    
    # 开始数据表链接
    for left_row in left_table:

        # 从左表中,找出对应键的值
        left_main_key_val = left_row[left_key_name]
        
        # 从右表中,找出对应的行(1个或多个)
        right_rows = pick_items_from_list(left_main_key_val, right_table, right_key_name, default_blank)

        if right_rows: # append new row to new table
            for right_row in right_rows:
                concatenate_table.append( concatenate_two_items(
                    left_table_name, left_row, 
                    right_table_name, right_row, 
                    auto_rename) )

    # return to caller
    return concatenate_table



def concatenate_with_left_join(default_blank=True, auto_rename=True, *args):
    """
    concatenate table list

    以左连接表的形式进行创建新的合成表，输入参数为元组列表形式
    元组结构为
    
    (table_name, rows, concatenate_key_name)
    
    使用该方法，需要最少两组元组
    rows必须是dict的list，即[dict1, dict2, dict3, ...]
    """

    if len(args) < 2: # 构造失败，因为组数小于2
        raise Exceptions.NoAvailableResourcesFoundException("this method needs two more lists to concatenate")

    concatenate_table = None
    left_primary_key = None
    concatenate_name = None

    for table_tuple in args:

        if concatenate_table is None: # 获取第一个表
            concatenate_name = table_tuple[0]
            concatenate_table = table_tuple[1]
            left_primary_key = table_tuple[2]

        else:
            concatenate_table = basic_left_join(
                concatenate_name, concatenate_table, left_primary_key, 
                table_tuple[0], table_tuple[1], table_tuple[2],
                default_blank, auto_rename)

    return concatenate_table


if __name__ == "__main__":
    data1_sample =  [
        {'id':'1', 'name':'data1'},
        {'id':'2', 'name':'data2'},
        {'id':'3', 'name':'data3'},
        {'id':'4', 'name':'data4'},
        {'id':'5', 'name':'data5'}
    ]
    

    data2_sample = [
        {'uid':'2', 'name': 't1', 'data':1},
        {'uid':'2', 'name': 't2', 'data':2},
        {'uid':'3', 'name': 't3', 'data':3}
    ]


    data3_sample = [
        {'gid':'2', 'pname': 'tp1', 'zdata':11},
        {'gid':'2', 'pname': 'tp2', 'zdata':12},
        {'gid':'3', 'pname': 'tp3', 'zdata':13},
        {'gid':'4', 'pname': 'tp4', 'zdata':14}
    ]

    
    # print("---------------pick_items_from_list---------------")
    print( pick_items_from_list('2', data2_sample, 'uid') )
    # print(pick_items_from_list('5', data2_sample, 'uid'))
    # print(pick_items_from_list('5', data2_sample, 'uid', False))
    # print(pick_items_from_list('7', data2_sample, 'uid'))
    # test done

    # print("---------------concatenate_two_items---------------")
    # print(concatenate_two_items("left", data1_sample[1], "right", data2_sample[0]))
    # print(concatenate_two_items("left", data1_sample[2], "right", data2_sample[2], False))
    # test done

    # print("---------------basic_left_join---------------")
    # rows = basic_left_join(
    #     "left", data2_sample, "uid", 
    #     "right", data1_sample, "id", 
    #     True, True)
    # for row in rows:
    #    print(row)
    # test done

    # print("---------------rename_table_rows---------------")
    # rows = rename_table_rows(data3_sample, "pname", "test")
    # for row in rows:
    #    print(row)
    # test done

    print("---------------concatenate_with_left_join---------------")
    rows = concatenate_with_left_join(True, True, ("d1", data1_sample, "id"), ("d2", data2_sample, "uid"), ("d3", data3_sample, "gid"))
    for row in rows:
        if row['id'] and row['uid'] and row['gid']:
            print(row)
    # test done
    
