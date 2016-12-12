#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='group_optimizer',
    version='0.1',
    description='Optimal grouping utilities and algorithms.',
    author='Eric Ihli',
    author_email='eihli@owoga.com',
    url='https://github.com/eihli/group_optimizer',
    tests_require=['nose'],
    packages=['group_optimizer'],
    )
