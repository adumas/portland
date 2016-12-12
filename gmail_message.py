#!/usr/local/bin/python
import base64

class Message(object):
    def __init__(self,msg):
        header_parse(self,msg)


    def header_parse(self,msg)
        

    def __base64_url_decode(inp):
        padding_factor = (4 - len(inp) % 4) % 4
        inp += "="*padding_factor
        return base64.b64decode(unicode(inp).translate(dict(zip(map(ord, u'-_'), u'+/'))))
