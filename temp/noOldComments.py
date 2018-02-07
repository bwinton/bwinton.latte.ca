"""
FIXME - Documentation for what your plugin does and how to set it up
goes here.

FIXME - License information goes here.

FIXME - Copyright information goes here.
"""
__author__      = "FIXME - your name and email address"
__version__     = "FIXME - version number and date released"
__url__         = "FIXME - url where this plugin can be found"
__description__ = "FIXME - one-line description of plugin"

import sys
import time

def verify_installation(request):
    # FIXME - code to verify that this plugin is installed correctly 
    # here.

    return 1


def cb_comment_reject(args):
    req = args["request"]
    comment = args["comment"]

    blog_config = req.getConfiguration()

    # FIXME - code for figuring out whether this comment should
    # be rejected or not goes here.  If you want to reject the
    # comment, return 1.  Otherwise return 0.
    data = req.getData()
    entry = data['entry_list'][0]
    if ( (time.time() - entry['mtime']) >= 2419200):
        return 1
    return 0
