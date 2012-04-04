#!/usr/bin/env python
from setuptools import setup, find_packages

import yell

METADATA = dict(
    name='yell',
    version=yell.__version__,
    author='Alen Mujezinovic',
    author_email='flashingpumpkin@gmail.com',
    description='User notification library with pluggable backends. Compatible with popular frameworks such as Django, Flask, Celery.',
    long_description=open('README.rst').read(),
    url='https://github.com/caffeinehit/yell',
    keywords='django flask celery user notifications yell buffalo',
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Environment :: Web Environment',
        'Environment :: Other Environment',
        'Environment :: X11 Applications',
        'Framework :: Django',
        'Framework :: Paste',
        'Framework :: Pylons',
        'Framework :: TurboGears',
        'Framework :: Twisted',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Communications',
        'Topic :: Communications :: Email',
        'Topic :: Database',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    packages=find_packages(),
    test_suite='yell.tests',
)

if __name__ == '__main__':
    setup(**METADATA)
