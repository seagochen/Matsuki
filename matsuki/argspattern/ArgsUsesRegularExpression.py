# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Feb 07, 2020
# LastChg: Apr 07, 2020

import re
from siki.basics import FileUtils
from siki.basics import Exceptions
from siki.basics import Convert


def use_args_regular_check(regDict: dict, args: dict):

    finalDict = {}

    # first, verify keys from second variable are matches to first variable
    for key in args.keys():
        if key not in args.keys():
            raise Exceptions.NoAvailableResourcesFoundException("key: {} in args not matched to regDict".format(key))

        # regular check
        if re.match(regDict[key], args[key]) is not None:
            finalDict[key] = args[key]
        else:
            finalDict[key] = None

    # return to caller
    return finalDict


def trim_tailer_from_text(text:str):
    if text[-2] == '\r':
        text = text.replace("\r\n", "")
    else:
        text = text.replace("\n", "")
    
    return text



def apply_reg_exp(rulefile: str, args: dict):
    """
    the format of rulefile:
    [keyname] [regexpress]

    @Args:
    * [rulefile] str, path of file
    * [args] dict, data contained with key and value

    @Returns:
    * [dict(str:obj)] dict type
    """

    if not FileUtils.exists(rulefile):
        raise Exceptions.NoAvailableResourcesFoundException("file: {} not found".format(rulefile))

    # rules dict
    rules = {}

    # read lines in file
    for line in open(rulefile, "rt"):
        # trim tailer
        line = trim_tailer_from_text(line)

        # split token from spaces
        seps = line.split(' ')
        
        # check size
        if len(seps) < 2 or len(seps) >= 3:
            raise Exceptions.InvalidArithException("regular line: {} is broken".format(line))

        # append rules to dict
        rules[seps[0]] = R"{}".format(seps[1])

    return use_args_regular_check(rules, args)



if __name__ == "__main__":
    args0 = {
        "key1": "seago@seagosoft.com",
        "key2": "0851-123456789",
        "key3": "root/foo/bar.txt"
    }

    print(apply_reg_exp("./rule.txt", args0))

    args1 = {
        "key1": "_seago^seagosoft.com",
        "key2": "0851-123456789a",
        "key3": "root_foo_bar"
    }

    print(apply_reg_exp("./rule.txt", args1))