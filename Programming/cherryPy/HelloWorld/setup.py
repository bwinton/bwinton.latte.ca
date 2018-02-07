#! /usr/local/bin/python


from setuptools import setup

setup( name="HelloWorld-CherryPy",
      version="1.0",
      description="Sample CherryPy Egg App",
      author="Blake Winton",
      author_email="bwinton+python@latte.ca",
      url="http://bwinton.latte.ca/",
      py_modules=['HelloWorld'],
      entry_points = {'cherrypy.app': 'Hello = HelloWorld:HelloWorld'}
     )
