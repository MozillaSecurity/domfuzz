#!/usr/bin/env python

from __future__ import absolute_import

import os

from Collector.Collector import Collector


def createCollector(tool):
    assert tool == "DOMFuzz" or tool == "jsfunfuzz"
    cacheDir = os.path.normpath(os.path.expanduser(os.path.join("~", "sigcache")))
    try:
        os.mkdir(cacheDir)
    except OSError:
        pass  # cacheDir already exists
    collector = Collector(sigCacheDir=cacheDir, tool=tool)
    return collector


def printCrashInfo(crashInfo):
    if crashInfo.createShortSignature() != "No crash detected":
        print
        print "crashInfo:"
        print "  Short Signature: " + crashInfo.createShortSignature()
        print "  Class name: " + crashInfo.__class__.__name__   # "NoCrashInfo", etc
        print "  Stack trace: " + repr(crashInfo.backtrace)
        print


def printMatchingSignature(match):
    print "Matches signature in FuzzManager:"
    print "  Signature description: " + match[1].get('shortDescription')
    print "  Signature file: " + match[0]
    print
