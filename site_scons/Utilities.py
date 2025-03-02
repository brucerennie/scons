# SPDX-License-Identifier: MIT
#
# Copyright The SCons Foundation

import os
import stat
import time
import sysconfig

platform = sysconfig.get_platform()

def is_windows() -> bool:
    """Check if we're on a Windows platform"""
    return platform.startswith('win')


def whereis(filename):
    """
    An internal "whereis" routine to figure out if a given program
    is available on this system.
    """
    exts = ['']
    if is_windows():
        exts += ['.exe']
    for dir in os.environ['PATH'].split(os.pathsep):
        f = os.path.join(dir, filename)
        for ext in exts:
            f_ext = f + ext
            if os.path.isfile(f_ext):
                try:
                    st = os.stat(f_ext)
                except:
                    continue
                if stat.S_IMODE(st.st_mode) & stat.S_IXUSR:
                    return f_ext
    return None


# Datestring for debian
# Should look like: Mon, 03 Nov 2016 13:37:42 -0700
deb_date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
