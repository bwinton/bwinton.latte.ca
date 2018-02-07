# vim: tabstop=4 shiftwidth=4 expandtab
from Pyblosxom.renderers.base import RendererBase
from Pyblosxom.tools import Stripper
from xml.dom.minidom import Document
import urlparse
AGENT = 'http://weblog.latte.ca'
ERROR_TO = 'mailto:bwinton+blog@latte.ca'
DOC_REQUEST = '/index.xml'

class RSS2Renderer(RendererBase):
    """
    This renderer is to create valid RSS2 documents without the need for a
    pyblosxom template. I mostly expect you to know what you are doing, before
    attempting this
    """
    # Items for you to change
    creator = 'Blake Winton (bwinton+blog@latte.ca)'
    # Have you installed pyblosxom comments? 1 if yes, else None to all these
    # variables
    comments = 1
    # Be sure to add a / at the back of the base URL
    trackback_baseURL = None
    pingback_baseURL = None
    commentAPI_baseURL = 'http://www.latte.ca/cgi-bin/commentAPI.cgi/'
    # How long you want the simple description to be
    desc_length = 20 # 20 words, at the most for me
    # Create the big html? <content:encoded>, yes, then 1, else 0
    create_entry = 1
    entry_type = 'CDATA' # or 'escaped' - choose your poison
    # Namespaces for you to pick and choose
    namespaces = {
        'admin': "http://webns.net/mvcb/",
        'content': "http://purl.org/rss/1.0/modules/content/",
        'creativeCommons': "http://backend.userland.com/creativeCommonsRssModule",
        'dc': "http://purl.org/dc/elements/1.1/",
        'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        'html': "http://www.w3.org/1999/html",
        'slash': "http://purl.org/rss/1.0/modules/slash/",
        'trackback': "http://madskills.com/public/xml/rss/module/trackback/",
        'pingback': "http://madskills.com/public/xml/rss/module/pingback/",
        'wfw': "http://wellformedweb.org/CommentAPI/",
    }

    def _addText(self, element, text, baseElement):
        e = self._doc.createElement(element)
        e.appendChild(self._doc.createTextNode(text))
        baseElement.appendChild(e)
        return e

    def _addCDATA(self, element, text, baseElement):
        e = self._doc.createElement(element)
        e.appendChild(self._doc.createCDATASection(text))
        baseElement.appendChild(e)
        return e

    def _addElemAttr(self, element, attr, content, baseElement, text = None):
        e = self._doc.createElement(element)
        e.setAttribute(attr, content)
        if text:
            e.appendChild(self._doc.createTextNode(text))
        baseElement.appendChild(e)
        return e

    def _addAttr(self, element, attr, content):
        element.setAttribute(attr, content)

    def _addNameSpaces(self, element, namespace_dict):
        for attr in namespace_dict:
            self._addAttr(element, 'xmlns:' + attr, namespace_dict[attr])

    def _createChannel(self):
        # Start our RSS document here
        self._doc = Document()
        d = self._doc
        rss = d.createElement('rss')
        rss.setAttribute('version', '2.0')
        self._addNameSpaces(rss, self.namespaces)
        d.appendChild(rss)
        self._channel = d.createElement('channel')
        channel = self._channel
        rss.appendChild(channel)

        # Add details about our blog here
        self._addText('title', self._config['blog_title'], channel)
        self._addText('link', self._config['base_url'], channel)
        self._addText('description', self._config['blog_description'], channel)
        self._addText('language', self._config['blog_language'], channel)
        self._addText('ttl', '60', channel)
        self._addText('dc:creator', self.creator, channel)
        self._addElemAttr('admin:generatorAgent', 'rdf:resource', AGENT, channel)
        self._addElemAttr('admin:errorReportsTo', 'rdf:resource', ERROR_TO, channel)

    def _generateDesc(self, html):
        s = Stripper()
        s.feed(html)
        str = s.gettext()
        frag = str.split()
        if len(frag) > self.desc_length:
            frag = frag[:self.desc_length]
            frag.append('...')
        return ' '.join(frag)

    def _createItem(self, entry):
        d = urlparse.urlsplit(self._config['base_url'])
        domain = '%s://%s' % (d[0], d[1])
        item = self._doc.createElement('item')
        self._channel.appendChild(item)
        self._addText('title', entry['title'], item)
        self._addElemAttr('guid', 'isPermaLink', 'false', item, entry['file_path'])
        self._addText('link', urlparse.urljoin(self._config['base_url'] + '/',
                entry['file_path']), item)
        # Text entry
        self._addText('description', self._generateDesc(entry['body']), item)
        if self.create_entry:
            if self.entry_type == 'CDATA':
                self._addCDATA('content:encoded', entry['body'], item)
            else:
                self._addText('content:encoded', entry['body'], item)
        # Metadata stuff
        # Category
        if entry['path'].strip():
            # category or dc:subject, but NOT both
            self._addElemAttr('category', 'domain', domain, item, entry['path'])
            #self._addText('dc:subject', entry['path'], item)
        self._addText('dc:date', entry['w3cdate'], item)
        # Comment stuff as per defined by others
        if self.comments:
            # Standard comments
            self._addText('comments', urlparse.urljoin(self._config['base_url'] + '/',
                    entry['file_path']), item)
            try:
                # So we assume that the comment plugin is installed here
                import comments
                self._addText('slash:comments', \
                        str(comments.getCommentCount(entry, self._config)), item)
            except ImportError:
                pass
            # Trackback
            if self.trackback_baseURL:
                self._addText('trackback:ping', urlparse.urljoin(self.trackback_baseURL,
                        entry['file_path']), item)
            # pingback
            if self.pingback_baseURL:
                self._addText('pingback:server', self.pingback_baseURL, item)
                self._addText('pingback:target', urlparse.urljoin(self._config['base_url'] + '/',
                        entry['file_path']), item)
            # CommentAPI
            if self.commentAPI_baseURL:
                self._addText('wfw:comment', urlparse.urljoin(self.commentAPI_baseURL,
                        entry['file_path']), item)
            # CommentRss
            self._addText('wfw:commentRss', urlparse.urljoin(self._config['base_url'] + '/',
                        entry['file_path'] + '/comments.xml'), item)

    def render(self, header = 1):
        self._data = self._request.getData()
        self._config = self._request.getConfiguration()
        self.addHeader('Content-Type', 'text/xml')
        self.showHeaders()
        self._createChannel()

        if self._config['num_entries'] > len(self._content):
            num_entries = len(self._content)
        else:
            num_entries = self._config['num_entries']

        for count in xrange(num_entries):
            self._createItem(self._content[count])

        # We are now ready to present the xml
        self.write(self._doc.toxml())

def cb_renderer(args):
    import sys
    req = args['request']
    http = req.getHttp()
    conf = req.getConfiguration()

    if http['PATH_INFO'].endswith( DOC_REQUEST ):
        http['PATH_INFO'] = http['PATH_INFO'][:-len(DOC_REQUEST)]
        return RSS2Renderer(req, conf.get('stdoutput', sys.stdout))
