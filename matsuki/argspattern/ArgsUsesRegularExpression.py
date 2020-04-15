# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Feb 07, 2020
# LastChg: Apr 15, 2020

import re
from siki.basics import FileUtils
from siki.basics import Exceptions
from siki.basics import Convert

class RegularToken(object):

    def __init__(self, key: str, mapping: str, regular: str):
        self.key = key
        self.mapping = mapping
        self.regular = regular



class ArgsMappingToken(object):
    """
    The token used to store the parsed data, including the key of the key-value pair, the mapped key, and the regular matching rules
    """

    def __init__(self):
        self.tokens = []

    
    def trim_tailer_from_text(self, text: str):
        """
        Windows and Linux systems have different line endings. These special symbols may cause regular matching to fail, so need to remove them all
        """
        if text[-2] == '\r':
            text = text.replace("\r\n", "")
        else:
            text = text.replace("\n", "")
        
        return text


    def search_token(self, key):
        """
        from token list, search the matched token
        """

        for t in self.tokens:
            if t.key == key:
                return t
            
        return None


    
    def use_args_regular_check(self, tokenList: list, args: dict):
        """
        Regularly match the parameters, if the format is correct, the data of the parameter will be retained, if it is wrong, it will be discarded
        """

        finalDict = {}

        # first, verify keys from second variable are matches to first variable
        for key, val in args.items():
            token = self.search_token(key)

            if not token:
                raise Exceptions.NoAvailableResourcesFoundException("key: {} in args not matched to token list".format(key))

            # do regular check
            if re.match(token.regular, val) is not None:
                finalDict[token.mapping] = val
            else:
                finalDict[token.mapping] = None

        # return to caller
        return finalDict


    
    def clear_tokens(self):
        """
        cleaning up data caches
        """
        self.tokens.clear()

    

    def parsing_reg_file(self, ruleFile: str, args: dict):
        """
        Parse the configuration file, and then verify the validity of the input parameters

        the format of rulefile:
        [argument key] [mapping key] [regular expression]

        @Args:
        * [ruleFile] str, path of file
        * [args] dict, data contained with key and value

        @Returns:
        * [dict(str:obj)] dict type
        """

        if not FileUtils.exists(rulefile):
            raise Exceptions.NoAvailableResourcesFoundException("file: {} not found".format(rulefile))

        # parse the file
        for line in open(rulefile, "rt"):
            # trim tailer
            line = self.trim_tailer_from_text(line)

            # split token from spaces
            seps = line.split(' ')
            
            # check size
            if len(seps) != 3:
                raise Exceptions.InvalidArithException("regular line: {} is broken, [argument key] [mapping key] [regular expression]".format(line))

            # append regular token to list
            self.tokens.append(RegularToken(seps[0], seps[1], R"{}".format(seps[2])))

        # After parsing the file, first extract the dictionary consisting of {old key-regular match} from the file, 
        # and then perform regular filtering on the parameters
        filtered_args = self.use_args_regular_check(self.tokens, args)

        return filtered_args


    def parsing_reg_rules(self, ruleList: list, args: dict):
        """
        Parse the configuration list, and then verify the validity of the input parameters

        the format of rule list:
        [argument key] [mapping key] [regular expression]

        @Args:
        * [ruleList] list
        * [args] dict, data contained with key and value

        @Returns:
        * [dict(str:obj)] dict type
        """

        # parse the file
        for line in ruleList:
            # split token from spaces
            seps = line.split(' ')
            
            # check size
            if len(seps) != 3:
                raise Exceptions.InvalidArithException("regular line: {} is broken, [argument key] [mapping key] [regular expression]".format(line))

            # append regular token to list
            self.tokens.append(RegularToken(seps[0], seps[1], seps[2]))

        # After parsing the file, first extract the dictionary consisting of {old key-regular match} from the file, 
        # and then perform regular filtering on the parameters
        filtered_args = self.use_args_regular_check(self.tokens, args)

        return filtered_args        



if __name__ == "__main__":
    args0 = {
        "key1": "seago@seagosoft.com",
        "key2": "0851-123456789",
        "key3": "123456789"
    }

    rules = [
        r"key1 to_key1 ^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$", # email
        r"key2 to_key2 ^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$", # phone
        r"key3 to_key3 ^[0-9]+$" # numbers
    ]

    amt = ArgsMappingToken()

    print(amt.parsing_reg_rules(rules, args0))

    args1 = {
        "key1": "_seago^seagosoft.com",
        "key2": "0851-123456789a",
        "key3": "123456789a"
    }

    print(amt.parsing_reg_rules(rules, args1))