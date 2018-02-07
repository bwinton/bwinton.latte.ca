#! python

import cgi
import cgitb
cgitb.enable()

import json
import os
import sys

providers = ["latte.ca", "gmail.com", "yahoo.com"]

def main():
  if "Firefox" in os.environ["HTTP_USER_AGENT"]:
    print "Content-Type: text/plain\n\n"
  else:
    print "Content-Type: application/json\n\n"

  form = cgi.FieldStorage()

  if not ("username" in form and "domain" in form):
    print json.dumps({"error": "Missing username or domain."})
    return

  rv = {}
  username = form["username"].value
  domain = form["domain"].value
  if username in ("bwinton", "blaketestwinton") or domain == "latte.ca":
    rv["succeeded"] = True
    for key in form:
      rv[key] = form[key].value
  else:
    rv["succeeded"] = False
    addresses = []
    for name in providers:
      if name == domain:
        addresses.append({"domain":name,
                          "alternates": [username+"1209",
                                         username+"1337",
                                         username+"16666"],
                        })
      else:
        addresses.append({"domain":name,
                          "alternates": [username, username+"1"]
                        })
    rv["addresses"] = addresses
  print json.dumps(rv)

if __name__ == "__main__":
  main()
