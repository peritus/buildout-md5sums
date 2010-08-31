
:Author: `Filip Noetzel <http://filip.noetzel.co.uk/>`__
:Web: http://github.com/peritus/buildout-md5sums/
:Git: ``git clone git://github.com/peritus/buildout-md5sums.git`` (`browse source <http://github.com/peritus/buildout-md5sums/>`__)
:Download: `Downloads page on GitHub <https://github.com/peritus/buildout-md5sums/downloads>`__

Simple usage
++++++++++++

Use a buildout.cfg like this and the md5sum for the download-python target will be checked::

    [buildout]
    extensions = buildout-md5sums
    md5sums =
      http://python.org/ftp/python/2.6.6/Python-2.6.6.tar.bz2 = 376df294ae16e9601da989f8c4d8d432
      http://python.org/ftp/python/2.7/Python-2.7.tar.bz2 = 0e8c9ec32abf5b732bea7d91b38c3339
    parts = download-python

    [versions]
    python = 2.6.6

    [download-python]
    recipe = hexagonit.recipe.download
    url = http://python.org/ftp/python/${versions:python}/Python-${versions:python}.tar.bz2

Using this setup, you can switch the downloaded version of python on the
command line while keeping the cryptographic checking alive::

    $ ./bin/buildout versions:python=2.7 install download-python

Disallowing downloads without md5sums
+++++++++++++++++++++++++++++++++++++

If your buildout.cfg like this, the extension will make the buildout fail if
there is a download using zc.buildout.download without a md5sum specified::

    [buildout]
    extensions = buildout-md5sums
    allow-picked-downloads = false
