#! /usr/local/bin/python


from setuptools import setup

setup( name="Grunnerkrigg-CherryPy",
      version="1.0",
      description="Grunnerkrigg Court Index App",
      author="Blake Winton",
      author_email="bwinton+python@latte.ca",
      url="http://bwinton.latte.ca/",
      py_modules=['Grunnerkrigg'],
      entry_points = {'cherrypy.app': 'Grunnerkrigg = Grunnerkrigg:Index'}
     )
