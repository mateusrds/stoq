# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

##
## Copyright (C) 2011 Async Open Source <http://www.async.com.br>
## All rights reserved
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., or visit: http://www.gnu.org/.
##
## Author(s): Stoq Team <stoq-devel@async.com.br>
##

import os
import unittest

import pylint.__pkginfo__

import stoqlib
from stoqlib.lib.process import Process


DISABLED = [
    # Reports
    'similarities',  # Similarity report

    # Convention
    'C0103',  # Invalid name "xxx" for type variable
              #  (should match [a-z_][a-z0-9_]{2,30}$)
    'C0111',  # Missing docstring
    'C0202',  # Class method xxx should have 'cls' as first argument
    'C0301',  # Line too long
    'C0302',  # Too many lines in module
    'C0322',  # Operator not preceded by a space

    # Errors
    'E1002',  # Use of super on an old style class
    'E1101',  # Instance of XXX has no yyy member
    'E1102',  # TODO: class is not callable
    'E1103',  # Instance of XXX has no yyy member (some not inferred)
    'E1120',  # No value passed for parameter 'xxx' in function call
    'E1121',  # TODO: Too many positional arguments for function call
    'E0211',  # Method has no argument - Interfaces
    'E0213',  # Method should have "self" as first argument - Interfaces
    'E0611',  # Pylint is confused about modules it cannot import
    'E0702',  # Raising NoneType while only classes, instances or string
    'E0710',  # Raising a new style class which doesn't inherit from Base

    # Fatal
    'F0401',  # Unable to import 'gudev'

    # Info
    'I0011',  # Locally disabling

    # Refactor
    'R0201',  # Method could be a function
    'R0901',  # Too many ancestors
    'R0902',  # Too many instance attributes
    'R0903',  # Too few public methods
    'R0904',  # Too many public methods
    'R0911',  # Too many return statements
    'R0912',  # Too many branches
    'R0913',  # Too many arguments
    'R0915',  # Too many statements
    'R0914',  # Too many local variables
    'R0921',  # TODO: Abstract class not referenced
    'R0922',  # Abstract class is only referenced 1 times

    # Warnings
    'W0101',  # TODO: Unreachable code
    'W0102',  # Dangerous default value [] as argument
    'W0104',  # Statement seems to have no effect
    'W0105',  # String statement has no effect
    'W0109',  # TODO: Duplicate key 'XX' in dictionary
    'W0141',  # TODO: Used builtin function 'map'
    'W0142',  # Used * or ** magic
    'W0201',  # Attribute 'loaded_uis' defined outside __init__
    'W0212',  # Method could be a function (SQLObject from/to_python)
    'W0222',  # Signature differs from overriden method
    'W0221',  # Arguments number differs from overriden method
    'W0223',  # Method 'add' is abstract in class 'xxx' but is not overriden
    'W0231',  # __init__ method from base class is not called
    'W0232',  # Class has no __init__ method
    'W0233',  # __init__ method from a non direct base class is called
    'W0311',  # TODO: Bad indentation
    'W0402',  # Uses of a deprecated module 'string'
    'W0404',  # TODO: Reimport 'XX'
    'W0511',  # FIXME/TODO/XXX
    'W0602',  # Using global for 'xxx' but no assignment is done
    'W0603',  # Using the global statement
    'W0612',  # Unused variable
    'W0613',  # Unused argument
    'W0621',  # Redefining name 'xxx' from outer scope
    'W0622',  # Redefined built-in variable
    'W0623',  # Redefining name 'xxx' from outer scope in exception handler
    'W0631',  # Using possibly undefined loop variable
    'W0702',  # No exception type(s) specified
    'W0703',  # Catching too general exception Exception
    'W0704',  # Except doesn't do anything
    'W1401',  # Anomalous backslash in string: '\d'
]

if pylint.__pkginfo__.numversion >= (0, 26):
    DISABLED.append('R0924')  # TODO: Badly implemented Container


class TestPylint(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.root = os.path.dirname(
            os.path.dirname(stoqlib.__file__)) + '/'

    def pylint(self, modules, args=None):
        if not args:
            args = []
        args = ["pylint",
                "--dummy-variables=unused,_",
                "--disable=%s" % (",".join(DISABLED)),
                "--include-ids=y",
                "--rcfile=%s/tools/pylint.rcfile" % (self.root,),
                "--reports=n"] + args + modules
        p = Process(args)
        retval = p.wait()
        if retval:
            raise Exception("Pylint errors")

    def test_stoq(self):
        self.pylint(["stoq"])

    def test_stoqlib(self):
        self.pylint(["stoqlib.database",
                     "stoqlib.drivers",
                     "stoqlib.exporters",
                     "stoqlib.gui",
                     "stoqlib.importers",
                     "stoqlib.l10n",
                     "stoqlib.lib",
                     "stoqlib.migration",
                     "stoqlib.net",
                     "stoqlib.reporting"])

    def test_stoqlib_domain(self):
        self.pylint(["stoqlib.domain"],
                    args=["--load-plugins",
                          "tools/pylint_stoq",
                          "--enable=E1101"])

    def test_plugins(self):
        self.pylint(["plugins"])
