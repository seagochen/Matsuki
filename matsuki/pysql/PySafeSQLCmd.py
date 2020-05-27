# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: May 08, 2018
# Modified: May 19, 2020

import re

from matsuki.pysql import PySQLConnection
from siki.basics import Exceptions


def _has_keywords(arg):
    pattern = r"(ALTER|CREATE|DELETE|DROP|EXEC(UTE){0,1}|INSERT( +INTO){0,1}|MERGE|SELECT|UPDATE|UNION( +ALL){0,1})"
    return re.search(pattern, arg) is not None


def _sql_args_check(*args):
    for arg in args:
        if _has_keywords(str(arg).upper()):
            return False
    return True


def safe_insert(conn, db, table, args, debug=False):
    """
    safely inserting database, and avoid sql injection attack
    
    Args:
    * [conn] connection of sql
    * [db] database name
    * [table] table name
    * [args(dict)] the data to insert, something like: {id:1, key1:val1, key2:val2, ...}
    * [debug] default to False, if you wannar to see the output sql statement, make it to True
    
    Returns:
    * [sql] str, command of sql
    """

    res = _sql_args_check(db, table, args.keys(), args.values())

    if res is False:
        raise Exceptions.SQLInjectionException(
            f"SQL injection detected, params: table[{table}], args[{args}]")

    if conn is None:
        raise Exceptions.InvalidParamException("conn cannot be null")

    if type(args) is not dict:
        raise Exceptions.InvalidParamException("args must be dict type")

    # generate a insert sql command
    keys = "`" + "`, `".join(args.keys()) + "`"
    values = "'" + "', '".join(args.values()) + "'"

    # generate insert sentence
    str_sql = f"INSERT INTO `{db}`.`{table}` ({keys}) VALUES ({values})"

    if debug:  # for debug only
        print(str_sql)

    # executing sql command
    return PySQLConnection.execute(conn, str_sql)


def safe_query_id(conn, db, table, item_id, debug=False):
    """
    safely querying database, and avoid sql injection attack

    Args:
    * [conn] connection of sql
    * [db] database name
    * [table] table name
    * [item_id] the item id want to search
    * [debug] default to False, if you wannar to see the output sql statement, make it to True

    Returns:
    * [rows(dict)] the execution results
    """
    res = _sql_args_check(db, table, item_id)
    if res is False:
        raise Exceptions.SQLInjectionException(
            f"SQL injection detected, params: table[{table}], id[{item_id}]")

    if conn is None:
        raise Exceptions.InvalidParamException("Conn cannot be null")

    # generate query sentence
    str_sql = f"SELECT * FROM `{db}`.`{table}` WHERE `id`='{item_id}'"

    if debug:  # for debug only
        print(str_sql)

    # executing sql
    return PySQLConnection.query(conn, str_sql)


def safe_simple_query(conn, db, table, select_con, where_con=None, order_by=None, debug=False):
    """
    safely simple querying, not allow nested querying to avoid sql injection.

    Args:
    * [conn] connection of sql
    * [db] database name
    * [table] table name
    * [select_con] selection condition
    * [where_con] where condition
    * [order_by] order by command, default sequency is asc, if you want a desc results, append "DESC" to your command
    * [debug] default to False, if you wannar to see the output sql statement, make it to True

    Returns:
    * [rows(dict/list)] dict, the execution results
    """
    res = _sql_args_check(db, table, select_con, where_con, order_by)
    if res is False:
        raise Exceptions.SQLInjectionException(
            f"SQL injection detected, params: table[{table}] select[{select_con}] where[{where_con}] order[{order_by}]"
        )

    if conn is None:
        raise Exceptions.InvalidParamException("Conn cannot be null")

    # generate simple querying
    str_sql = f'SELECT {select_con} FROM `{db}`.`{table}`'
    if where_con is not None:
        str_sql += f' WHERE {where_con}'
    if order_by is not None:
        str_sql += f' ORDER BY {order_by}'

    if debug:  # for debug only
        print(str_sql)

        # executing sql
    return PySQLConnection.query(conn, str_sql)


