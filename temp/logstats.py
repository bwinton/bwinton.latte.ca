"""
Keep statistics based on HTTP Log information

At the moment it computes a list of referrrers
Generate a string containing the last 15 referrers, marked up with HTML
<a> tag.  If the string is longer than 40 characters, truncate by displaying ...
You can access the list of referrers as the variable $referrers

TODO:
Allow number of referrers as parameters
Compute some additional statistics
"""

__author__ = "Ted Leung - twl@sauria.com"
__version__ = "$Id: logstats.py,v 1.1 2003/01/21 06:51:03 twl Exp $"

import string, re, time, cPickle
from libs import api

class PyblStats:
    def __init__(self, py):
        self._py = py
        self._referrers ={}
        self._referrersText = ""
        self._requestors = {}
        self._destinations = {}

    def __str__(self):
        """
        Returns the on-demand generated string - part of pybloxsom plugin fwk
        """
        if self._referrers == None:
            self.genReferrers()
        return self._referrersText

    def addReferer(self, uri):
        # process -
        if uri == '-':
            return

        self._referrers[uri]=self._referrers.get(uri, 0) + 1
        import sys
        refs = self.transformReferrers( self._referrers.items() )
        self._referrers.clear()
        for current in refs:
            (uri,count) = current
            self._referrers[uri] = count

    def addDestination(self, uri):
        return uri

    def addVisitor(self, uri):
        return uri

    # process blacklist
    def blacklist(self, uri):
        if self._py.has_key('refer_blacklist'):
            bad_list = string.split(self._py['refer_blacklist'],',')
            for pat in bad_list:
                if re.search(pat, uri):
                    return 1
        return 0


    def transform(self, uri):
        if self._py.has_key('refer_transforms'):
            transforms = self._py['refer_transforms']
            for pat in transforms.keys():
                (uri, stops) = re.subn( pat, transforms[pat], uri )
        return uri

    def transformReferrers(self, refs):
        outRefs = {}
        import sys
        for tuples in refs:
            uri,count = tuples
            if not self.blacklist( uri ):
                sys.stderr.write( uri + ' -> ' )
                uri = self.transform( uri )
                sys.stderr.write ( uri + '\n' )
                outRefs[ uri ] = outRefs.get( uri, 0 ) + count
        return outRefs.items()

    def genReferrers(self):
        """
        Generate the list of referring files
        """
        def url(tuple):
            """
            Markup (and truncate) a referrer URL
            """
            uri = tuple[0]
            vis = uri
            count = tuple[1]
            size = 40

            if len(uri) > size: vis = vis[:size]+'...'
            return '<a href="'+uri+'" title="'+uri+'">'+vis+' ('+str(count)+')'+'</a><br />'

        def compareCounts(tuple1, tuple2):
            count1 = tuple1[1]
            count2 = tuple2[1]
            if count1 > count2:
                return -1 # reverse order
            if count1 < count2:
                return 1
            return 0

        
        items = self._referrers.items()
        items.sort(compareCounts)
        refs = items[0:14]
        refs = self.transformReferrers( refs )

        self._referrersText = string.join([ url(x) for x in refs ])
        return self._referrersText

def processRequest(args):
    if args == None or args[0] == '':
        return
    import os
    filename = args[0]+'.dat'
    returnCode = args[1]

    try:
        f = file(filename)
        stats = cPickle.load(f)
        f.close()
    except IOError:
        stats = PyblStats({})

    stats.addReferer(os.environ.get('HTTP_REFERER', '-'))
    stats.addDestination(os.environ.get('REQUEST_URI', '-'))
    stats.addVisitor(os.environ.get('REMOTE_ADDR', '-'))

    f = file(filename,"w")
    cPickle.dump(stats, f)


def initialize():
    api.logRequest.register(processRequest)

def load(py, entryList):
    """
    part of the pyblosxom framework
    """
    try:
        filename = py['logfile']+'.dat'
        f = file(filename)
        stats = cPickle.load(f)
        stats._py = py
        f.close()
    except IOError:
        stats = PyblStats(py)

    py["referrers"] = stats.genReferrers()


# command line testing
if __name__ == '__main__':
    pass
