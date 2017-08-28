#!/usr/bin/env python

from __future__ import absolute_import

import os
from optparse import OptionParser

import subprocesses as sps

from lithium.interestingness import timed_run, utils


def parseOptions(arguments):
    parser = OptionParser()
    parser.disable_interspersed_args()
    parser.add_option('-r', '--regex', action='store_true', dest='useRegex',
                      default=False,
                      help='Allow search for regular expressions instead of strings.')
    parser.add_option('-s', '--sig', action='store', dest='sig',
                      default='',
                      help='Match this crash signature. Defaults to "%default".')
    parser.add_option('-t', '--timeout', type='int', action='store', dest='condTimeout',
                      default=120,
                      help='Optionally set the timeout. Defaults to "%default" seconds.')

    options, args = parser.parse_args(arguments)

    return options.useRegex, options.sig, options.condTimeout, args


def interesting(cliArgs, tempPrefix):
    (regexEnabled, crashSig, timeout, args) = parseOptions(cliArgs)

    # Examine stack for crash signature, this is needed if crashSig is specified.
    runinfo = timed_run.timed_run(args, timeout, tempPrefix)
    if runinfo.sta == timed_run.CRASHED:
        sps.grabCrashLog(args[0], runinfo.pid, tempPrefix, True)

    timeString = " (%.3f seconds)" % runinfo.elapsedtime

    crashLogName = tempPrefix + "-crash.txt"

    if runinfo.sta == timed_run.CRASHED:
        if os.path.exists(crashLogName):
            # When using this script, remember to escape characters, e.g. "\(" instead of "(" !
            found, _foundSig = utils.file_contains(crashLogName, crashSig, regexEnabled)
            if found:
                print 'Exit status: ' + runinfo.msg + timeString
                return True
            else:
                print "[Uninteresting] It crashed somewhere else!" + timeString
                return False
        else:
            print "[Uninteresting] It appeared to crash, but no crash log was found?" + timeString
            return False
    else:
        print "[Uninteresting] It didn't crash." + timeString
        return False
