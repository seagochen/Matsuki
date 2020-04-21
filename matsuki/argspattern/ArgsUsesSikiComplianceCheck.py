# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Feb 07, 2020
# LastChg: Apr 07, 2020

from siki.basics import Exceptions as excepts
from siki.basics import Convert as convert
from siki.interfaces.ApplyingXMLRules import ApplyingXMLRules as ApplyingXML


def apply_siki_rules(xmlfile: str, args: dict):
    """
    applying siki defined compliance check rules, to prevent some illegal invadation.
    such as sql injection, etc.

    @Args:
    * [xmlfile] xml file path
    * [args] simplied http request
    
    @Returns:
    * [dict(str:obj)] dict type
    """
    # load mapping rules from xml file
    parser = ApplyingXML(xmlfile)

    # mapping the parameters
    return parser.convert(args)