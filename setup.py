from setuptools import setup, find_packages
from pocketlab.methods.config import inject_init

init_path = 'pocketlab/__init__.py'
readme_path = 'README.rst'
setup_kwargs = {
    'include_package_data': True, # Checks MANIFEST.in for explicit rules
    'packages': find_packages(),
    'install_requires': [
        'jsonmodel',
        'labpack',
        'tabulate>=0.7.7',
        'ruamel.yaml>=0.14.12'
    ],
    'classifiers': [
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5'
    ]
}
setup_kwargs = inject_init(init_path, readme_path, setup_kwargs)
setup(**setup_kwargs)

''' DOCUMENTATION
References:
https://docs.python.org/3.6/distutils/setupscript.html

https://python-packaging-user-guide.readthedocs.org/en/latest/
https://docs.python.org/3.5/distutils/index.html
https://github.com/jgehrcke/python-cmdline-bootstrap
http://www.pyinstaller.org/

Installation Packages:
pip install wheel
pip install twine

Build Distributions:
python setup.py sdist --format=gztar,zip
pip wheel --no-index --no-deps --wheel-dir dist dist/pocketlab-0.3.tar.gz

Upload (or Register) Distributions to PyPi:
twine upload dist/[module-version]*

Upload Documentation to Github:
mkdocs gh-deploy
.gitconfig [credential] helper = wincred

Installation:
pip install [module]
python setup.py develop  # for local on-the-fly file updates
python setup.py install  # when possessing distribution files
pip install dist/pocketlab-0.3-py3-none-any.whl # when possessing wheel file

Uninstall:
pip uninstall [module]
python setup.py develop --uninstall # for removing symbolic link
# remove command line tool in ../Python/Python35-32/Scripts/

CLI Installation:
command = 'name of command'
module = 'name of module'
entry_points = {
    "console_scripts": ['%s = %s.cli:cli' % (command, module)]
},

System Installation:
# http://www.pyinstaller.org/

Mercurial Dev Setup:
.hgignore (add dist/, *.egg-info/, '.git/')
hgrc [paths] default = ssh://hg@bitbucket.org/collectiveacuity/pocketlab

Git Public Setup:
.gitignore (add dist/, *.egg-info/, dev/, tests_dev/, docs/, docs_dev/, .hg/, .hgignore)
git init
git remote add origin git@github.com:collectiveacuity/pocketLab.git

Git Public Updates:
git add -A
git commit -m 'updates'
git push origin master

Git Remove History: [Run as admin and pause syncing]
git filter-branch --force --index-filter 'git rm -rf --cached --ignore-unmatch dev/*' --prune-empty --tag-name-filter cat -- --all
'''