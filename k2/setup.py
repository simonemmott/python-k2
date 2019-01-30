'''
Created on 30 Jan 2019

@author: simon
'''
from setuptools import setup, find_packages

setup(
    name='k2',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        k2=k2.cli:k2
    ''',
)