# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: Apr 07, 2020
# LastChg: Apr 07, 2020

import enum

class Code(enum.IntEnum):

    ##### GENERAL PROCESS ####                                *
    OK_GENERAL_TRUE             = 0x00000001 # 0x0 00 0 0 0 0 1 - logical flow and result ok
    OK_GENERAL_FALSE            = 0x0000000F # 0x0 00 0 0 0 0 F - logical flow correct, but result is incorrect
    OK_GENERAL_NONE             = 0x00000000 # 0x0 00 0 0 0 0 0 - logical flow correct, but no result need to return

    ##### TOKEN VERIFICATION ####                           *
    TOKEN_SIGNATURE_EXPIRED     = 0X00000010 # 0X0 00 0 0 0 1 0 - token signature expired
    TOKEN_SIGNATURE_ERROR       = 0X00000020 # 0X0 00 0 0 0 2 0 - token signature invalid
    TOKEN_UNKNOWN_ERROR         = 0X000000F0 # 0X0 00 0 0 0 F 0 - unexcepted error
    TOKEN_VERIFY_PASSED         = 0X00000000 # 0X0 00 0 0 0 0 0 - token test passed
    
    ##### DATABASE ERRORS ####                            *
    DATABASE_CONNECTION_ERROR   = 0X00000100 # 0X0 00 0 0 1 0 0 - database has connection error
    DATABASE_INVALID_STATEMENT  = 0X00000200 # 0X0 00 0 0 2 0 0 - database statement is invalid
    DATABASE_NO_DATA_FOUND      = 0X00000C00 # 0X0 00 0 0 C 0 0 - database no data was found
    DATABASE_UNKNOWN_ERROR      = 0x00000F00 # 0x0 00 0 0 F 0 0 - database found unknown error
    DATABASE_DATA_FOUND         = 0x00000000 # 0x0 00 0 0 0 0 0 - database ok

    ##### CACHED ERRORS #####                           *
    CACHED_CONNECTION_ERROR     = 0x00001000 # 0x0 00 0 1 0 0 0 - data cached has connection error
    CACHED_INVALID_STATEMENT    = 0x00002000 # 0x0 00 0 2 0 0 0 - data cached statment is invalid
    CACHED_NO_CACHE_FOUND       = 0X00003000 # 0X0 00 0 3 0 0 0 - data cached was not found
    CACHED_NO_RESOURCE_FOUND    = 0X0000C000 # 0X0 00 0 C 0 0 0 - data cached was no available resource found
    CACHED_UNKNOWN_ERROR        = 0x0000F000 # 0x0 00 0 F 0 0 0 - data cached found unknown error
    CACHED_RESOURCE_FOUND       = 0X00000000 # 0X0 00 0 0 0 0 0 - data cached ok

    #### RESERVED STATES ####              *
    #RESERVED_ERROR             = # 0x0 00 0 0 0 0 0 - reserved error

    ##### SERVER ERRORS ####                       **
    SERV_UNEXCEPT_ERROR         = 0X0FF00000 # 0X0 FF 0 0 0 0 0 # server side unexcepted error
    SERV_UNIMPLEMENTED_ERROR    = 0X0F100000 # 0X0 F1 0 0 0 0 0 # unimplemented method error
    SERVER_RAISED_EXCEPTION     = 0X0F200000 # 0X0 F2 0 0 00 0 # server side raised other exceptions
  

def encode(*codes):
    """
    do or-operation for codes
    """

    final_code = 0
    if len(codes) > 0:
        for c in codes:
            final_code = final_code | c
    
    return final_code


def decode(code):
    """
    seperate codes from given code
    """
    general_code    = code & 0x0000000F
    token_code      = (code & 0x000000F0) >> 4
    database_code   = (code & 0x00000F00) >> 8
    cached_code     = (code & 0x0000F000) >> 12
    reserved_code   = (code & 0x000F0000) >> 16
    server_code     = (code & 0x0FF00000) >> 20

    return [server_code, reserved_code, cached_code, database_code, token_code, general_code]


def print_code(codes):
    print("SERV CODE:", '0x%x'%codes[0])
    print("REVS CODE:", '0x%x'%codes[1])
    print("CACH CODE:", '0x%x'%codes[2])
    print("BASE CODE:", '0x%x'%codes[3])
    print("TOKN CODE:", '0x%x'%codes[4])
    print("GENL CODE:", '0x%x'%codes[5])



if __name__ == "__main__":
    from MatsukiCode import MatsukiCode as code
    code = encode(code.SERV_UNEXCEPT_ERROR, code.CACHED_CONNECTION_ERROR, code.DATABASE_CONNECTION_ERROR)
    print_code(decode(code))
