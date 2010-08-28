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
... """ % normpath(join(getcwd(), "..", "..", "..")))

>>> print system(join(getcwd(), 'bin', 'buildout')),  # doctest: +REPORT_UDIFF
Installing 'zc.buildout', '...'.
We have the best distribution that satisfies 'zc.buildout'.
Picked: zc.buildout = ...
We have the best distribution that satisfies '...'.
Picked: ...
Upgraded:
  zc.buildout version ...,
  setuptools version ...;
restarting.
Installing 'zc.buildout', '...'.
We have the best distribution that satisfies 'zc.buildout'.
Picked: zc.buildout = ...
We have the best distribution that satisfies '...'.
Picked: setuptools = ...
Develop: '...'
Installing 'zc.recipe.egg'.
We have the best distribution that satisfies 'zc.recipe.egg'.
Picked: zc.recipe.egg = ...
Installing self.
Installing 'buildout-md5sums'.
We have a develop egg: buildout-md5sums ...

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

>>> print system(join(getcwd(), 'bin', 'buildout')),  # doctest: +REPORT_UDIFF
Installing 'buildout-md5sums'.
We have a develop egg: buildout-md5sums ...
Don't allow picking downloads that have no md5sums
Installing 'zc.buildout', '...'.
We have the best distribution that satisfies 'zc.buildout'.
Picked: zc.buildout = ...
We have the best distribution that satisfies '...'.
Picked: ...
Develop: '...'
Installing 'zc.recipe.egg'.
We have the best distribution that satisfies 'zc.recipe.egg'.
Picked: zc.recipe.egg = ...
Installing 'hexagonit.recipe.download'.
We have the best distribution that satisfies 'hexagonit.recipe.download'.
Picked: hexagonit.recipe.download = ...
Updating self.
Installing 'buildout-md5sums'.
We have a develop egg: buildout-md5sums ...
Getting required 'zc.buildout==...'
  required by buildout-md5sums ...
We have the distribution that satisfies 'zc.buildout==...'.
Getting required 'setuptools'
  required by zc.buildout ...
We have the best distribution that satisfies 'setuptools'.
Picked: setuptools = ...
Installing test1.
While:
  Installing test1.
Error: Attempting to download http://localhost:.../1dcca23355272056f04fe8bf20edfce0 without md5sum

>>> stop_server('http://localhost:%d/'%port)

