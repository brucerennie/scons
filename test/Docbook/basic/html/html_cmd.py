#!/usr/bin/env python
#
# Copyright (c) 2001-2010 The SCons Foundation
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
#

"""
Test the HTML builder while using
the xsltproc executable, if it exists.
"""

import TestSCons

test = TestSCons.TestSCons()

xsltproc = test.where_is('xsltproc')
if not xsltproc:
    test.skip_test('No xsltproc executable found, skipping test.\n')

test.dir_fixture('image')

# Normal invocation
test.run(arguments=['-f','SConstruct.cmd','DOCBOOK_XSLTPROC=%s'%xsltproc], stderr=None)
test.must_not_be_empty(test.workpath('manual.html'))

# Cleanup
test.run(arguments=['-f','SConstruct.cmd','-c','DOCBOOK_XSLTPROC=%s'%xsltproc])
test.must_not_exist(test.workpath('manual.html'))

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
