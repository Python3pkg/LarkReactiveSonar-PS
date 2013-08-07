import os
from setuptools import setup, find_packages
import sys

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='LarkReactiveSonar-PS',
    version='1.0',
    author='Andrew Koerner',
    author_email='andrew@k0ner.com',
    packages=['LarkReactiveSonar'],
    scripts=[
        'LarkReactiveSonar/LarkReactiveSonar-PS.py',
      ],
    include_package_data=True,
    zip_safe=False,
    url='http://pypi.python.org/pypi/LarkReactiveSonar-PS/',
    license='APACHE 2',
    description='LarkSonar-PS system see git repository for more info.',
    long_description=open('README.md').read(),
    ) 
