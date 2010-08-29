buildout-md5sums
================

>>> from zc.buildout.testing import _start_server, stop_server, write, mkdir, system, make_buildout
>>> from os import chdir, getcwd
>>> from os.path import dirname, join, normpath
>>> import urllib2
>>> port, thread = _start_server(join(dirname(__file__), 'testdata'))

>>> def get(path):
...     return urllib2.urlopen('http://localhost:%d%s' % (port, path)).read()

>>> get('/1dcca23355272056f04fe8bf20edfce0')
'5\n'

>>> sample_buildout = 'sample_buildout'

>>> mkdir(sample_buildout)
>>> chdir(sample_buildout)
>>> make_buildout()

>>> write('buildout.cfg',
... """\
... [buildout]
... develop = %s
... parts =
...   self
...
... [self]
... recipe = zc.recipe.egg
... eggs = buildout-md5sums
...
... """ % normpath(join(getcwd(), "..", "..", "..")))

>>> print '\n'.join(system(join(getcwd(), 'bin', 'buildout')).splitlines()[-5:])  # doctest: +REPORT_UDIFF
We have the distribution that satisfies 'zc.buildout==...'.
Getting required '...'
  required by zc.buildout ...
We have the best distribution that satisfies '...'.
Picked: ...

>>> write('buildout.cfg',
... """\
... [buildout]
... develop = %s
... extensions = buildout-md5sums
... parts =
...   self
...   test1
...
... [self]
... recipe = zc.recipe.egg
... eggs = buildout-md5sums
...
... [test1]
... recipe = hexagonit.recipe.download
... url = http://localhost:%d/1dcca23355272056f04fe8bf20edfce0
... download-only = true
... """ % (normpath(join(getcwd(), "..", "..", "..")), port))

>>> print '\n'.join(system(join(getcwd(), 'bin', 'buildout')).splitlines()[-5:])  # doctest: +REPORT_UDIFF
Picked: ...
Installing test1.
While:
  Installing test1.
Error: Attempting to download http://localhost:.../1dcca23355272056f04fe8bf20edfce0 without md5sum

>>> stop_server('http://localhost:%d/'%port)

