# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Apr 09, 2020
# Modified: Apr 24, 2020

from flask import request, jsonify

from matsuki.argspattern import ArgsUsesRegularExpression
from matsuki.argspattern import ArgsUsesSikiComplianceCheck
from matsuki.tools import FlaskRequestSimplify

from werkzeug.local import LocalProxy

from siki.basics import FileUtils


def siki_verified_args(request: LocalProxy, xml: object, fromFile=True):
    """
    expand the parameters from the http request and simplify the process of obtaining the parameters

    @Args:
    * [request] LocalProxy type, the request from flask
    * [xml] str type, the path of siki-style xml file, or string
    * [fromFile] default is true, means xml source comes from file, set to false, could read configurations from xml string

    @Returns:
    * [bool] success or failed
    * [dict(str:obj)] if success return http arguments, or failed with json message returned
    * [dict(str:obj)] not always, {dict: file}
    """

    # simplify the HTTP request
    flask_args = FlaskRequestSimplify.simplify_request(request)

    if flask_args[0] is None:  # no variables found
        return False, "flask arguments are none", None

    # verify parameters
    if fromFile and not FileUtils.exists(xml):
        return False, "rule file is broken", None

    # update filtered arguments
    args = ArgsUsesSikiComplianceCheck.apply_siki_rules(xml, flask_args[0], fromFile)

    if len(args) <= 0:
        return False, "no arguments passed the check", None

    # return to caller filtered result
    if flask_args[1]:
        return True, args, flask_args[1]

    else:
        return True, args, None


def regular_verified_args(request: LocalProxy, rule: str):
    """
    expand the parameters from the http request and simplify the process of obtaining the parameters

    @Args:
    * [request] LocalProxy type, the request from flask
    * [rule] str type, the path of regular check file, or lists of regular expressions
    * [fromFile] default is true, means source comes from a file, set to false, could read configurations from list

    @Returns:
    * [bool] success or failed
    * [dict(str:obj)] if success return http arguments, or failed with json message returned
    * [dict(str:obj)] not always, {dict: file}
    """

    # simplify the HTTP request
    flask_args = FlaskRequestSimplify.simplify_request(request)

    if flask_args[0] is None:  # no variables found
        return False, "flask arguments are none", None

    # verify parameters
    if not rule or not FileUtils.exists(rule):
        return False, "rule file is broken", None

    # update filtered arguments
    args = ArgsUsesRegularExpression.apply_reg_rules(rule, flask_args[0])

    if len(args) <= 0:
        return False, "no arguments passed the check", None

    # return to caller filtered result
    if flask_args[1]:
        return True, args, flask_args[1]

    else:
        return True, args, None
