#! /usr/local/bin/python


from setuptools import setup

setup( name="UpdateComics-CherryPy",
      version="1.0",
      description="Comic Collator CherryPy Egg App",
      author="Blake Winton",
      author_email="bwinton+python@latte.ca",
      url="http://bwinton.latte.ca/",
      py_modules=['ComicsApp', 'updateComics'],
      entry_points = {'cherrypy.app': 'Comics = ComicsApp:UpdateComics'}
     )
