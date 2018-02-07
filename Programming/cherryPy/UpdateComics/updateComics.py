#!/usr/local/bin/python

import cgi
import os
import re
import string
import sys
import time
import threading
import urllib
import cgitb

args = ['bizarro', 'dilbert', 'getfuzzy', 'roseisrose',
	'gpf', 'machall', 'achewood', 'sforth',
	'pennyarcade', 'calvinandhobbes', 'sluggy', 'pvp',
	'doonesbury', 'foxtrot', 'megatokyo', 'phantom',
	'joyoftech', 'ctrlaltdel', 'orderofthestick']

# Where to put the comics
location = '/usr/local/www/data/images/comics'
    
comic_list = {}

# Comic dictionaries example 
#comic_list['name'] = {
#    'name': 'name of comic for filename and selection',
#    'page': 'URL of the comic page',
#    'expr': "regex for the picture name",
#    'suff': 'suffix of image (.gif, .jpg, .etc)',
#    'base': 'URL where the pictures are stored _or_ cgi script (see popeye)',
#    'refr': 'URL of referring page (some King Features comics need this'}
    
comic_list['achewood'] = {
	'name': 'achewood',
	'page': 'http://www.achewood.com/',
	'expr': r"/comic.php\?date=\d+",
	'suff': '.gif',
	'base': 'http://www.achewood.com'}

comic_list['calvinandhobbes'] = {
	'name': 'calvinandhobbes',
	# 'page': 'http://www.ucomics.com/calvinandhobbes/viewch.htm',
	'page': 'http://www.ucomics.com/calvinandhobbes/index.phtml',
        # http://images.ucomics.com/comics/ch/1993/ch930804.gif
	'expr': r"images.ucomics.com/comics/ch/\d+/ch\d+\.gif",
	'suff': '.gif',
	'base': 'http://'}

comic_list['doonesbury'] = {
	'name': 'doonesbury',
	'page': 'http://www.ucomics.com/doonesbury/viewdb.htm',
	'expr': r"images.ucomics.com/comics/db/\d+/db\d+\.gif",
	'suff': '.gif',
	'base': 'http://'}

comic_list['foxtrot'] = {
	'name': 'foxtrot',
	'page': 'http://www.ucomics.com/foxtrot/',
	'expr': r"images.ucomics.com/comics/ft/\d+/ft\d+\.gif",
	'suff': '.gif',
	'base': 'http://'}

comic_list['gpf'] = {
	'name': 'gpf',
	'page': 'http://www.gpf-comics.com/',
	'expr': r"gpf\d+.*\.(gif|jpg|png)",
	'suff': '.gif',
	'base': 'http://www.gpf-comics.com/comics/'}

comic_list['bizarro'] = {
	'name': 'bizarro',
	'page': 'http://www.kingfeatures.com/features/comics/bizarro/aboutMaina.php',
	'expr': r"http://\w*.\w*.\w*/content/\w*\?date=\d*",
	'suff': '.gif',
	'base': '',
	'refr': 'http://www.kingfeatures.com'}

comic_list['sforth'] = {
	'name': 'sforth',
	'page': 'http://www.kingfeatures.com/features/comics/sforth/aboutMaina.php',
	'expr': r"http://\w*.\w*.\w*/content/\w*\?date=\d*",
	'suff': '.gif',
	'base': '',
	'refr': 'http://www.kingfeatures.com'}

comic_list['phantom'] = {
	'name': 'phantom',
	'page': 'http://www.kingfeatures.com/features/comics/phantom/aboutMaina.php',
	'expr': r"http://\w*.\w*.\w*/content/\w*\?date=\d*",
	'suff': '.gif',
	'base': '',
	'refr': 'http://www.kingfeatures.com'}

comic_list['ctrlaltdel'] = {
	'name': 'ctrlaltdel',
	'page': 'http://www.ctrlaltdel-online.com/index.php?t=archives&date=last',
	'expr': r"images/comics/.*\d+\.(gif|jpg)",
	'suff': '.jpg',
	'base': 'http://www.ctrlaltdel-online.com/'}

comic_list['pennyarcade'] = {
	'name': 'pennyarcade',
	'page': 'http://www.penny-arcade.com/view.php3',
	'expr': r"images/\d+/\d+\w\.(gif|jpg)",
	'suff': '.gif',
	'base': 'http://www.penny-arcade.com/'}

comic_list['joyoftech'] = {
	'name': 'joyoftech',
	'page': 'http://www.joyoftech.com/joyoftech/index.html',
	'expr': r"joyimages/\d+\.(gif|jpg)",
	'suff': '.gif',
	'base': 'http://www.joyoftech.com/joyoftech/'}

comic_list['sluggy'] = {
	'name': 'sluggy',
	'page': 'http://www.sluggy.com/',
	'expr': r"\comics\/\d+\w+\.(gif|jpg)",
        'suff': '.gif',
        'base': 'http://pics.sluggy.com/'}

comic_list['megatokyo'] = {
	'name': 'megatokyo',
	'page': 'http://www.megatokyo.com/',
	'expr': r"strips/\d+\.(gif|jpg)",
        'suff': '.gif',
        'base': 'http://www.megatokyo.com//'}

