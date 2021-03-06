#!/usr/bin/env python3

from setuptools import find_packages, setup

# allow setup.py to be run from any path
# os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='i3wonderbar',
    packages=find_packages(where='src'),
    package_dir={'wonderbar': 'src/wonderbar'},
    version='1.0.0',
    include_package_data=True,
    scripts=['src/i3wonderbar'],
    license='GPL-3',
    description='',
    url='https://github.com/ezaquarii/i3wonderbar',
    author='Chris Narkiewicz',
    author_email='hello@ezaquarii.com',
    classifiers=[
        'Environment :: X11 Applications'
    ],
)