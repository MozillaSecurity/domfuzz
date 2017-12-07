# encoding: utf-8
from __future__ import print_function
import collections
import json
import os
import re
import time
import psutil


CPU_CHECK_INTERVAL = 1


def get_tmp_status():
    for subdir in os.listdir("."):
        if re.match(r"^wtmp\d+$", subdir) is not None:
            if os.path.isfile(os.path.join(subdir, "stats.txt")):
                with open(os.path.join(subdir, "stats.txt")) as f:
                    status = json.load(f)
                status["alive"] = psutil.pid_exists(status["pid"])
                del status["pid"]
                yield status


def merge_status():
    status = {"iterations": [], "results": {}, "errors": 0}
    for substat in get_tmp_status():
        status["iterations"].append(substat["iterations"])
        for q, v in substat["results"].items():
            status["results"].setdefault(q, 0)
            status["results"][q] += v
        if not substat["alive"]:
            status["errors"] += 1
    status["results"] = collections.OrderedDict(sorted(status["results"].items(), key=lambda t: t[0]))
    return status


def output_status(status):
    print("Iterations: %d (%s)" % (sum(status["iterations"]),
                                   ", ".join("%d" % v for v in status["iterations"])))
    print("Results:    %d {%s}" % (sum(status["results"].values()),
                                   ", ".join("q%d: %d" % (q, v) for (q, v) in status["results"].items())))
    print("Errors:     %d" % status["errors"])
    print("CPU & Load: %0.1f%% %s" % (psutil.cpu_percent(interval=CPU_CHECK_INTERVAL), os.getloadavg()))
    print("Memory:     %dMB available" % (psutil.virtual_memory().available / 1048576))
    print("Disk:       %dMB available" % (psutil.disk_usage("/").free / 1048576))
    print("Timestamp:  %s" % time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))


def main():
    output_status(merge_status())


if __name__ == "__main__":
    main()
