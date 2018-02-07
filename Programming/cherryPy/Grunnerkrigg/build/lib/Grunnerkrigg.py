# Import CherryPy global namespace
import cherrypy
from elementtree import ElementTree
import urllib

class Index:
    """ Sample request handler class. """

    @cherrypy.expose
    def index(self):
        # Let's link to another method here.
        latest = urllib.urlopen( "http://www.gunnerkrigg.com/index2.php" )
        doc = latest.read()
        a = doc.rfind( '<option value="' )
        a += len( '<option value="' )
        b = doc.find( '"', a )
        last = int( doc[a:b] )
	yield '<html><head><title>Grunnerkrigg Court Index</title></head>'
	yield '<body><h1>Grunnerkrigg Court Index</h1>'
        for i in range( last ):
            yield '<a href="%s">%d</a><br/>' %( self.getUrl( i+1 ), i+1 )
	yield '</body></html>'

    def getUrl( self, index ):
        return 'http://www.gunnerkrigg.com/archive_page.php?comicID=%d'%index

if __name__ == "__main__":
    print "".join( Index().index() )
