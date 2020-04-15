# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Apr 09, 2020
# LastChg: Apr 09, 2020

from flask import request, jsonify

from matsuki.argspattern import ArgsUsesRegularExpression
from matsuki.argspattern import ArgsUsesSikiComplianceCheck
from matsuki.tools import FlaskRequestSimplify
from matsuki.MatsukiCode import MatsukiCode, encode
from matsuki.HttpCode import HttpCode, response

from werkzeug.local import LocalProxy

from siki.basics import FileUtils


def siki_verified_args(request: LocalProxy, xmlfile: str):
    """
    expand the parameters from the http request and simplify the process of obtaining the parameters

    @Args:
    * [request] LocalProxy type, the request from flask
    * [xmlfile] str type, the path of siki parameter check

    @Returns:
    * [bool] success or failed
    * [dict(str:obj)] if success return http arguments, or failed with json message returned
    * [dict(str:obj)] not always, {dict: file}
    """

    # simplify the HTTP request
    flask_args = FlaskRequestSimplify.simplify_request(request)

    if flask_args[0] is None: # no variables found
        return False, jsonify(response(HttpCode.CERR_Not_Acceptable, encode(MatsukiCode.OK_GENERAL_FALSE), 
            "you cannot do that!"))
    
    # verify parameters
    if not FileUtils.exists(xmlfile):
        return False, jsonify(response(HttpCode.SERR_Internal_Server_Error, 
            encode(MatsukiCode.OK_GENERAL_FALSE, MatsukiCode.SERV_UNIMPLEMENTED_ERROR),
            "rule file is broken"))

    # update filtered arguments
    args = ArgsUsesSikiComplianceCheck.apply_siki_rules(xmlfile, args)

    # return to caller filtered result
    if flask_args[1]:
        return True, args, flask_args[1]
    
    else:
        return True, args




def regular_verified_args(request: LocalProxy, rulefile: str):
    """
    expand the parameters from the http request and simplify the process of obtaining the parameters

    @Args:
    * [request] LocalProxy type, the request from flask
    * [rulefile] str type, the path of regular parameter check

    @Returns:
    * [bool] success or failed
    * [dict(str:obj)] if success return http arguments, or failed with json message returned
    * [dict(str:obj)] not always, {dict: file}
    """

    # simplify the HTTP request
    flask_args = FlaskRequestSimplify.simplify_request(request)

    if flask_args[0] is None: # no variables found
        return False, jsonify(response(HttpCode.CERR_Not_Acceptable, encode(MatsukiCode.OK_GENERAL_FALSE), 
            "you cannot do that!"))
    
    # verify parameters
    if not FileUtils.exists(rulefile):
        return False, jsonify(response(HttpCode.SERR_Internal_Server_Error, 
            encode(MatsukiCode.OK_GENERAL_FALSE, MatsukiCode.SERV_UNIMPLEMENTED_ERROR),
            "rule file is broken"))

    # update filtered arguments
    args = ArgsUsesRegularExpression.apply_reg_rules(rulefile, flask_args[0])

    # return to caller filtered result
    if flask_args[1]:
        return True, args, flask_args[1]
    
    else:
        return True, args