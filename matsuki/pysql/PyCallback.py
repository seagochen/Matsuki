# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Create: Apr 15, 2020
# Modifi: Apr 15, 2020

from matsuki.pysql import PySafeSQLCmd, PySQLConnection
from matsuki.pysql.PySQLPool import PySQLPool
from siki.basics import Exceptions

def database_do_action(database: PySQLPool, do_action: object, *args):
    """
    用于数据库连接池自释放，提供一个可供用户使用的数据库连接和回调函数

    @Args:
    * [database] 用于访问的数据库
    * [do_action] 回调函数, 函数结构为callback(conn, [args]), 如果不需要附加参数，那么回调函数只为callback(conn)
    * [args] 用户需要添加的参数
    """
    if not isinstance(database, PySQLPool):
        raise Exceptions.NoAvailableResourcesFoundException("database is not available")
    
    conn = None

    try:
        # get connection from pool
        conn = database.get_connection()

        # check the connection status
        if not PySQLConnection.check_connection(conn):
            PySQLConnection.reconnect(conn)

        # send database connection to callback function
        if args is None:
            return do_action(conn)
        else:
            return do_action(conn, args)

    finally:
        if conn:
            database.put_connection(conn)