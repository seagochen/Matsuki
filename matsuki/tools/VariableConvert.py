# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Apr 15, 2020
# LastChg: Apr 15, 2020

from siki.basics import Convert
from siki.basics import Validators


def http_args_to_py_objs(args: dict):
    """
    convert http parameters to python primary types
    """

    convt_dict = {}
    for key, val in args.items():
        if Validators.check_number(val):
            convt_dict[key] = int(val)
            continue
        
        if Validators.check_float(val):
            convt_dict[key] = float(val)
            continue

        convt_dict[key] = val            

    return convt_dict



def py_objs_to_str_args(pyobj: dict):
    """
    convert python primary types to string-type parameters
    """

    convt_dict = {}
    for key, val in pyobj.items():
        convt_dict[key] = str(val)

    return convt_dict