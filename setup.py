from setuptools import setup
import re

with open('dcss/__init__.py', 'r') as f:
    version = re.search(r"__version__ = '(.*)'", f.read()).group(1)

setup(
    name='dcss',
    version=version,
    license='MIT',
    url='https://github.com/AustralianSynchrotron/pydcss',
    packages=['dcss'],
)
