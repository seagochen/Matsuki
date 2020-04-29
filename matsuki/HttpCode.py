# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Create: Sep 22, 2018
# Modifi: Oct 02, 2018

from enum import IntEnum

from siki.basics import Convert

class Code(IntEnum):

    '''2xx Success'''

    # Standard response for successful HTTP requests. 
    # The actual response will depend on the request method used. 
    # In a GET request, the response will contain an entity 
    # corresponding to the requested resource. 
    # In a POST request, the response will contain an 
    # entity describing or containing the result of the action.    
    OK_General = 200 

    # The request has been fulfilled, resulting in the 
    # creation of a new resource.
    OK_Created = 201

    # The request has been accepted for processing, 
    # but the processing has not been completed. 
    # The request might or might not be eventually acted upon, 
    # and may be disallowed when processing occurs.
    OK_Accepted = 202

    # The server is a transforming proxy (e.g. a Web accelerator) that
    # received a 200 OK from its origin,
    # but is returning a modified version of the origin's response.
    OK_Non_Authoritative_Information = 203

    # The server successfully processed the request 
    # and is not returning any content.
    OK_No_Content = 204

    # The server successfully processed the request, 
    # but is not returning any content. Unlike a 204 response, 
    # this response requires that the requester reset the document view.
    OK_Reset_Content = 205

    # The server is delivering only part of the resource (byte serving) 
    # due to a range header sent by the client. 
    # The range header is used by HTTP clients to enable resuming of 
    # interrupted downloads, or split a download into multiple 
    # simultaneous streams.
    OK_Partial_Content = 206

    # The message body that follows is by default an XML message 
    # and can contain a number of separate response codes, 
    # depending on how many sub-requests were made.
    OK_Multi_Status = 207

    # The members of a DAV binding have already been enumerated 
    # in a preceding part of the (multistatus) response, and are 
    # not being included again.
    OK_Already_Reported = 208

    # The server has fulfilled a request for the resource, 
    # and the response is a representation of the result 
    # of one or more instance-manipulations applied to 
    # the current instance.
    OK_IM_Used = 226

    '''3xx Redirection'''

    # Indicates multiple options for the resource from which the 
    # client may choose (via agent-driven content negotiation). 
    # For example, this code could be used to present multiple 
    # video format options, to list files with different filename 
    # extensions, or to suggest word-sense disambiguation.
    REDIREC_Multiple_Choices = 300

    # This and all future requests should be directed to the given URI.
    REDIREC_Moved_Permanently = 301

    # Tells the client to look at (browse to) another url. 
    # 302 has been superseded by 303 and 307. This is an example of 
    # industry practice contradicting the standard. The HTTP/1.0 
    # specification (RFC 1945) required the client to perform a 
    # temporary redirect (the original describing phrase was 
    # "Moved Temporarily"), but popular browsers implemented 
    # 302 with the functionality of a 303 See Other.
    # Therefore, HTTP/1.1 added status codes 303 and 307 to distinguish 
    # between the two behaviours. However, some Web applications 
    # and frameworks use the 302 status code as if it were the 303.
    REDIREC_Found = 302

    # The response to the request can be found under another URI 
    # using the GET method. When received in response to a POST (or PUT/DELETE), 
    # the client should presume that the server has received the 
    # data and should issue a new GET request to the given URI.
    REDIREC_See_Other = 303

    # Indicates that the resource has not been modified since the version 
    # specified by the request headers If-Modified-Since or If-None-Match. 
    # In such case, there is no need to retransmit the resource since 
    # the client still has a previously-downloaded copy.
    REDIREC_Not_Modified = 304

    # The requested resource is available only through a proxy, 
    # the address for which is provided in the response. 
    # Many HTTP clients (such as Mozilla and Internet Explorer) 
    # do not correctly handle responses with this status code, 
    # primarily for security reasons.
    REDIREC_Use_Proxy = 305

    # No longer used. Originally meant "Subsequent requests should use 
    # the specified proxy."
    REDIREC_Switch_Proxy = 306

    # In this case, the request should be repeated with another URI; 
    # however, future requests should still use the original URI. 
    # In contrast to how 302 was historically implemented, 
    # the request method is not allowed to be changed when reissuing the 
    # original request. For example, a POST request should be repeated 
    # using another POST request.
    REDIREC_Temporary_Redirect = 307

    # The request and all future requests should be repeated using 
    # another URI. 307 and 308 parallel the behaviors of 302 and 301, 
    # but do not allow the HTTP method to change. So, for example, 
    # submitting a form to a permanently redirected resource may 
    # continue smoothly.
    REDIREC_Permanent_Redirect = 308

    '''4xx Client errors'''

    # The server cannot or will not process the request due to an apparent 
    # client error (e.g., malformed request syntax, size too large, 
    # invalid request message framing, or deceptive request routing).
    CERR_Bad_Request = 400

    # Similar to 403 Forbidden, but specifically for use when authentication
    # is required and has failed or has not yet been provided. 
    # The response must include a WWW-Authenticate header field 
    # containing a challenge applicable to the requested resource. 
    # See Basic access authentication and Digest access authentication.
    # 401 semantically means "unauthenticated", i.e. the user does not
    # have the necessary credentials.
    # Note: Some sites incorrectly issue HTTP 401 when an IP address is 
    # banned from the website (usually the website domain) and that 
    # specific address is refused permission to access a website.
    CERR_Unauthorized = 401

    # Reserved for future use. The original intention was that this code 
    # might be used as part of some form of digital cash or micropayment 
    # scheme, as proposed for example by GNU Taler, but that has not 
    # yet happened, and this code is not usually used. Google Developers 
    # API uses this status if a particular developer has exceeded the daily 
    # limit on requests. Sipgate uses this code if an account does not 
    # have sufficient funds to start a call. Shopify uses this code 
    # when the store has not paid their fees and is temporarily disabled.
    CERR_Payment_Required = 402

    # The request was valid, but the server is refusing action. 
    # The user might not have the necessary permissions for a resource, 
    # or may need an account of some sort.
    CERR_Forbidden = 403

    # The requested resource could not be found but may be available in 
    # the future. Subsequent requests by the client are permissible.
    CERR_Not_Found = 404

    # A request method is not supported for the requested resource; 
    # for example, a GET request on a form that requires data to be 
    # presented via POST, or a PUT request on a read-only resource.
    CERR_Method_Not_Allowed = 405

    # The requested resource is capable of generating only content 
    # not acceptable according to the Accept headers sent in the request. 
    # See Content negotiation.
    CERR_Not_Acceptable = 406

    # The client must first authenticate itself with the proxy.
    CERR_Proxy_Authentication_Required = 407

    # The server timed out waiting for the request. According to HTTP 
    # specifications: "The client did not produce a request within the 
    # time that the server was prepared to wait. The client MAY repeat 
    # the request without modifications at any later time."
    CERR_Request_Timeout = 408

    # Indicates that the request could not be processed because of 
    # conflict in the current state of the resource, such as an edit 
    # conflict between multiple simultaneous updates.
    CERR_Conflict = 409

    # Indicates that the resource requested is no longer available and 
    # will not be available again. This should be used when a resource 
    # has been intentionally removed and the resource should be purged. 
    # Upon receiving a 410 status code, the client should not request 
    # the resource in the future. Clients such as search engines 
    # should remove the resource from their indices. Most use cases do 
    # not require clients and search engines to purge the resource, 
    # and a "404 Not Found" may be used instead.
    CERR_Gone = 410

    # The request did not specify the length of its content, which is 
    # required by the requested resource.
    CERR_Length_Required = 411

    # The server does not meet one of the preconditions that the requester
    # put on the request.
    CERR_Precondition_Failed = 412

    # The request is larger than the server is willing or able to process. 
    # Previously called "Request Entity Too Large".
    CERR_Payload_Too_Large = 413

    # The URI provided was too long for the server to process. 
    # Often the result of too much data being encoded as a query-string 
    # of a GET request, in which case it should be converted to a POST 
    # request. Called "Request-URI Too Long" previously.
    CERR_URI_Too_Long = 414

    # The request entity has a media type which the server or resource 
    # does not support. For example, the client uploads an image as 
    # image/svg+xml, but the server requires that images use a different 
    # format.
    CERR_Unsupported_Media_Type = 415

    # The client has asked for a portion of the file (byte serving), 
    # but the server cannot supply that portion. For example, if the 
    # client asked for a part of the file that lies beyond the end of 
    # the file. Called "Requested Range Not Satisfiable" previously.
    CERR_Range_Not_Satisfiable = 416

    # The server cannot meet the requirements of the Expect request-header 
    # field.
    CERR_Expectation_Failed = 417

    # This code was defined in 1998 as one of the traditional IETF 
    # April Fools' jokes, in RFC 2324, Hyper Text Coffee Pot Control 
    # Protocol, and is not expected to be implemented by actual HTTP 
    # servers. The RFC specifies this code should be returned by teapots 
    # requested to brew coffee. This HTTP status is used as an 
    # Easter egg in some websites, including Google.com.
    CERR_IM_A_Teapot = 418

    # The request was directed at a server that is not able to produce 
    # a response (for example because of connection reuse).
    CERR_Misdirected_Request = 421

    # The request was well-formed but was unable to be followed due to 
    # semantic errors.
    CERR_Unprocessable_Entity = 422

    # The resource that is being accessed is locked.
    CERR_Locked = 423

    # The request failed because it depended on another request and that 
    # request failed (e.g., a PROPPATCH).
    CERR_Failed_Dependency = 424  

    # The client should switch to a different protocol such as TLS/1.0, 
    # given in the Upgrade header field.
    CERR_Upgrade_Required = 426

    # The origin server requires the request to be conditional. 
    # Intended to prevent the 'lost update' problem, where a client
    # GETs a resource's state, modifies it, and PUTs it back to the 
    # server, when meanwhile a third party has modified the state on 
    # the server, leading to a conflict."
    CERR_Precondition_Required = 428 

    # The user has sent too many requests in a given amount of time. 
    # Intended for use with rate-limiting schemes.
    CERR_Too_Many_Requests = 429

    # The server is unwilling to process the request because either
    # an individual header field, or all the header fields collectively, 
    # are too large.
    CERR_Request_Header_Fields_Too_Large = 431

    # A server operator has received a legal demand to deny access to a 
    # resource or to a set of resources that includes the requested 
    # resource. The code 451 was chosen as a reference to the novel 
    # Fahrenheit 451 (see the Acknowledgements in the RFC).
    CERR_Unavailable_For_Legal_Reasons = 451

    '''5xx Server errors'''

    # A generic error message, given when an unexpected condition 
    # was encountered and no more specific message is suitable.
    SERR_Internal_Server_Error = 500

    # The server either does not recognize the request method, 
    # or it lacks the ability to fulfil the request. Usually this 
    # implies future availability (e.g., a new feature of a web-service API).
    SERR_Not_Implemented = 501

    # The server was acting as a gateway or proxy and received an 
    # invalid response from the upstream server.
    SERR_Bad_Gateway = 502

    # The server is currently unavailable (because it is overloaded or 
    # down for maintenance). Generally, this is a temporary state.
    SERR_Service_Unavailable = 503

    # The server was acting as a gateway or proxy and did not receive a
    # timely response from the upstream server.
    SERR_Gateway_Timeout = 504

    # The server does not support the HTTP protocol version used in the request.
    SERR_HTTP_Version_Not_Supported = 505

    # Transparent content negotiation for the request results in a 
    # circular reference.
    SERR_Variant_Also_Negotiates = 506

    # The server is unable to store the representation needed to 
    # complete the request.
    SERR_Insufficient_Storage = 507

    # The server detected an infinite loop while processing the 
    # request (sent in lieu of 208 Already Reported).
    SERR_Loop_Detected = 508
    
    # Further extensions to the request are required for the server 
    # to fulfill it.
    SERR_Not_Extended = 510

    # The client needs to authenticate to gain network access. 
    # Intended for use by intercepting proxies used to control access 
    # to the network (e.g., "captive portals" used to require agreement 
    # to Terms of Service before granting full Internet access via a Wi-Fi 
    # hotspot).
    SERR_Network_Authentication_Required = 511



def response(httpcode, matsukicode,  msg = None, data = None):
    res = {}

    # convert enum to int
    res['http'] = int(httpcode)
    res['code']   = int(matsukicode) 

    # convert msg if necessary
    if msg is not None:
        if isinstance(msg, bytes):
            res['feedback'] = Convert.binary_to_string(msg)
        elif isinstance(msg, list):
            res['feedback'] = Convert.list_to_string(msg)
        elif isinstance(msg, dict):
            res['feedback'] = Convert.dict_to_string(msg)
        else:
            res['feedback'] = str(msg)
    
    # convert data if necessary
    if data is not None:
        if isinstance(data, bytes):
            res['data'] = Convert.binary_to_string(data)
        elif isinstance(data, list):
            res['data'] = Convert.list_to_string(data)
        elif isinstance(data, dict):
            res['data'] = Convert.dict_to_string(data)
        else:
            res['data'] = str(data)

    # return to caller
    return res