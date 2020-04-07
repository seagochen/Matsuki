# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Feb 07, 2020
# LastChg: Apr 07, 2020

import re


def apply_reg_exp(pattern: str, arg: str):
    """
    applying siki defined compliance check rules, to prevent some illegal invadation.
    such as sql injection, etc.

    @Args:
    * [pattern] regular expression
    * [arg] simplied http request
    
    @Returns:
    * [str/None] return str itself if correct, else is none
    """
    
    if re.match(pattern, arg):
        return arg
    
    else:
        return None