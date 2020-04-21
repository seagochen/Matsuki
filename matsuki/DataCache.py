# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Apr 21, 2020
# LastChg: Apr 21, 2020

from matsuki.pysql import PySafeSQLCmd

def create_cache(conn, db, table, select_con = None, where_con = None):
    """
    create a cache from database
    """
    rows = PySafeSQLCmd.safe_simple_query(conn, db, table, select_con, where_con)

    if isinstance(rows, dict):
        rows = [rows]
    
    if not rows:
        return []
    
    return rows



def cache_search(cache: list, key: str, val: str):
    """
    search a key with value in the given cache

    @Args:
    * [cache] the cache list, which probably comes from database or redis-like cache
    * [key] the key contains in every row of cache
    * [val] the value that matches to the given val
    """
    if cache and isinstance(cache, list):
        if key not in cache[0].keys():
            return None

        for row in cache:
            if row[key] == val: # found the item
                return row

    return None

