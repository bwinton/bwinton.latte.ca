#!/usr/bin/env python
"""
Tutorial - Hello World

The most basic (working) CherryPy application possible.
"""
# Import CherryPy global namespace
import cherrypy
import path
import pkg_resources

class Deployer:
    def __init__( self ):
        w = pkg_resources.working_set
	apps = pkg_resources.find_distributions( "apps" )
	self.appList = []
	for dist in apps:
            w.add( dist )
        for line in w.iter_entry_points( "cherrypy.app" ):
            # "Hello = HelloWorld.HelloWorld
	    #mod = __import__( line )
	    #handler = getattr( mod, line )
	    print "Adding handler for %s." % line.name
	    handler = line.load()
	    self.__dict__[line.name] = handler()
	    self.appList.append( line.name )

    @cherrypy.expose
    def index(self):
        # Let's link to all our sub-apps
	apps = ""
	for app in self.appList:
            apps += '  <li><a href="%s/">%s</a></li>\n' % (app, app)
        return '''<h1>CherryPy Apps</h1>
<ul>
%s
</ul>.''' % apps

    @cherrypy.expose
    def default(self, id, *args, **kwargs ):
        retval = "Unknown id %s...(%s, %s)<p>\n" % (id, args, kwargs)
	return retval

# CherryPy always starts with cherrypy.root when trying to map request URIs
# to objects, so we need to mount a request handler object here. A request
# to '/' will be mapped to cherrypy.root.index().
cherrypy.root = Deployer()

if __name__ == '__main__':
    # Use the configuration file tutorial.conf.
    cherrypy.config.update(file = 'tutorial.conf')
    # Start the CherryPy server.
    cherrypy.server.start()
