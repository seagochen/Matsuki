# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Feb 07, 2020
# LastChg: Apr 07, 2020

from siki.basics import Exceptions as excepts
from siki.basics import Convert as convert
from siki.interfaces.ApplyingXMLRules import ApplyingXMLRules as ApplyingXML


def apply_siki_rules(xml: str, args: dict, fromFile = True):
    """
    applying siki defined compliance check rules, to prevent some illegal invadation.
    such as sql injection, etc.

    @Args:
    * [xml] xml file path
    * [args] simplied http request
    * [fromFile] default is true, set false could read configuration from xml string
    
    @Returns:
    * [dict(str:obj)] dict type
    """
    # load mapping rules from xml file
    parser = ApplyingXML(xml, fromFile)

    # mapping the parameters
    return parser.convert(args)