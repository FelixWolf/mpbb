from flask import request, abort, Response
from html import escape
import pprint
import json
from uuid import UUID
import datetime
import time
import xml.etree.ElementTree as ET
import base64
import struct

def determinePreferredFormat(input, findFull=False):
    input = input.split(",")
    results = []
    for value in input:
        values = value.split(";")
        mediatype = values.pop(0)
        preference = 1
        for prop in values:
            tmp = prop.split("=")
            if tmp[0].strip() == "q" and len(tmp) == 2:
                preference = float(tmp[1].strip())
            else:
                mediatype = mediatype + ";" + prop.strip()
        
        results.append((mediatype.strip(), preference))
    
    bestPreference = 0
    bestType = "*/*"
    bestIsAmbiguous = True
    for result in results:
        isAmbiguous = result[0].split(";", 1)[0].endswith("/*")
        #Is the result better than preference or equal to an ambiguous result?
        if result[1] > bestPreference or (result[1] >= bestPreference and bestIsAmbiguous):
            #Are we searching for a fullest result?
            if findFull and isAmbiguous:
                continue
            bestType = result[0]
            bestIsAmbiguous = isAmbiguous
            bestPreference = result[1]
    
    return bestType

supportedMimes = {}
def registerMime(mimes):
    def wrapper(func, mimes):
        if mimes == str:
            mimes = [mimes]
        
        for mime in mimes:
            supportedMimes[mime] = func
        return func
    return lambda func: wrapper(func, mimes)

# HTML DUMPER
def dumpHTML(input, noWrapper=False):
    result = pprint.pformat(input, indent=4, width=80)
    if noWrapper:
        return result
    
    return """<!DOCTYPE html><html><head><title>Data Dump</title>
<link href="https://fonts.googleapis.com/css?family=Source+Code+Pro" rel="stylesheet">
<style>body{font-family:'Source Code Pro',monospace;white-space:pre;}</style>
</head><body>"""+escape(result)+"</body></html>"

@registerMime(["text/plain"])
def dumpHTMLPlain(input):
    return dumpHTML(input, True)

@registerMime(["text/html"])
def dumpHTMLFormatted(input):
    return dumpHTML(input, False)

# JSON DUMPER
class jsonPythonTypes(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, complex):
            return [obj.real, obj.imag]
        elif isinstance(obj, UUID):
            return str(obj)
        elif isinstance(obj, datetime.datetime):
            return obj.timestamp()
        elif isinstance(obj, datetime.date):
            return [obj.year, obj.month, obj.day]
        
        try:
            return json.JSONEncoder.default(self, obj)
        except TypeError:
            return repr(obj)

@registerMime(["application/json"])
def dumpJSON(input):
    return json.dumps(input, cls=jsonPythonTypes)

# XML DUMPER
@registerMime(["text/xml", "application/xml"])
def dumpXML(input, root=None):
    result = None
    if type(input) == dict:
        result = ET.Element("dict")
        for key in input:
            elm = dumpXML(input[key], result)
            elm.set("name", str(key))
            result.append(elm)
    
    elif type(input) == list:
        result = ET.Element("list")
        for value in input:
            elm = dumpXML(value, result)
            result.append(elm)
    
    elif type(input) == str:
        result = ET.Element("string")
        result.text = input
    
    elif type(input) == int:
        result = ET.Element("integer")
        result.text = str(input)
    
    elif type(input) == float:
        result = ET.Element("float")
        result.text = str(input)
    
    elif type(input) == UUID:
        result = ET.Element("uuid")
        result.text = str(input)
    
    elif type(input) == datetime.date:
        result = ET.Element("uuid")
        result.text = str("{}-{}-{}".format(input.year, input.month, input.day))
    
    elif type(input) == datetime.datetime:
        result = ET.Element("timestamp")
        result.text = str(input.timestamp())
    
    elif input == None:
        result = ET.Element("undef")
    
    elif type(input) == bool:
        result = ET.Element("bool")
        result.text = "true" if True else "false"
    
    else:
        result = ET.Element("unsupported")
        result.text = repr(input)
    
    if root == None:
        root = ET.Element("data")
        root.append(result)
        return ET.tostring(root)
    
    return result


