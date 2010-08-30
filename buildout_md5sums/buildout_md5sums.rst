buildout-md5sums
================

>>> from zc.buildout.testing import _start_server, stop_server, write, mkdir, system, make_buildout
>>> from os import chdir, getcwd
>>> from os.path import dirname, join, normpath
>>> import urllib2
>>> port, thread = _start_server(join(dirname(__file__), 'testdata'))

>>> mkdir('sample_buildout')
>>> chdir('sample_buildout')
>>> make_buildout()

>>> mkdir('download-cache')
>>> values = dict(
...   develop=normpath(join(getcwd(), "..", "..", "..")),
...   port=port,
... )

>>> write('buildout.cfg', """\
... [buildout]
... develop = %(develop)s
... newest = false
... download-cache = download-cache
... parts = self
...
... [self]
... recipe = zc.recipe.egg
... eggs = buildout-md5sums
...
... """ % values)

>>> _  = system(join(getcwd(), 'bin', 'buildout'))

>>> write('buildout.cfg', """\
... [buildout]
... develop = %(develop)s
... newest = false
... extensions = buildout-md5sums
... download-cache = download-cache
... allow-picked-downloads = false
... parts = self unspecified
...
... [self]
... recipe = zc.recipe.egg
... eggs = buildout-md5sums
...
... [unspecified]
... recipe = hexagonit.recipe.download
... url = http://localhost:%(port)d/1dcca23355272056f04fe8bf20edfce0
... download-only = true
...
... """ % values)

>>> print '\n'.join(system(join(getcwd(), 'bin', 'buildout')).splitlines()[-5:])  # doctest: +REPORT_UDIFF
Picked: ...
Installing unspecified.
While:
  Installing unspecified.
Error: Attempting to download http://localhost:.../1dcca23355272056f04fe8bf20edfce0 without md5sum

The same behaviour is also observed when loading from cache:

>>> print '\n'.join(system(join(getcwd(), 'bin', 'buildout')).splitlines()[-5:])  # doctest: +REPORT_UDIFF
Picked: ...
Installing unspecified.
While:
  Installing unspecified.
Error: Attempting to download http://localhost:.../1dcca23355272056f04fe8bf20edfce0 without md5sum

You can specify the md5sum as part of the url in two ways:

>>> write('buildout.cfg', """\
... [buildout]
... develop = %(develop)s
... newest = false
... extensions = buildout-md5sums
... allow-picked-downloads = false
... download-cache = download-cache
... md5sums =
...   http://localhost:%(port)d/1dcca23355272056f04fe8bf20edfce0 = 1dcca23355272056f04fe8bf20edfce0
...   http://localhost:%(port)d/26ab0db90d72e28ad0ba1e22ee510510 = 12345
... parts = self specified specified-inline specified-inline2 specified-but-invalid
...
... [self]
... recipe = zc.recipe.egg
... eggs = buildout-md5sums
...
... [specified]
... recipe = hexagonit.recipe.download
... url = http://localhost:%(port)d/1dcca23355272056f04fe8bf20edfce0
... download-only = true
...
... [specified-inline]
... recipe = hexagonit.recipe.download
... url = http://localhost:%(port)d/6d7fce9fee471194aa8b5b6e47267f03#md5=6d7fce9fee471194aa8b5b6e47267f03
... download-only = true
...
... [specified-inline2]
... recipe = hexagonit.recipe.download
... url = http://localhost:%(port)d/b026324c6904b2a9cb4b88d6d61c81d1#md5sum=b026324c6904b2a9cb4b88d6d61c81d1
... download-only = true
...
... [specified-but-invalid]
... recipe = hexagonit.recipe.download
... url = http://localhost:%(port)d/26ab0db90d72e28ad0ba1e22ee510510
... download-only = true
...
... """ % values)

>>> print '\n'.join(system(join(getcwd(), 'bin', 'buildout')).splitlines()[18:])  # doctest: +REPORT_UDIFF
Searching cache at .../parts/test/sample_buildout/download-cache/
Cache miss; will cache http://localhost:.../1dcca23355272056f04fe8bf20edfce0 as .../parts/test/sample_buildout/download-cache/...
Downloading http://localhost:.../1dcca23355272056f04fe8bf20edfce0
Installing specified-inline.
Searching cache at .../parts/test/sample_buildout/download-cache/
Cache miss; will cache http://localhost:.../6d7fce9fee471194aa8b5b6e47267f03 as .../parts/test/sample_buildout/download-cache/...
Downloading http://localhost:.../6d7fce9fee471194aa8b5b6e47267f03
Installing specified-inline2.
Searching cache at .../parts/test/sample_buildout/download-cache/
Cache miss; will cache http://localhost:.../b026324c6904b2a9cb4b88d6d61c81d1 as .../parts/test/sample_buildout/download-cache/...
Downloading http://localhost:.../b026324c6904b2a9cb4b88d6d61c81d1
Installing specified-but-invalid.
Searching cache at .../parts/test/sample_buildout/download-cache/
Cache miss; will cache http://localhost:.../26ab0db90d72e28ad0ba1e22ee510510 as .../parts/test/sample_buildout/download-cache/...
Downloading http://localhost:.../26ab0db90d72e28ad0ba1e22ee510510
While:
  Installing specified-but-invalid.
Error: MD5 checksum mismatch downloading 'http://localhost:.../26ab0db90d72e28ad0ba1e22ee510510'


The same behaviour is also observed when loading from cache:

>>> print '\n'.join(system(join(getcwd(), 'bin', 'buildout')).splitlines()[-10:])  # doctest: +REPORT_UDIFF
Updating specified.
Updating specified-inline.
Updating specified-inline2.
Installing specified-but-invalid.
Searching cache at .../parts/test/sample_buildout/download-cache/
Cache miss; will cache http://localhost:.../26ab0db90d72e28ad0ba1e22ee510510 as .../parts/test/sample_buildout/download-cache/...
Downloading http://localhost:.../26ab0db90d72e28ad0ba1e22ee510510
While:
  Installing specified-but-invalid.
Error: MD5 checksum mismatch downloading 'http://localhost:.../26ab0db90d72e28ad0ba1e22ee510510'


>>> stop_server('http://localhost:%d/'%port)

