# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Feb 07, 2020
# LastChg: Apr 07, 2020

from siki.basics import Exceptions as excepts
from siki.basics import Convert as convert
from siki.interfaces.ApplyingXMLRules import ApplyingXMLRules as ApplyingXML


def apply_siki_rules(xml_file: str, args: dict):
    """
    applying siki defined compliance check rules, to prevent some illegal invadation.
    such as sql injection, etc.

    @Args:
    * [xml] xml file path
    * [args] simplied http request
    
    @Returns:
    * [dict(str:obj)] dict type
    """
    try:
        # load mapping rules from xml file
        parser = ApplyingXML(xml)

        # mapping the parameters
        arg_dict = parser.convert(args)
        for key, val in arg_dict.items():

            if type(val) is int:
                arg_dict[key] = str(val)

            elif type(val) is float:
                arg_dict[key] = str(val)

            elif type(val) is dict:
                arg_dict[key] = convert.dict_to_string(val)

            elif type(val) is list:
                arg_dict[key] = convert.list_to_string(val)

            elif type(val) is bytes:
                arg_dict[key] = convert.binary_to_string(val)

            else:
                arg_dict[key] = val

        # return to caller
        return arg_dict

    except Exception as e:
        raise excepts.NoAvailableResourcesFoundException("error occurs")