comic_list['pvp'] = {
	'name': 'pvp',
	'page': 'http://www.pvponline.com/',
	'expr': r"archive/\d+/pvp\d+\.gif",
        'suff': '.gif',
        'base': 'http://www.pvponline.com//'}

comic_list['machall'] = {
	'name': 'machall',
	'page': 'http://www.machall.com/',
	#'expr': "index.php\?do_command=show_strip&strip_id=\d+",
	'expr': r"index.php\?do_command=show_strip&strip_id=\d+&auth=[^']*",
        'suff': '.gif',
        'base': 'http://www.machall.com/'}

comic_list['dilbert'] = {
	'name': 'dilbert',
	'page': 'http://comics.com/comics/dilbert/',
	'expr': r"dilbert\d+\.(gif|jpg)",
	'suff': '.gif',
	'base': 'http://comics.com/comics/dilbert/archive/images/'}

comic_list['getfuzzy'] = {
	'name': 'getfuzzy',
	'page': 'http://comics.com/comics/getfuzzy/index.html',
	'expr': r"getfuzzy\d+\.(gif|jpg)",
	'suff': '.gif',
	'base': 'http://comics.com/comics/getfuzzy/archive/images/'}

comic_list['roseisrose'] = {
	'name': 'roseisrose',
	'page': 'http://comics.com/comics/roseisrose/index.html',
	'expr': r"roseisrose\d+\.(gif|jpg)",
	'suff': '.gif',
	'base': 'http://comics.com/comics/roseisrose/archive/images/'}

comic_list['orderofthestick'] = {
	'name': 'orderofthestick',
	'page': 'http://www.giantitp.com/cgi-bin/GiantITP/ootscript',
	'expr': r"oots\d+\.(gif|jpg)",
	'suff': '.gif',
	'base': 'http://www.giantitp.com/oots/'}

class GetComic( threading.Thread ):
    def __init__( self, name ):
        super( GetComic, self ).__init__( name=name )
        self.name = name
        self.today = time.strftime("%Y%m%d", time.localtime( time.time() ) )

    def run( self ):
        t1 = time.time()
	name = self.name
	self.retval = ""
        get_me = comic_list[name]
        try:
            conn = urllib.urlopen(get_me['page'])
            page = conn.read()
            conn.close()

            name = re.search(get_me['expr'], page)
            if name is not None:
                path = urllib.URLopener()
                if get_me.has_key('refr'):
                    path.addheader('Referer', get_me['refr'])
                self.retval += self.name + "<br/>\n"
                conn = path.open(get_me['base'] + name.group())
                comic = conn.read()
                conn.close()
                title = get_me['name'] + self.today
                fileName = os.path.join(location,title + get_me['suff'])
                output = open(fileName, 'wb')
                output.write(comic)
                output.close()
                os.chmod( fileName, 0664 )
            else:
                self.retval += "Can't find %s at %s<br/>\n" % (get_me['expr'], get_me['page'])
        except Exception, ex:
            self.retval += "Error (%s) getting %s from %s.<br/>\n" % (ex, get_me['name'], get_me['page'])
        t2 = time.time()
    
def header():
    # Output the standard header info...
    return "<html><head><title>Comics</title></head><body>"

def body():
    import re
    
    get_all = 0
    make_home = 1
    remove_all = 1

    # URL shortening utility
    def shorten_url(line, length = 30):
        sline = line
        while len(sline) > length:
            parts = string.split(sline, '/')
            if len(parts) < 5:
                return sline
            if parts.count('...'):
                parts.remove('...')
            parts[-2:-1] = ['...']
            sline = string.join(parts, '/')
        return sline
    
    if remove_all:
        for name in os.listdir(location):
            os.remove(os.path.join(location,name))
    
    comics = []
    for name in args:
        comic = GetComic( name )
	comic.start()
	comics.append( comic )
    for comic in comics:
        comic.join()
        yield comic.retval

    fileName = os.path.join(location, 'index.html' )
    home = open( fileName , 'w' )
    home.write("<TITLE>Cartoons</TITLE>\n")
    home.write("<P>Comics from the Web.</P>\n")
    home.write("<P>\n")
    
    for name in os.listdir(location):
        if name != 'index.html':
            line = "%s<BR><IMG SRC=\"/images/comics/%s\"><P>\n" % (name, name)
            home.write(line)
    home.close()
    os.chmod( os.path.join(location, 'index.html'), 0664 )
    yield "Updated.<br />\n"

def footer():
    retval = ""
    retval += 'Go <a href="http://www.latte.ca/images/comics">here</a>'
    retval += "</body></html>"
    return retval

def main():
    if len(sys.argv) > 1:
        global args
        args = sys.argv[1:]
    try:
        import time
        t1 = time.time()
        yield header()
	for output in body():
           yield output
        yield footer()
        t2 = time.time()
    except:
        cgitb.handler()

if __name__ == "__main__":
    t1 = time.time()
    for output in main():
        print output
    t2 = time.time()
    print "Total Seconds:", t2 - t1
