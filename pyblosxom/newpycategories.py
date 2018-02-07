# vim: tabstop=4 shiftwidth=4
"""
Walks through your blog root figuring out all the categories you have
and how many entries are in each category.  It generates html with
this information and stores it in the $categorylinks variable which
you can use in your head or foot templates.

Additionally, you can specify the flavour for the link by creating an 
entry in the config.py file or the ini file with the name 
"category_flavour" and the value of the flavour you want to use.

config.py example::

   py["category_flavour"] = "index"
"""
__author__ = "Will Guaraldi - willg at bluesock dot org"
__version__ = "$Id: pycategories.py,v 1.12 2003/08/07 14:15:23 willhelm Exp $"

from Pyblosxom import tools
import os, re, sys

class PyblCategories:
    def __init__(self, request):
        self._request = request
        self._categories = None

    def __str__(self):
        if self._categories == None:
            self.genCategories()
        return self._categories

    def genItems(self, items, prefix=""):
        retval = []
        for item in sorted(items.keys()):
          path = prefix + "/" + item
          num = self._elistmap.get(path, 0)
          for key in self._elistmap.keys():
              if key != path and key.find(path) == 0 and self._elistmap[key] > 0:
                  num = num + self._elistmap[key]
          if num == 0:
              continue
          elif num < 0:
              num = " (link)"
          elif num > 0:
              num = " (%d)" % num

          # Do something with len(itemlist)-1?
          children = self.genItems(items[item], path)
          if len(children):
            retval.append("<li class='expand collapsed'>")
          else:
            retval.append("<li>")
          retval.append("<a href=\"%s%s%s\">%s</a>%s" % (
                 self._baseurl, path, self._flavour, item + "/", num))
          if len(children):
            retval.append("<ul>")
            retval.extend(children)
            retval.append("</ul>")
          retval.append("</li>")
        return retval

    def genCategories(self):
        config = self._request.getConfiguration()
        root = config["datadir"]

        flav = config.get("category_flavour", "")
        if flav:
            self._flavour = "?flav=" + flav
        else:
            self._flavour = ""

        self._baseurl = config.get("base_url", "")

        # build the list of directories (categories)
        clist = tools.Walk(self._request, root, pattern=re.compile('.*'), return_folders=1)
        clist = [mem[len(root)+1:] for mem in clist]

        clist.sort()
        clist.insert(0, "")

        # build the list of entries
        elist = tools.Walk(self._request, root)
        elist = [mem[len(root)+1:] for mem in elist]

        elistmap = {}
        for mem in elist:
            name = "/"+os.path.dirname(mem)
            isLink = False
            temp = mem
            while temp:
                if os.path.islink(os.path.join(root, temp)):
                  isLink = True
                temp = os.path.dirname(temp)
            if isLink:
                elistmap[name] = -1
                continue
            elistmap[name] = 1 + elistmap.get(name, 0)
        self._elistmap = elistmap

        retval = {}
        for path in clist:
          itemlist = path.split(os.sep)
          cur = retval
          for item in itemlist:
            cur = cur.setdefault(item, {})
        retval = self.genItems(retval)
        self._categories = "<ul class='collapsable'>" + "".join(retval) + "</ul>"


def cb_prepare(args):
    request = args["request"]
    data = request.getData()
    data["newcategorylinks"] = PyblCategories(request)
