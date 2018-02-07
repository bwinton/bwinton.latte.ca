#!/Library/Frameworks/Python.framework/Versions/2.4/bin/python

import Image
import random
import StringIO
import os

print "Content-Type: image/png\n"

color = 0x0000FF;
lockfile = "/tmp/jeff.lock"
if not os.path.exists(lockfile):
  color = 0x00FF00
  open(lockfile,"w")
else:
  os.unlink(lockfile)

img = Image.new("RGB", (100,100), color)
f = StringIO.StringIO()
img.save(f, "PNG")
f.seek(0)
print f.read()
