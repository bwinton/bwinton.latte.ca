# Import CherryPy global namespace
import cherrypy
import updateComics

class UpdateComics:
    """ Sample request handler class. """

    @cherrypy.expose
    def index(self):
        yield updateComics.header()
	yield updateComics.body()
	yield updateComics.footer()
