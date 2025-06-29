#!/usr/bin/env python
#
# Copyright The SCons Foundation
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
Regression test for issue #4730: almost the same as force_scons_callback
function, but uses a target name with a space in it, to make sure
quoting is handled correctly all the way through.
"""

import os

import TestSCons
from TestCmd import IS_WINDOWS

test = TestSCons.TestSCons()

try:
    import ninja
except ImportError:
    test.skip_test("Could not find module in python")

_python_ = TestSCons._python_
_exe = TestSCons._exe

ninja_bin = TestSCons.NINJA_BINARY

test.dir_fixture("ninja-fixture")

test.file_fixture(
    "ninja_test_sconscripts/sconstruct_force_scons_callback-4730", "SConstruct"
)

# generate simple build
test.run(stdout=None)
test.must_contain_all_lines(test.stdout(), ["Generating: build.ninja"])
test.must_contain_all(test.stdout(), "Executing:")
test.must_contain_all(test.stdout(), "ninja%(_exe)s -f" % locals())
defers = test.stdout().count("Defer to SCons to build")
if not defers:
    test.fail_test(message="Did not see expected 'Defer to SCons' message.")
if defers > 1:
    test.fail_test(message=f"Too many 'Defer to SCons' messages {defers}).")
test.must_match("out.txt", "foo.c" + os.linesep)
test.must_match("out words.txt", "test2.cpp" + os.linesep)

# clean build and ninja files
test.run(arguments="-c", stdout=None)
test.must_contain_all_lines(
    test.stdout(),
    ["Removed out.txt", "Removed out words.txt", "Removed build.ninja"]
)

# only generate the ninja file
test.run(arguments="--disable-execute-ninja", stdout=None)
test.must_contain_all_lines(test.stdout(), ["Generating: build.ninja"])
test.must_not_exist(test.workpath("out.txt"))
test.must_not_exist(test.workpath("out words.txt"))

# run ninja independently
program = test.workpath("run_ninja_env.bat") if IS_WINDOWS else ninja_bin
test.run(program=program, stdout=None)
defers = test.stdout().count("Defer to SCons to build")
if not defers:
    test.fail_test(message=f"Too many 'Defer to SCons' messages {defers}).")
if defers > 1:
    test.fail_test(message="Too many 'Defer to SCons' messages.")
test.must_match("out.txt", "foo.c" + os.linesep)
test.must_match("out words.txt", "test2.cpp" + os.linesep)

# only generate the ninja file with specific NINJA_SCONS_DAEMON_PORT
test.run(arguments="PORT=9999 --disable-execute-ninja", stdout=None)
# Verify that port # propagates to call to ninja_run_daemon.py
test.must_contain(test.workpath("build.ninja"), "PORT = 9999")

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
