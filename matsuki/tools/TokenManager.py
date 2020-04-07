# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Feb 07, 2020
# LastChg: Apr 07, 2020

import base64
import random
import time
from enum import IntEnum

from itsdangerous import TimedJSONWebSignatureSerializer as serializer
from itsdangerous import SignatureExpired, BadSignature, BadData

from siki.basics import TimeTicker as ticker
from siki.basics import Exceptions as excepts
from siki.basics import Convert as convert
from siki.dstruct import DictExtern
from siki.pysql import SafeSQLCmd

class TOKEN_STATUS(IntEnum):
    
    # token is ok
    OK = 0

    # token is signature expired
    SignatureExpiredError = 1

    # token is bad signature
    BadSignatureError = 2

    # other error
    OtherError = 3


def create_auth_token(secret_key : str, data : dict, expiration = 28800):
    """
    generate security token
    
    Args:
    * [secret_key] the secret key to encode
    * [data] the data which encapsulated to the token 
    * [expiration] out date time in seconds, default 60 x 60 x 8
    
    Returns:
    * [bytes] authorized token
    """
    security = serializer(
        secret_key=secret_key,
        expires_in=expiration
    )

    timestamp = ticker.time_since1970()
    iat = {"iat": timestamp}

    if data is None:
        return security.dumps(iat)
    else:
        ext = DictExtern.union(data, iat)
        return security.dumps(ext)


    


def verify_auth_token(token : bytes, secret_key : str):
    """
    verify security token

    Args:
    * [token] the web token
    * [secret_key] the secret key to decode
    
    Returns:
    * [tunple(int, dict)] deserialized contains data in dict
    """
    security = serializer(
        secret_key=secret_key
    )

    # try to decode
    data = None
    try:
        data = security.loads(token)
        # token decode if failed, because time expired
    except SignatureExpired:
        #log.warning("TokenManager", "remote token expired", remoteip)
        return TOKEN_STATUS.SignatureExpiredError, None
    except BadSignature:
        #log.warning("TokenManager", "remote token has bad signature", remoteip)
        return TOKEN_STATUS.BadSignatureError, None
    except:
        #log.warning("TokenManager", "unkonw exception", remoteip)
        return TOKEN_STATUS.OtherError, None

    return TOKEN_STATUS.OK, data