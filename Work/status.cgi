#! /usr/bin/python

import cgi
import cgitb
cgitb.enable()

import json
import os
import sys
import urllib2

def main():
  print "Content-Type: application/json\n\n"

  form = cgi.FieldStorage()
  params = "?q=(thunderbird+OR+raindrop)+mozilla&rpp=50"
  if "refresh_url" in form:
    params = form["refresh_url"].value

  x = urllib2.urlopen("http://search.twitter.com/search.json"+params)
  print x.read()

if __name__ == "__main__":
  main()
