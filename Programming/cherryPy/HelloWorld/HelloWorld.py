# Import CherryPy global namespace
import cherrypy

class HelloWorld:
    """ Sample request handler class. """

    @cherrypy.expose
    def index(self):
        # Let's link to another method here.
        return '''We have a <a href="showMessage">message</a> for you!<br/>
and a <a href="showMassage/foo/bar?baz=qux&yadda=yadda&yadda=more%20yadda">bad link</a>.'''
    
    @cherrypy.expose
    def showMessage(self):
        # Here's the important message!
        retval = "Hello World!<br />\n"
	return retval

    @cherrypy.expose
    def default(self, id, *args, **kwargs ):
        retval = "Details for id %s...(%s, %s)<p>\n" % (id, args, kwargs)
        items = [x + ': ' + y for x,y in cherrypy.request.headerMap.items()]
	retval += "requestLine: " + cherrypy.request.requestLine + "<br />\n"
	retval += "method: " + cherrypy.request.method + "<br />\n"
	retval += "path: " + cherrypy.request.path + "<br />\n"
	retval += "queryString: " + cherrypy.request.queryString + "<br />\n"
	retval += "protocol: " + cherrypy.request.protocol + "<br />\n"
	retval += "base: " + cherrypy.request.base + "<br />\n"
	retval += "browserUrl: " + cherrypy.request.browserUrl + "<br />\n"
	retval += "objectPath: " + cherrypy.request.objectPath + "<br />\n"
	retval += "originalPath: " + cherrypy.request.originalPath + "<br />\n"
	retval += "<p>\nItems:<br />\n"
	retval += "<br />\n".join(items)
	return retval
