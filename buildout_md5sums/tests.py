from os import listdir, remove
from os.path import isdir
from shutil import rmtree
import doctest
import unittest

def setUp():
    for afile in listdir('.'):
        if isdir(afile):
            rmtree(afile)
        else:
            remove(afile)

def test_suite():
    setUp()

    return unittest.TestSuite([
        doctest.DocFileSuite(
          'buildout_md5sums.rst',
          optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
        ),
    ])

