# Windows INI style file to read to override the values below
configFile = '/home/httpd/pyblosxom/pyblosxom.ini'
# -----------------------------------------------------------

py = {}
# What's this blog's title?
py['blog_title'] = "Another pyblosxom blog"

# What's this blog's description (for outgoing RSS feed)?
py['blog_description'] = "blosxom with a touch of python"

# What's this blog's primary language (for outgoing RSS feed)?
py['blog_language'] = "en"

# Where are this blog's entries kept?
py['datadir'] = "/path/to/blog"

# Should I stick only to the datadir for items or travel down the directory
# hierarchy looking for items?  If so, to what depth?
# 0 = infinite depth (aka grab everything), 1 = datadir only, n = n levels down
py['depth'] = 0

# How many entries should I show on the home page?
py['num_entries'] = 40

# Trackback data directory (If you install Standalone Trackback Tool)
py['tb_data'] = '/path/to/tb_data/directory'

# Default parser/preformatter. Defaults to plain (does nothing)
py['parser'] = 'plain'

# Enable Caching? Depends on your directory permissions and whether you use
# preformatters
py['cache_enable'] = 0

# Cached file extension.
py['cache_ext'] = '.compiled'

# The class to give to the first day's div.
py['firstDayDiv'] = 'blosxomFirstDayDiv'

# The filename to log stuff in.
py['logfile'] = '/home/httpd/html/weblog/referer'

# Urls not to track referers from.
py['refer_blacklist'] = 'http://www.latte.ca/~arbrown/journal/.*,http://arbrown.latte.ca/journal/.*,http://www.latte.ca/cgi-bin/weblog-add.py.*'

# Regular expressions to transform urls.
py['refer_transforms'] = {
    r'http://(www\.)?latte\.ca/weblog.*' : r'http://www.latte.ca/weblog/',
    r'http://www\.latte\.ca/~([^\/]*).*' : r'http://\1.latte.ca/',
    }

# XML-RPC data
xmlrpc = {}
# Username to access this server
xmlrpc['username'] = 'someusername'
# Password to access this server
xmlrpc['password'] = 'somepassword'
# Path call that activates XML-RPC mode
xmlrpc['path'] = '/RPC2'

__author__ = 'Wari Wahab <wari@wari.per.sg>'
__version__ = "0+5i_rev3"
__date__ = "$Date: 2003/01/11 04:19:01 $"
__revision__ = "$Revision: 1.1 $"
__copyright__ = "Copyright (c) 2003 Wari Wahab"
__license__ = "Python"
py['pyblosxom_version'] = __version__
py['pyblosxom_name'] = 'pyblosxom'

# Override default configurations
import os
if os.path.isfile(configFile):
    import ConfigParser
    cp = ConfigParser.ConfigParser()
    cp.read(configFile)
    if cp.has_section('pyblosxom'):
        for key in cp.options('pyblosxom'):
            py[key] = cp.get('pyblosxom', key).strip()
    if cp.has_section('xmlrpc'):
        for key in cp.options('xmlrpc'):
            xmlrpc[key] = cp.get('xmlrpc', key).strip()
