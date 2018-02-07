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

import os, re

class BikeLog:
    def __init__(self, request, user):
        self._request = request
        self._user = user
        self._data = None
        self.x = re.compile( "([^a-zA-Z0-9_]+)" )

    def __str__(self):
        if self._data == None:
            self.getData()
        return self._data

    def getData(self):
        self._data = ""
        config = self._request.getConfiguration()
        dir = config.get( "bikelog", "/tmp/" )
        filename = os.path.join( dir, self._user + ".txt" )
        infile = file(filename,"r")
        line = infile.readline().strip()
        template = "<tr><td>Error!</td></tr>\n"
        headers = ""
        while line.startswith("#") or len(line) == 1:
            line = infile.readline()
            if line.startswith( "# template=" ):
                template = line[len("# template="):]
        while len(line) <> 1:
            headers = headers + line
            line = infile.readline()
        headers = self.x.split(headers)
        while 1:
            temp = ""
            while len(line) == 1:
                line = infile.readline()
            while len(line) > 1:
                temp = temp + line
                line = infile.readline()
            # Break temp up into a dictionary.
            self._data = self._data + template % self.parseLine(headers,temp)
            if len(line) == 0:
                break

    def parseLine( self, headers, line ):
        previousHeader = ""
        data = {}
        for elem in headers:
            if self.x.match( elem ):
                # We've got a delimiter, so search for it in the line
                index = line.find( elem )
                data[previousHeader] = line[:index]
                line = line[index+len(elem):]
            else:
                previousHeader = elem
        return data


def cb_prepare(args):
    request = args["request"]
    data = request.getData()
    config = request.getConfiguration()
    for user in config.get( "bikelog_users", [] ):
        data["bikelog-"+user] = BikeLog(request, user)

