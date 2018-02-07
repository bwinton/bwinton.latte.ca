#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import subprocess
import sys

def main(data):
    try:
        sys.stdout.write("Content-type: text/html; charset=utf-8\n\n")
        sys.stdout.flush()
        json_payload = data
        if (not json_payload):
            json_payload = u'{"build":"Nothing to see here…"}'
        myjson = json.loads(json_payload)
        zen = u'not found.'
        if myjson.has_key('zen'):
            zen = myjson.get('zen')
        sys.stdout.write(zen.encode('utf-8'))
        sys.stdout.write('\n'.encode('utf-8'))
        sys.stdout.flush()
        sys.stdout.close()
        if myjson.has_key('build'):
            build = myjson.get('build')
            if build.has_key('status'):
                zen = build.get('status')
                subprocess.call('./setuid')

    except:
        e = sys.exc_info()[0];
        sys.stderr.write(str(e));

data = sys.stdin.read()
main(data)
