#!/usr/bin/env python

import cgitb; cgitb.enable()
import cgi
import os
import path
from xml.etree import ElementTree as ET

def main():
    form = cgi.FieldStorage()
    debug = form.has_key( 'debug' )
    ua = os.environ.get( 'HTTP_USER_AGENT', "" )
    if not debug and 'CFNetwork' not in ua or 'iPhone' in ua:
        print 'Location: %s\n' % ("browser.html",)
        print
        return
    if not debug:
        print 'Content-type: application/x-apptapp-repository\n'
        print
    else:
        print
    generateIndex( 'plists' )

def generateIndex( subdir ):
    index = ET.parse( 'repository.plist' ).getroot()
    packageList = index.find('dict/array')

    packages = path.path( subdir ).walkfiles( "*.plist" )
    
    for package in packages:
        category = package.dirname().basename()
        temp = ET.parse( package ).getroot()
        dictElem = temp.findall('dict')[0]
        addSub( dictElem, 'key', 'category' )
        addSub( dictElem, 'string', category )
        addSub( dictElem, 'key', 'date' )
        addSub( dictElem, 'string', package.mtime )
        packageList.append( dictElem )

    print ET.tostring( index, 'UTF-8' )

def addSub( elem, name, value ):
    child = elem.makeelement( name, {} )
    child.text = str(value)
    elem.append( child )

if __name__=='__main__':
    main()
