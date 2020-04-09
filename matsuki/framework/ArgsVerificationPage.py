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

from siki.basics import Exceptions
from siki.basics import FileUtils


def siki_verified_page(request: LocalProxy, xmlfile: str, fn = __file__):
    """
    simplified the http request, and the routine of some blocks of web server

    @Args:
    * [request] LocalProxy type, the request from flask
    * [xmlfile] str type, the path of siki parameter check
    * [fn] str type, the filename

    @Returns:
    * [dict(str:obj)]
    """

    # simplify the HTTP request
    args = FlaskRequestSimplify.simplify_request(request)

    if args is None: # no variables found
        return jsonify(response(HttpCode.CERR_Not_Acceptable, encode(MatsukiCode.OK_GENERAL_FALSE), 
            "you cannot do that!"))
    
    # verify parameters
    if not FileUtils.exists(xmlfile):
        return jsonify(response(HttpCode.SERR_Internal_Server_Error, 
            encode(MatsukiCode.OK_GENERAL_FALSE, MatsukiCode.SERV_UNIMPLEMENTED_ERROR),
            "rule file is broken"))

    # return to caller filtered result
    return ArgsUsesSikiComplianceCheck.apply_siki_rules(xmlfile, args)




def regular_verified_page(request: LocalProxy, rulefile: str, fn = __file__):
    """
    simplified the http request, and the routine of some blocks of web server

    @Args:
    * [request] LocalProxy type, the request from flask
    * [rulefile] str type, the path of regular parameter check
    * [fn] str type, the filename

    @Returns:
    * [dict(str:obj)]
    """

    # simplify the HTTP request
    args = FlaskRequestSimplify.simplify_request(request)

    if args is None: # no variables found
        return jsonify(response(HttpCode.CERR_Not_Acceptable, encode(MatsukiCode.OK_GENERAL_FALSE), 
            "you cannot do that!"))
    
    # verify parameters
    if not FileUtils.exists(rulefile):
        return jsonify(response(HttpCode.SERR_Internal_Server_Error, 
            encode(MatsukiCode.OK_GENERAL_FALSE, MatsukiCode.SERV_UNIMPLEMENTED_ERROR),
            "rule file is broken"))

    # return to caller filtered result
    return ArgsUsesRegularExpression.apply_reg_exp(rulefile, args)