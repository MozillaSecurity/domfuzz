#!/usr/bin/env python

from __future__ import absolute_import

import os
import subprocess

from lithium.interestingness import timed_run

# usage: put the js in a separate file from html.  give the js filename to lithium as --testcase *and* the second parameter to this shell_compiles_browser_dies.
# for example:
# ./lithium.py --testcase=c.js shell_compiles_browser_dies.py 120 c.js ~/central/debug-obj/dist/MinefieldDebug.app/Contents/MacOS/firefox-bin uses-c.html

jsshell = os.path.expanduser("~/tracemonkey/js/src/debug/js")


def interesting(args, tempPrefix):
    timeout = int(args[0])
    returncode = subprocess.call([jsshell, "-c", args[1]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if returncode != 0:
        print "JS didn't compile, skipping browser test"
        return False
    wantStack = False  # We do not care about the stack when using this interestingness test.
    runinfo = timed_run.timed_run(args[2:], timeout, tempPrefix, wantStack)
    print "Exit status: %s (%.3f seconds)" % (runinfo.msg, runinfo.elapsedtime)
    return runinfo.sta == timed_run.CRASHED or runinfo.sta == timed_run.ABNORMAL
