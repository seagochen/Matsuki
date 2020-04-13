# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Apr 10, 2020
# LastChg: Apr 10, 2020

from flask import jsonify

from matsuki.MatsukiCode import MatsukiCode, encode
from matsuki.HttpCode import HttpCode, response
from matsuki.tools import TokenManager
from matsuki.tools.TokenManager import TOKEN_STATUS

def verify_user_permission(args:dict, secretKey:str):
    """
    verify user access permission

    @Args:
    * [args] dict, contains 'token' word

    @Returns:
    * [bool] success or failed
    * [dict(str:obj)] if success data in token, or failed with json message returned
    """

    if 'token' not in args.keys():
        return False, jsonify(response(HttpCode.CERR_Not_Acceptable, encode(MatsukiCode.TOKEN_SIGNATURE_ERROR), 
            "you cannot do that!")) 

    status, token = TokenManager.verify_auth_token(args['token'], secretKey)
    if status == TOKEN_STATUS.SignatureExpiredError:
        return False, jsonify(response(HttpCode.CERR_Not_Acceptable, encode(MatsukiCode.TOKEN_SIGNATURE_EXPIRED), 
            "token is expired"))

    elif status == TOKEN_STATUS.BadSignatureError:
        return False, jsonify(response(HttpCode.CERR_Not_Acceptable, encode(MatsukiCode.TOKEN_SIGNATURE_ERROR), 
            "token has signature error"))
    
    elif status == TOKEN_STATUS.OtherError:
        return False, jsonify(response(HttpCode.CERR_Not_Acceptable, encode(MatsukiCode.TOKEN_UNKNOWN_ERROR), 
            "token has unknown error"))
    
    return True, token