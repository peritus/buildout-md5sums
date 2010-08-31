from setuptools import setup
from os.path import join, dirname

import buildout_md5sums

description = (
  'A zc.builout extension that allows you to specify and '
  'enforce md5 checksums for all downloads'
)

long_description = open(join(dirname(__file__), "README.rst")).read()

name = "buildout-md5sums"

setup(
    author='Filip Noetzel',
    author_email='filip+pypi@j03.de',
    license='Beerware',
    name=name,
    long_description=long_description,
    description=description,
    packages = ['buildout_md5sums'],
    url='http://www.python.org/pypi/'+name,
    version = ".".join(str(n) for n in buildout_md5sums.__VERSION__),
    install_requires = [
        'zc.buildout<=1.5.1',
    ],
    extras_require = dict(
        test=[
            'distribute==0.6.14',
            'junitxml==0.5',
            'python-subunit==0.0.6',
            'tornado==1.0',
            'zope.testing==3.10.0',
            'zc.buildout==1.5.0',
            ],
        ),
    entry_points = {
       'zc.buildout.extension': ['ext = buildout_md5sums.plugin:ext'],
       'zc.buildout.unloadextension': ['ext = buildout_md5sums.plugin:unload'],
       },
    )

