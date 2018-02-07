#!/usr/local/bin/python

import Image, ImageDraw
import random
import StringIO
import sys
import urllib

class Sparkline(object):
    def __init__(self, request):
        self._request = request
        self._data = None

    def __str__(self):
        if self._data == None:
            data = self._request.getData()
	    values = [len(x.getData()) for x in data['entry_list']]
	    minVal = min(values)
	    maxVal = max(values)
	    values = [int(float(x-minVal) /(maxVal-minVal) * 100) for x in values]
            self._data = '<img src="%s">' % self.getData( values )
        return self._data

    def getData(self, results):
        """Returns a sparkline image as a data: URI.
           The source data is a list of values between
           0 and 100. Values greater than 95
           are displayed in red, otherwise they are displayed
           in green"""
        im = Image.new("RGB", (len(results)+2, 20), 0xd8e2c6)
        draw = ImageDraw.Draw(im)
        coords = zip(range(len(results)), [15 - y/10 for y in results])
        draw.line(coords, fill="#000000")
        end = coords[-1]
        end_pt = coords[results.index(max(results))]
        draw.rectangle([end_pt[0]-1, end_pt[1]-1,
            end_pt[0]+1, end_pt[1]+1], fill="#FF0000")
        end_pt = coords[results.index(min(results))]
        draw.rectangle([end_pt[0]-1, end_pt[1]-1,
            end_pt[0]+1, end_pt[1]+1], fill="#0000FF")
        draw.rectangle([end[0]-1, end[1]-1, end[0]+1, end[1]+1], fill="#00AA00")
        del draw 
        f = StringIO.StringIO()
        im.save(f, "PNG")
	return 'data:image/png,' + urllib.quote(f.getvalue())

def cb_prepare(args):
    request = args["request"]
    data = request.getData()
    data["sparkline"] = Sparkline(request)