# LLSD DUMPER
@registerMime(["application/llsd+xml"])
def dumpLLSD(input, root=None):
    result = None
    if type(input) == dict:
        result = ET.Element("map")
        for key in input:
            elm = dumpLLSD(input[key], result)
            if elm != None:
                mkey = ET.Element("key")
                mkey.text = str(key)
                result.append(mkey)
                
                result.append(elm)
    
    elif type(input) == list:
        result = ET.Element("array")
        for value in input:
            elm = dumpLLSD(value, result)
            if elm != None:
                result.append(elm)
    
    elif type(input) == str:
        result = ET.Element("string")
        result.text = input
    
    elif type(input) == bool:
        result = ET.Element("boolean")
        result.text = "true" if True else "false"
    
    elif type(input) == UUID:
        result = ET.Element("uuid")
        if str(input) != "00000000-0000-0000-0000-000000000000":
            result.text = str(input)
    
    elif type(input) == int:
        result = ET.Element("integer")
        result.text = str(input)
    
    elif type(input) == float:
        result = ET.Element("real")
        result.text = str(input)
    
    elif type(input) == datetime.datetime:
        result = ET.Element("date")
        result.text = input.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    
    elif type(input) == datetime.date:
        result = ET.Element("date")
        result.text = datetime.datetime.fromordinal(input.toordinal()).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    
    elif type(input) == bytes:
        result = ET.Element("binary")
        result.text = base64.b64encode(input).decode()
        if result.text != "":
            result.set("encoding", "base64")
    
    elif input == None:
        result = ET.Element("undef")
    
    if root == None:
        root = ET.Element("llsd")
        root.append(result)
        return ET.tostring(root)
    
    return result

# LLSD BINARY DUMPER
@registerMime(["application/llsd+binary"])
def dumpLLSDBinary(input):
    if type(input) == dict:
        result = b"{" + struct.pack(">i", len(input))
        for key in input:
            result = result + dumpLLSDBinary(key) + dumpLLSDBinary(input[key])
        return result + b"}"
    
    elif type(input) == list:
        result = b"[" + struct.pack(">i", len(input))
        for value in input:
            result = result + dumpLLSDBinary(value)
        return result + b"]"
    
    elif type(input) == str:
        input = input.encode()
        return b"s" + struct.pack(">i", len(input)) + input
    
    elif type(input) == bool:
        return b"1" if True else b"0"
    
    elif type(input) == UUID:
        return b"u" + input.bytes
    
    elif type(input) == int:
        return b"i" + struct.pack(">i", input)
    
    elif type(input) == float:
        return b"r" + struct.pack(">d", input)
    
    elif type(input) == datetime.datetime:
        return b"d" + struct.pack(">i", int(input.timestamp()))
    
    elif type(input) == datetime.date:
        return b"d" + struct.pack(">i", int(datetime.datetime.fromordinal(input.toordinal()).timestamp()))
    
    elif type(input) == bytes:
        return b"i" + struct.pack(">i", len(input)) + input
    
    elif input == None:
        return b"!"
    
    else:
        return dumpLLSDBinary(repr(input))

def dump(input):
    tmp = determinePreferredFormat(request.headers.get('accept', ""), True).split(",")
    mediatype = tmp.pop(0).strip().lower()
    params = [(ii.strip() for ii in i.split("=",1)) for i in tmp]
    
    if mediatype == "*/*":
        mediatype = "application/json"
    
    if mediatype == "":
        return Response("Avaliable content types: " + ", ".join(sorted(supportedMimes.keys())), status=300, mimetype='text/plain')
    
    elif mediatype in supportedMimes:
        return Response(supportedMimes[mediatype](input), mimetype=mediatype)
    
    else:
        #sad.. they wanted a format we don't support. :(
        return Response("Avaliable content types: " + ", ".join(sorted(supportedMimes.keys())), status=406, mimetype='text/plain')
    
