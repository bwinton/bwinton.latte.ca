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

  form = json.load(sys.stdin)

  # Validation.
  if not ("items" in form):
    print json.dumps({"error": "Missing item."})
    return

  rv = {}
  username, domain = form["items"][0]["address"].split("@")
  if form["account"]["first_name"] in ("Bryan", "Dan"):
    rv["succeeded"] = False
    rv["errors"] = {"account.first_name": 'Invalid first name.  Try "Andrew" instead.',
                    "account.billing.card_cvv": "Incorrect CVV.",
                    "items.0.quote": "Quote is invalid or expired; please retry suggest."
    }
  else:
    rv["succeeded"] = True
    f = open("config.xml").read()
    f = f.replace("%DOMAIN%", domain)
    rv["config"] = f
  print json.dumps(rv)

if __name__ == "__main__":
  main()
