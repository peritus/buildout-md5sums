from setuptools import setup

import buildout_md5sums

name = "buildout-md5sums"

setup(
    author='Filip Noetzel',
    author_email='filip+pypi@j03.de',
    license='Beerware',
    name=name,
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
       'zc.buildout.extension': ['ext = buildout_md5sums:ext'],
       'zc.buildout.unloadextension': ['ext = buildout_md5sums:unload'],
       },
    )

