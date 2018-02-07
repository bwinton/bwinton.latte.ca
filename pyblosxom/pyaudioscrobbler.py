# vim: tabstop=4 shiftwidth=4
"""
Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of the
Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Copyright 2005 The PyBlosxom Development Group
"""
__author__ = "Blake Winton - bwinton at latte dot ca"
__version__ = "$Id: "

# The base url to grab the audio data from.
_URL = "http://ws.audioscrobbler.com/rdf/history/"

# The time between updates.
_DELTA = 1*60*60   # 1 hour in seconds.

# The number of characters to truncate at.
_TRUNCATE_LENGTH = 32

# The template to expand into.
_TEMPLATE = '<a href="%s">%s - %s</a><br />\n'

import time

class PyAudioScrobbler:
    def __init__(self, request, user):
        self._request = request
        self._user = user
        self._data = None

    def __str__(self):
        if self._data == None:
            self.getData()
        return self._data

    def getData(self):
        import os
        config = self._request.getConfiguration()
        dir = config.get( "audio_cache", "/tmp/" )
        filename = os.path.join( dir, self._user + ".auc" )
        if not os.path.exists( dir ):
            os.makedirs( dir )
            self.getFile( filename, os )
        elif not os.path.exists( filename ):
            self.getFile( filename, os )
        elif ((os.stat( filename )[9] + _DELTA) < time.time() ):
            self.getFile( filename, os )
        else:
            self._data = self.parseData( file(filename,"r").read(),(os.stat( filename )[9] + _DELTA) - time.time() )

    def getFile( self, filename, os ):
        import urllib
        retval = ""
        url = _URL + self._user
        try:
            data = urllib.urlopen( url )
            cache = file( filename, "w" )
            retval = data.read()
            cache.write( retval )
            cache.flush()
            cache.close()
        except:
            if not os.path.exists( filename ):
                cache = file( filename )
                retval = cache.read()
                cache.close()
            else:
                cache = file( filename, "w" )
                retval = "Unable to open feed!"
                cache.write( retval )
                cache.close()
        self._data = self.parseData( retval, (os.stat( filename )[9] + _DELTA) - time.time() )
        return

    def parseData( self, data, seconds ):
        import sys
        sys.stderr.write( "Caching for %d seconds" % (seconds,) )
        from xml.dom.minidom import parseString
        retval = ""
        dom = parseString( data )
        songs = dom.getElementsByTagName( 'description' )
        links = dom.getElementsByTagName( 'link' )
        songs = zip( songs, links )
        header = songs[0]
        songs = songs[1:]
        desc = header[0].firstChild.nodeValue
        link = header[1].firstChild.nodeValue
        hours = seconds/3600
        minutes = (seconds%3600)/60
        seconds = seconds%60
        retval += '<a href="%s">%s (caching for another %d:%02d:%02d)</a><br />\n' % ( link, desc, hours, minutes, seconds )

        for song in songs:
            retval += self.appendSong( song )

        dom.unlink()
        return retval

    def appendSong( self, song ):
        artist,title = song[0].firstChild.nodeValue.split( ' - ', 1 )
        link = song[1].firstChild.nodeValue
        return _TEMPLATE % (link, artist, title)

def cb_prepare(args):
    request = args["request"]
    data = request.getData()
    config = request.getConfiguration()
    for user in config.get( "audio_users", [] ):
        data["audio-"+user] = PyAudioScrobbler(request, user)

