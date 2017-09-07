**For the maintained version of jsfunfuzz, head to the [funfuzz](https://github.com/MozillaSecurity/funfuzz) repository.**

This repository contains [DOMFuzz](dom) tests layout and other parts of browser engines through DOM API calls.

Most of the code other than testcase generation is written in Python: restarting the program when it exits or crashes, noticing evidence of new bugs from the program's output, [reducing testcases](https://github.com/MozillaSecurity/lithium/).


## Setup

Install the required pip packages using `pip install -r requirements.txt`.

Some parts of the fuzzer will only activate if the Python scripts can find your mozilla-central tree:
```
mkdir -p ~/trees/
hg clone https://hg.mozilla.org/mozilla-central/ ~/trees/mozilla-central/
```

Some parts of the harness assume a clean **Mercurial** clone of the mozilla trees. There is insufficient testing with Git for now - please file an issue if you hit problems with Git repositories of mozilla trees.

If you want to use these scripts to compile SpiderMonkey or Firefox, install the usual prerequisites for [building Firefox](https://developer.mozilla.org/en-US/docs/Mozilla/Developer_guide/Build_Instructions) or [building SpiderMonkey](https://developer.mozilla.org/en-US/docs/Mozilla/Projects/SpiderMonkey/Build_Documentation). There are [additional requirements for building with Address Sanitizer](https://developer.mozilla.org/en-US/docs/Mozilla/Testing/Firefox_and_Address_Sanitizer).

After the addition of FuzzManager support, you will need to first install the pip packages listed in requirements.txt of [FuzzManager](https://github.com/MozillaSecurity/FuzzManager).

Here's a guide to [pip and virtualenv](https://www.dabapps.com/blog/introduction-to-pip-and-virtualenv-python/).

### Windows (only 64-bit supported)

1. Install [MozillaBuild](https://wiki.mozilla.org/MozillaBuild) (Using compileShell for SpiderMonkey requires at least version 2.2.0) to get an msys shell.
2. Install [Git for Windows](https://msysgit.github.io/) to get Git for Windows in order to clone these funfuzz repositories. (32-bit works best for now)
3. Install [Debugging Tools for Windows](https://msdn.microsoft.com/en-us/windows/hardware/hh852365.aspx) to get cdb.exe and thus stacks from crashes.
4. Make sure you install at least Microsoft Visual Studio 2015 (Community Edition is recommended) as per the build instructions above in the Setup section.
5. Run `start-shell-msvc2015.bat` to get a MSYS shell. Do not use the MSYS shell that comes with Git for Windows. You can use Git by calling its absolute path, e.g. `/c/Program\ Files\ \(x86\)/Git/bin/git.exe`.
    1. Run the batch file with administrator privileges to get gflags analysis working correctly.


### Mac

1. On Mac OS X 10.9, you must first install a newer version of unzip than the one that comes with the OS. (Old versions [hit an error](https://bugzilla.mozilla.org/show_bug.cgi?id=1032391) on large zip files, such as the "mac64.tests.zip" file that [downloadBuild.py](util/downloadBuild.py) grabs.)

  ```
  brew install homebrew/dupes/unzip
  brew link --force unzip
  ```

2. If you encounter problems accessing the compiler, try re-running this command:

  ```xcode-select --install```

especially after updating major/minor OS versions. This sometimes manifests on Mac OS X Combo updates.

3. Install LLVM via Homebrew, to get llvm-symbolizer needed for symbolizing ASan crash stacks.

  ```
  brew install llvm
  ```


### Linux

1. To ensure your core dumps don't get mixed up when multiple instances crash at the same time, run:

  ```
  echo -n 1 | sudo tee /proc/sys/kernel/core_uses_pid
  ```
2. Install 32-bit libraries to compile 32-bit binaries:
  * Debian/Ubuntu: ```sudo apt-get install lib32z1 gcc-multilib g++-multilib```
  * Fedora: (Fedora is known to work, however the exact library names are unknown for now.)
  ** Note that parts of the code which contain ```if isLinux and float(platform.linux_distribution()[1]) > 15.04``` might fail on Fedora, as they assume Ubuntu's versioning scheme. Patches welcome.
3. Install gdb:
  * Debian/Ubuntu: ```sudo apt-get install gdb```
  * Fedora: Please ensure that all development packages are installed (see ```rpm -qa "*devel"```), and run ```yum install gdb```
4. Install clang for clang/ASan builds:
  * Debian/Ubuntu: ```sudo apt-get install clang```


## Running domfuzz

*For the maintained version of jsfunfuzz, head to the [funfuzz](https://github.com/MozillaSecurity/funfuzz) repository.*


`python ./domfuzz/dom/automation/loopdomfuzz.py ~/build`


FuzzManager support got landed, so you will also need to create a ~/.fuzzmanagerconf file, similar to:

```
[Main]
serverhost = <your hostname>
serverport = <your port>
serverproto = https
serverauthtoken = <if any>
sigdir = /Users/<your username>/sigcache/
tool = jsfunfuzz
```

Replace anything between "<" and ">" with your desired parameters.

## FAQ:

**Q: What platforms does domfuzz run on?**

**A:** compileShell has been tested on:

* Windows 7 and Windows Server 2012 R2, with [MozillaBuild 2.2.0](https://wiki.mozilla.org/MozillaBuild)
  * Windows 10 seems to work fine with [MozillaBuild 2.2.0](https://wiki.mozilla.org/MozillaBuild) and some funfuzz fixes that have landed, but needs more testing
* Mac OS X 10.12
* Ubuntu 15.10 and later (best supported on 16.04 LTS)
* Ubuntu (and variants) on [ARM ODROID boards](http://www.hardkernel.com/main/main.php) are also known to work.

Fedora Linux has not been tested extensively and there may be a few bugs along the way.

The following operating systems are old/less common and while they may still work, be prepared to **expect issues** along the way:

* Windows Vista / Windows 8 / Windows 8.1
* Mac OS X 10.10 / 10.11
* Ubuntu Linux 14.04 LTS, 15.04 and prior

Support for the following operating systems **have been removed**:

* Windows XP
* Mac OS X 10.6 through 10.9

**Q:** What version of Python does domfuzz require?

**A:** We recommend the Python 2.7.x series. There is no support for Python3 yet.

**Q:** How do I reproduce a crash from a test case?

**A:**

The domfuzz way:

    python ./domfuzz/dom/automation/domInteresting.py ~/build ~/test_case.html

The manual way:

    mkdir -p ~/tmp_profile/extensions
    cp ./domfuzz/dom/automation/constant-prefs.js ~/tmp_profile/prefs.js
    echo ./domfuzz/dom/extension/ > ~/tmp_profile/extensions/domfuzz@squarefree.com
    lldb -- ~/build/dist/bin/firefox -profile ~/tmp_profile/ -no-remote ~/test_case.html
