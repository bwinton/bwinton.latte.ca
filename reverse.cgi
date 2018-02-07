#!/usr/bin/env python

import sys
import cgi
import cgitb
import re
import urllib

ALEF='\xE0'
TAV='\xFA'
RE_HEB=re.compile('[%s-%s]' % (ALEF,TAV))
RE_HEB_WHITE=re.compile('[%s-%s \t\n\r\f\v]' % (ALEF,TAV))
RE_MULTI_HEB=re.compile('[%s-%s][%s-%s \t\n\r\f\v]+' % (ALEF,TAV,ALEF,TAV))

def asciify( intext ):
    retval = intext
    for x in xrange( ord(ALEF), ord(TAV)+1 ):
        retval = retval.replace( '&#x%x;'%(x+0x4F0,), '%c'%(x,) )
        retval = retval.replace( '&#x%X;'%(x+0x4F0,), '%c'%(x,) )
        retval = retval.replace( '&#x0%x;'%(x+0x4F0,), '%c'%(x,) )
        retval = retval.replace( '&#x0%X;'%(x+0x4F0,), '%c'%(x,) )
        retval = retval.replace( '&#%d;'%(x+0x4F0,), '%c'%(x,) )
    return retval

def reverse( intext ):
    retval = intext
    end = -1
    matchObj = RE_MULTI_HEB.search( retval )
    while matchObj != None:
        start = matchObj.start()
        end = matchObj.end()
        chars = list(retval[start:end])
        chars.reverse()
        sys.stderr.write( "Reversing from %d to %d ['%s'->'%s'].\n" % (start, end, retval[start:end], ''.join(chars)) )
        sys.stderr.flush()
        retval = retval[0:start] + ''.join(chars) + retval[end:]
        matchObj = RE_MULTI_HEB.search( retval, end+1 )
    return retval

def main( args ):
    try:
        print "Content-type: text/html\n\n"
        if not args.has_key( "url" ):
            print "<html><head><title>error</title></head><body><h1>No Url Specified</h1></body></html>\r\n"
            return

        url = urllib.urlopen( args["url"].value )
        intext = url.read( -1 )
        url.close()
        outtext = asciify( intext )
        outtext = reverse( outtext )
        sys.stdout.write( outtext )
        sys.stdout.flush()
        sys.stdout.close()
    except:
        cgitb.handler()

form = cgi.FieldStorage()
main( form )
