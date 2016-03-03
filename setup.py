__author__ = 'rcj1492'
__created__ = '2016.02'

import re
from setuptools import setup, find_packages

'''
References:
https://python-packaging-user-guide.readthedocs.org/en/latest/
https://docs.python.org/3.5/distutils/index.html
https://github.com/jgehrcke/python-cmdline-bootstrap

Installation Packages:
pip install wheel
pip install twine

Build Distributions:
python setup.py sdist --format=gztar,zip bdist_wheel

Upload Distributions to PyPi:
twine register dist/*
twine upload dist/*

Installation:
pip install [module]
python setup.py develop  # for local on-the-fly file updates
python setup.py install  # when possessing distribution files

Uninstall:
pip uninstall [module]
python setup.py develop --uninstall # for removing symbolic link

Old Methods:
python setup.py sdist bdist_wheel upload  # for PyPi
pip wheel --no-index --no-deps --wheel-dir dist dist/*.tar.gz
'''

version = re.search(
    "^__version__\s*=\s*'(.*)'",
    open('labMgmt/cli.py').read(),
    re.M
    ).group(1)

command = re.search(
    "^__command__\s*=\s*'(.*)'",
    open('labMgmt/cli.py').read(),
    re.M
    ).group(1)

setup(
    name="labMgmt",
    version=version,
    author = __author__,
    maintainer_email="support@collectiveacuity.com",
    entry_points = {
        "console_scripts": ['%s = labMgmt.cli:cli' % command]
    },
    include_package_data=True,  # Checks MANIFEST.in for explicit rules
    packages=find_packages(exclude=['cred','docs','keys','models','notes','tests']),  # Needed for bdist
    license="MIT",
    description="A Collection of Methods for Managing Laboratory Projects",
    long_description=open('README.rst').read(),
    install_requires=[
        "jsonmodel>=1.0"
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5'
    ]
)
