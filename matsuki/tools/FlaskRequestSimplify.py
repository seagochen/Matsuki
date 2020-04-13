# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Create: Sep 19, 2018
# Modifi: Apr 10, 2020

from flask import request

from siki.basics.Hashcode import md5

from werkzeug.local import LocalProxy


def get_request_params(request: LocalProxy):
    """
    get parameters from request
    
    @Args:
    * [request] werkzeug.local.LocalProxy, the flask request
    """

    params = {}

    # adding request method
    if request.method == 'POST':
        params['http_request'] = 'POST'
    elif request.method == 'GET':
        params['http_request'] = 'GET'
    elif request.method == 'HEAD':
        params['http_request'] = 'HEAD'
    elif request.method == 'PUT':
        params['http_request'] = 'PUT'
    elif request.method == 'DELETE':
        params['http_request'] = 'DELETE'
    elif request.method == 'TRACE':
        params['http_request'] = 'TRACE'
    elif request.method == 'CONNECT':
        params['http_request'] = 'CONNECT'
    else:
        params['http_request'] = 'UNKNOW'
        return params

    # adding request parameters
    if len(request.args) > 0:
        get_args = {}
        for key, val in request.args.items():
            get_args[key] = val
        params['args'] = get_args
    else:
        params['args'] = None
    
    if len(request.form) > 0:
        form_args = {}
        for key, val in request.form.items():
            form_args[key] = val
        params['form'] = form_args
    else:
        params['form'] = None

    # adding files to redis
    if len(request.files) > 0:
        params['files'] = request.files
    else:
        params['files'] = None

    return params



def get_remote_ip(request: LocalProxy):
    """
    get remote ip from request

    @Args:
    * [request] werkzeug.local.LocalProxy, the flask request
    """
    return request.remote_addr



def simplify_request(request: LocalProxy):
    """
    to simplify the flask request
    
    @Args:
    * [request] request handler of flask framework
    
    @Returns:
    * [tuple(dict, dict)] request parameters are simplified to a python tuple type, first one is args, second one is files
    """
    # simplify GET/POST request
    args = None
    files = None
    params = get_request_params(request)
    
    # simpilify the POST args
    if 'POST' == params['http_request']:
        if params['form'] is None and params['args'] is not None:
            args = params['args']
        else:
            args = params['form']

    # simpilify the GET args
    if 'GET' == params['http_request']:
        args = params['args']
    
    if params['files']:
        files = params['files']

    # return
    return args, files
