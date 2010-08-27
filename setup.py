from setuptools import setup

setup(
    packages = ['buildout_md5sums'],
    name = "buildout-md5sums",
    entry_points = {
       'zc.buildout.extension': ['ext = buildout_md5sums:ext'],
       'zc.buildout.unloadextension': ['ext = buildout_md5sums:unload'],
       },
    )
