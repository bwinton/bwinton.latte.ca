#!/usr/bin/python

import cgi
import os
import string
import sys
import time
import urllib
import urlparse
import cgitb
import py2html
import PyFontify

def get( url, start, end ):
    temp = ""
    try:
        session = urllib.urlopen( url )
        index = -1
        retry = 0
        while index == -1:
            temp2 = session.read()
            if temp2 == "":
                retry = retry + 1
                if retry > 5:
                    break
                else:
                    continue
            retry = 0
            temp = temp + temp2
        index = string.find(temp, start)
        temp = temp[index:]
        index = string.find(temp, end )
        temp =  temp[:index+len(end)]
        session.close()
    except IOError, detail:
        # If we can't connect, fail semi-gracefully.
        temp = 'Can\'t connect to ' + url + '\n'
        temp = temp + str(detail)
    return temp

storyurl = "http://weather.yahoo.com/forecast/Toronto_CN_c.html"

def header():
    # Output the standard header info...
    print "Content-type: text/html"
    print
    print "<HTML><HEAD><TITLE>Stories</TITLE></HEAD><BODY>"
    print "<H1>Stories</H1>"
    print

def getUrl( line ):
    start = line.find( 'href="' )
    if start != -1:
        start = start + 6
        end = line.find ( '"', start )
        return "http://www.mcstories.com/" + line[ start:end ]
    else:
        return None

def fixUrls( url, temp ):
    hrefStart = temp.find( 'href="', 0 )
    hrefEnd = 0
    while hrefStart != -1:
        hrefStart += 6
        hrefEnd = temp.find( '"', hrefStart )
        href = temp[hrefStart:hrefEnd]
        if href.startswith( "../Tags" ) or href.startswith( "../Authors" ):
            href = "mailto:dev@null.net"
        else:
            href = urlparse.urljoin( url, href )
        temp = temp[:hrefStart] + href + temp[hrefEnd:]
        hrefStart = temp.find( 'href="', hrefStart )
    return temp

def story():
    temp = get( 'http://www.mcstories.com/WhatsNew.html',
                '<h1>Recent Additions</h1>',
                '<h3><a href="WhatWasNew.html">What Previously Was Recent</a></h3>' )
    temp = temp.splitlines( 1 )
    urls = []
    for line in temp:
        test = getUrl( line )
        if test != None:
            urls.append( getUrl( line ) )
    urls[20:] = []
    for url in urls:
        temp = get( url, '<h3>Categories:</h3>', '<p class="nav">' )
        temp = fixUrls( url, temp[:-16])
        print temp

def main():
    try:
        header()
        story()
        # End the page off.
        print "</BODY></HTML>"
    except:
        cgitb.handler()

main()
