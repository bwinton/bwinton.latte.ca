"""
Latest few comments RSS2 feed generator using xmltramp, this requires xmltramp
from http://www.aaronsw.com/2002/xmltramp/

It displays py['num_entries'] of the newest comments from your blog (Note: the
comments in questions are the one distributed in pyblosxom - /contrib/plugins/comments)
"""
# vim: tabstop=4 shiftwidth=4 expandtab
from Pyblosxom.renderers.base import RendererBase
from Pyblosxom.tools import Walk
from xmltramp import Element, seed
import urlparse, re, os

# Constants
DOC_REQUEST = '/comments.xml' # What path will activate this renderer
CONTENT_TYPE = 'text/xml' # Some would love to make this application/rss+xml

class CommentRSS2Renderer(RendererBase):
    """
    This renderer is to create valid RSS2 documents without the need for a
    pyblosxom template. I mostly expect you to know what you are doing, before
    attempting this
    """
    # Items for you to change
    creator = 'Ted Leung (twl@sauria.com)'
    # Got other feedback mechanisms? Be sure to add a / at the back of the base
    # URL
    trackback_baseURL = "trackback/"
    pingback_baseURL = "xmlrpc/"
    commentAPI_baseURL = "commentAPI/"
    # Namespaces for you to pick and choose
    namespaces = {
        'content': "http://purl.org/rss/1.0/modules/content/",
        'dc': "http://purl.org/dc/elements/1.1/",
        'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        'trackback': "http://madskills.com/public/xml/rss/module/trackback/",
        'pingback': "http://madskills.com/public/xml/rss/module/pingback/",
        'wfw': "http://wellformedweb.org/CommentAPI/",
    }

    def _addNameSpaces(self, element, namespace_dict):
        for attr in namespace_dict:
            element('xmlns:' + attr, namespace_dict[attr])

    def _createChannel(self):
        # Start our RSS document here
        self._doc = Element('rss')
        d = self._doc
        d('version', '2.0')
        self._addNameSpaces(d, self.namespaces)
        # Add details about our blog here
        d.channel = Element('title')
        channel = d.channel
        channel.title = self._config['blog_title']
        channel.link = self._config['base_url']
        channel.description = self._config['blog_description']
        channel.language = self._config['blog_language']
        channel['dc:creator'] = self.creator

    def _createItem(self, entry, count):
        basedir = self._config['comment_dir']
        path = re.sub(basedir, '', entry['filename'])
        if path.startswith('/'):
            path = path[1:]
        path = re.sub('-[0-9]+\.?[0-9]*?\.' + self._config['comment_ext'] + '$', '', path)

        # xmltramp is weird like that
        if count == 0:
            self._doc.channel.item = Element('title')
            item = self._doc.channel.item
        else:
            self._doc.channel['item':] = Element('title')
            item = self._doc.channel['item':][count]

        cmt = seed(file(entry['filename']))
        item.title = 'Feedback:"%(title)s" by %(author)s on %(pubDate)s'% cmt
        item.description = str(cmt.description)
        link = urlparse.urljoin(self._config['base_url'] + '/', path)
        cmtlink = link + '#%(pubDate)s' % cmt
        item.link = cmtlink

        # Standard comments
        item.comments = link
        # Trackback
        if self.trackback_baseURL:
            item['trackback:ping'] = urlparse.urljoin(self.trackback_baseURL, link)
        # pingback
        if self.pingback_baseURL:
            item['pingback:server'] = self.pingback_baseURL
            item['pingback:target'] = link
        # CommentAPI
        if self.commentAPI_baseURL:
            item['wfw:comment'] = urlparse.urljoin(self.commentAPI_baseURL, path)

    def render(self, header = 1):
        self._data = self._request.getData()
        self._config = self._request.getConfiguration()
        self.addHeader('Content-Type', CONTENT_TYPE)
        self.addHeader('Status', '200')
        self.showHeaders()
        self._createChannel()

        # This is where we get our comments
        if not self._config.has_key('comment_dir'):
            self._config['comment_dir'] = os.path.join(self._config['datadir'],'comments')
        if not self._config.has_key('comment_ext'):
            self._config['comment_ext'] = 'cmt'

        commentDirArray = [self._config['comment_dir'], ]
        if self._data['bl_type'] == 'file':
            commentDirArray.extend( self._data['path_info'][:-1] )
        else:
            commentDirArray.extend( self._data['path_info'] )
        commentDir = apply( os.path.join, commentDirArray )
        if self._data['bl_type'] == 'file':
            comments = Walk(commentDir, 0,
                re.compile(self._data['path_info'][-1] + r'-.*\.' + self._config['comment_ext']))
        else:
            comments = Walk(commentDir, 0,
                re.compile(r'.*\.' + self._config['comment_ext']))
        comments = [x for x in comments if os.path.join(commentDir,
                'LATEST.' + self._config['comment_ext']) != x]

        self._cmtPattern = re.compile(r'.*/(?P<entryname>[^/]+)-(?P<entrytime>[0-9]+\.?[0-9]*?)\.'
                + self._config['comment_ext'] + '$')

        commentlist = []
        for x in comments:
            match = self._cmtPattern.match(x)
            if match:
                item = match.groupdict()
                item['filename'] = x
                commentlist.append((float(item['entrytime']), item))

        # Thank you Randal! :)
        commentlist.sort()
        commentlist.reverse()
        commentlist = [x[1] for x in commentlist]

        if self._config['num_entries'] > len(commentlist):
            num_entries = len(commentlist)
        else:
            num_entries = self._config['num_entries']

        for count in xrange(num_entries):
            self._createItem(commentlist[count], count)

        # We are now ready to present the xml
        self.write('<?xml version="1.0" encoding="iso-8859-1"?>\n')
        self.write(self._doc.__repr__(1, 1))

def cb_renderer(args):
    import sys
    req = args['request']
    http = req.getHttp()
    conf = req.getConfiguration()

    if http['PATH_INFO'].endswith( DOC_REQUEST ):
        http['PATH_INFO'] = http['PATH_INFO'][:-len(DOC_REQUEST)]
        return CommentRSS2Renderer(req, conf.get('stdoutput', sys.stdout))

def cb_filelist(args):
    # Short circuiting the filelist process
    req = args['request']
    http = req.getHttp()
    if http['PATH_INFO'].endswith( DOC_REQUEST ):
        http['PATH_INFO'] = http['PATH_INFO'][:-len(DOC_REQUEST)]
        return []

