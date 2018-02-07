#! /usr/bin/python

import cgi
import cgitb
cgitb.enable()

import json
import os
import sys
import uuid

def main():
  if "Firefox" in os.environ["HTTP_USER_AGENT"]:
    print "Content-Type: text/plain\n\n"
  else:
    print "Content-Type: application/json\n\n"

  form = cgi.FieldStorage()
  if not ("first_name" in form and "last_name" in form and "providers" in form):
    print json.dumps({"error": "Missing first name, last name, or providers."})
    return

  firstname = form["first_name"].value.lower().replace(" ","")
  lastname = form["last_name"].value.lower().replace(" ","")
  providers = form["providers"].value.lower().split(",")
  providerData = {
    "aol":{"price": "0",
           "extraFields": {},
           "addresses": [firstname+"@aol.com",
                         firstname+"_"+lastname+"@aol.com",
                         firstname[:1]+lastname+"@aol.com"],
    },
    "hover":{"price": "$20-$40",
             "extraFields": {"quote":  uuid.uuid4().hex[:20],
                             "product": "personalized_email"},
             "addresses": [{"address": firstname+"@"+lastname+".com", "price":"$20.00"},
                           {"address": "me@"+firstname+lastname+".com", "price": "$22.50"},
                           {"address": firstname+"@"+firstname+lastname+".com", "price": "$25.00"},
                           {"address": firstname+"@"+firstname+lastname+".net", "price": "$30.00"},
                           {"address": firstname+"@"+firstname+lastname+".org", "price": "$35.00"},
                           {"address": firstname+"@"+firstname+lastname+".me", "price": "$37.50"},
                           {"address": "me@"+firstname+lastname+".me", "price": "$40.00"}],
    },
    "yandex":{"price": "0",
              "extraFields": {},
              "addresses": [firstname+"@yandex.com",
                            firstname+"_"+lastname+"@yandex.com",
                            firstname[:1]+lastname+"@yandex.com"],
    },
  }

  out = []
  for provider in providers:
    rv = {"provider":provider}
    if firstname in ("test", "error"):
      rv["succeeded"] = False
      rv["errors"] = {"first_name": "Invalid first name."}
    else:
      rv["succeeded"] = True
      rv["price"] = providerData[provider]["price"]
      rv["addresses"] = providerData[provider]["addresses"]
      for key,value in providerData[provider]["extraFields"].items():
        rv[key] = value
    out.append(rv)

  print json.dumps(out)

if __name__ == "__main__":
  main()
