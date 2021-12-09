from setuptools import setup

exec(open("the_project/version.py").read())
setup(version=__version__)
