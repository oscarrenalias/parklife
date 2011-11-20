#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 Oscar Renalias
#
# Licensed under GNU General Public License version 3:
# http://www.gnu.org/licenses/gpl-3.0.txt
#

import unittest
from app.tests.utils import TestUtils
from app.tests.viewhelpers import TestViewHelpers
from app.tests.forms import TestForms
from app.tests.services import *

#		
# If run from command line, run all tests
#
# Alternatively, module-specific texts can be run like this:
#	python -m unittest app.tests.forms
#
# Where app.tests.forms is a module with test classes
#
if __name__ == '__main__':
    unittest.main()