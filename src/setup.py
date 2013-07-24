from distutils.core import setup

setup(
    name='LarkReactiveSonar-PS',
    version='0.1.0',
    author='A. Koerner',
    author_email='andrew@k0ner.com',
    packages=['towelstuff', 'towelstuff.test'],
    scripts=[
	     'bin/stowe-towels.py',
	     'bin/wash-towels.py'
	    ],
    url='http://pypi.python.org/pypi/LarkReactiveSonar-PS/',
    license='LICENSE',
    description='LarkSonar-PS system see git repository for more info.',
    long_description=open('README.md').read(),
    )
