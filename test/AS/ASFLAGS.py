#!/usr/bin/env python
#
# MIT License
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

import sys

import TestSCons

_python_ = TestSCons._python_

test = TestSCons.TestSCons()
_exe = TestSCons._exe

test.file_fixture('mylink.py')
test.file_fixture(['fixture', 'myas_args.py'])

o = ' -x'
o_c = ' -x -c'

test.write('SConstruct', """
DefaultEnvironment(tools=[])
env = Environment(tools=['link','as'],
                  LINK = r'%(_python_)s mylink.py',
                  LINKFLAGS = [],
                  AS = r'%(_python_)s myas_args.py', ASFLAGS = '-x',
                  CC = r'%(_python_)s myas_args.py')
env.Program(target = 'test1', source = 'test1.s')
env.Program(target = 'test2', source = 'test2.S')
env.Program(target = 'test3', source = 'test3.asm')
env.Program(target = 'test4', source = 'test4.ASM')
env.Program(target = 'test5', source = 'test5.spp')
env.Program(target = 'test6', source = 'test6.SPP')
""" % locals())

test.write('test1.s', r"""This is a .s file.
#as
#link
""")

test.write('test2.S', r"""This is a .S file.
#as
#link
""")

test.write('test3.asm', r"""This is a .asm file.
#as
#link
""")

test.write('test4.ASM', r"""This is a .ASM file.
#as
#link
""")

test.write('test5.spp', r"""This is a .spp file.
#as
#link
""")

test.write('test6.SPP', r"""This is a .SPP file.
#as
#link
""")

test.run(arguments = '.', stderr = None)

if TestSCons.case_sensitive_suffixes('.s', '.S'):
    o_css = o_c
else:
    o_css = o

test.must_match('test1' + _exe, "%s\nThis is a .s file.\n" % o)
test.must_match('test2' + _exe, "%s\nThis is a .S file.\n" % o_css)
test.must_match('test3' + _exe, "%s\nThis is a .asm file.\n" % o)
test.must_match('test4' + _exe, "%s\nThis is a .ASM file.\n" % o)
test.must_match('test5' + _exe, "%s\nThis is a .spp file.\n" % o_c)
test.must_match('test6' + _exe, "%s\nThis is a .SPP file.\n" % o_c)

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
