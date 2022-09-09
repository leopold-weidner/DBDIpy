from setuptools import setup

 setup(
   name = 'dbdiLW',
   version = '0.1.0',
   author = 'Leopold Weidner',
   author_email = 'leopold.weidner@tum.de',
   packages = ['dbdiLW', 'dbdiLW.test'],
   scripts = ['bin/tutorial'],
   url = 'http://pypi.python.org/pypi/PackageName/',
   license = 'docs/license.txt',
   description =    'A python package for the curation and interpretation of dielectric barrier discharge ionisation 
                    mass spectrometric datasets.',
   long_description = open('README.md').read(),
   install_requires=[
       "Django >= 1.1.1",
       "pytest",
   ],
)