def safe_multiple_tables_query(conn, db: str, tables: list, select_con, where_con=None, order_by=None, debug=False):
    """
    safely multiple table cross querying, not allow nested querying to avoid sql injection.

    Args:
    * [conn] connection of sql
    * [db] database name
    * [tables] list of tables to query
    * [select_con] selection condition
    * [where_con] where condition
    * [order_by] order by command, default sequency is asc, if you want a desc results, append "DESC" to your command
    * [debug] default to False, if you wannar to see the output sql statement, make it to True

    Returns:
    * [rows(dict/list)] dict, the execution results
    """
    if not isinstance(tables, list):
        raise Exceptions.InvalidParamException("tables must be a list")

    res = _sql_args_check(db, *tables, select_con, where_con, order_by)
    if res is False:
        raise Exceptions.SQLInjectionException(
            f"SQL injection detected, params: table[{tables}] select[{select_con}] where[{where_con}] order[{order_by}]"
        )

    if conn is None:
        raise Exceptions.InvalidParamException("Conn cannot be null")

    # generate simple querying
    str_tables = ''
    for t in tables:
        str_tables += f"`{db}`.`{t}`,"

    str_sql = f"SELECT {select_con} FROM {str_tables[:-1]}"
    if where_con is not None:
        str_sql += f' WHERE {where_con}'
    if order_by is not None:
        str_sql += f' ORDER BY {order_by}'

    if debug:  # for debug only
        print(str_sql)

    # executing sql
    return PySQLConnection.query(conn, str_sql)


def safe_update(conn, db, table, item_id, args, debug=False):
    """
    safely updating database, and avoid sql injection attack

    Args:
    * [conn] connection of sql
    * [db] database name
    * [table] table name
    * [item_id] the item id want to update
    * [args(dict)] the data to update, something like: {id:1, key1:val1, key2:val2, ...}
    * [debug] default to False, if you wannar to see the output sql statement, make it to True

    Returns:
    * [sql] str, the command of sql
    """
    res = _sql_args_check(db, table, item_id, args.keys(), args.values())
    if res is False:
        raise Exceptions.SQLInjectionException(
            f"SQL injection detected, params: table[{table}] item_id[{item_id}] vals[{args}]"
        )

    if conn is None:
        raise Exceptions.InvalidParamException("Conn cannot be null")

    # generate sql querying
    setval = []
    for key, val in args.items():
        if val:
            setval.append("`" + str(key) + "`='" + str(val) + "'")
        else:
            setval.append("`" + str(key) + "`=NULL")
    p_vals = ", ".join(setval)

    # generate sql
    str_sql = f"UPDATE `{db}`.`{table}` SET {p_vals} WHERE `id`='{item_id}'"

    if debug:  # for debug only
        print(str_sql)

        # executing sql
    return PySQLConnection.execute(conn, str_sql)


def safe_delete(conn, db, table, item_id, debug=False):
    """
    safely deleting row in table

    Args:
    * [conn] connection of sql
    * [db] database name
    * [table] table name
    * [item_id] the item id want to delete

    Returns:
    * [sql] str, the command of sql    
    """
    res = _sql_args_check(table, item_id)
    if res is False:
        raise Exceptions.SQLInjectionException(
            f"SQL injection detected, params: table[{table}] item_id[{item_id}]"
        )

    if conn is None:
        raise Exceptions.InvalidParamException("Conn cannot be null")

    # generate sql
    str_sql = f"DELETE FROM `{db}`.`{table}` WHERE `id` = '{item_id}'"

    if debug:  # for deubg
        print(str_sql)

    # executing sql
    return PySQLConnection.execute(conn, str_sql)


def safe_query_tables(conn, db):
    """
    safely show tables in schema

    Args:
    * [conn] connection of sql
    * [db] database name

    Returns:
    * [rows] dict, the execution results
    * [sql] str, the command of sql    
    """
    res = _sql_args_check(db)
    if res is False:
        raise Exceptions.SQLInjectionException(f"SQL injection detected, params: db[{db}]")

    if conn is None:
        raise Exceptions.InvalidParamException("Conn cannot be null")

    # generating sql
    str_sql = f"SHOW TABLES IN `{db}`"

    # executing sql
    final_results = []
    for i in PySQLConnection.query(conn, str_sql):  # obtaining a list
        for k, v in i.items():
            final_results.append(v)
    return final_results


def safe_query_columns(conn, db, table):
    """
    safely show columns in table

    Args:
    * [conn] connection of sql
    * [db] database name
    * [table] table name

    Returns:
    * [rows] dict, the execution results
    * [sql] str, the command of sql    
    """
    res = _sql_args_check(db, table)
    if res is False:
        raise Exceptions.SQLInjectionException(f"SQL injection detected, params: db[{db}] table[{table}]")

    if conn is None:
        raise Exceptions.InvalidParamException("Conn cannot be null")

    # generating sql
    str_sql = f'SHOW COLUMNS IN `{db}`.`{table}`'

    # executing sql
    return PySQLConnection.query(conn, str_sql)  # obtaining a list
