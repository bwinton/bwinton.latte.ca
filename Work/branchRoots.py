#!/usr/bin/python
# vim: set fileencoding=utf-8 :


from mercurial import ui, hg
import re
import subprocess
import sys

# hg branches | egrep "^[0-9]" | awk '{print $1}'
myBranchPat = re.compile("(testing|review|fix-breakage|fix-bustage|(bug)?[0-9]{4,6}-?)")
if len(sys.argv) > 1 and sys.argv[1] in ("--all", "-a"):
  myBranchPat = re.compile(".*");
aUi = ui.ui()
repo = hg.repository(aUi, '.')
myBranches = [x for x in repo.branchmap().keys() if myBranchPat.match(x)]
myBranches.sort()

for i in myBranches:
  print i, repo[i], repo[i].rev(), "->",
  pipe = subprocess.Popen(["hg", "log", "-b", i, "--template", "{node|short}\\n"],
                          stdout=subprocess.PIPE)
  baseRev = pipe.stdout.readlines()[-1].strip()
  print baseRev

  # This fails with a RevlogError on the second branch.
  #x = raw_input("Remove this branch? ")
  #if len(x) and x[0].lower() == 'y':
  #  pipe = subprocess.Popen(["hg", "strip", baseRev],
  #                          stdout=subprocess.PIPE)
  #  output = pipe.stdout.read()
  #  print output
