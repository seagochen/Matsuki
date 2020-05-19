# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Feb 24, 2020
# Modified: Feb 24, 2020

import threading
import time
from datetime import datetime

from siki.basics import Exceptions as excepts


class ThreadSafeIDCreator(object):

    """
    Create id for database table item.
    """



    def __init__(self, bits=4):
        self.bits = bits
        self.lock = threading.Lock()
        self.lastid = None
        self.lasttime = None




    def _datetime(self):
        return datetime.now().strftime("%Y%m%d%H%M%S")




    def _id_generate(self):
        """
        generate the id in format of YYYYmmDDHHMMSS00000000
        """
        id_strings = ""

        if self.bits <= 12 and self.bits > 0:
            id_strings = self._datetime() + "000000000000000000"[0 : self.bits]
        else:
            raise excepts.ArrayIndexOutOfBoundsException(
                "bits of seed to generate id is out of range")

        return int(id_strings)




    def update_id(self, new_id):
        if type(new_id) is int:
            self.lastid = new_id
        elif type(new_id) is str:
            self.lastid = int(new_id)
        else:
            raise excepts.InvalidParamException("given id must be string or integer")
    



    def generate_id(self):
        """
        generate a new id from given table of database
        @return the id in format of YYYYmmDDHHMMSSXXXX [default type]
        """

        try:
            # lock
            self.lock.acquire()

            if self.lastid is None: # first time calling
                self.lastid = self._id_generate() + 1
                self.lasttime = self._datetime()
                return str(self.lastid)

            if self._datetime() != self.lasttime: # current timestamp is over previous
                self.lastid = self._id_generate() + 1
                self.lasttime = self._datetime()
                return str(self.lastid)

            else: # not exceeding the time
                self.lastid = self.lastid + 1
                return str(self.lastid)

        finally:
            # release the lock
            self.lock.release()