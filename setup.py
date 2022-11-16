from setuptools import setup

setup(
   name = 'DBDIpy',
   version = '1.0.0',
   author = 'Leopold Weidner',
   author_email = 'leopold.weidner@tum.de',
   packages = ['DBDIpy', 'DBDIpy.tests'],
   url = 'https://github.com/leopold-weidner/DBDIpy',
   license = 'docs/license.txt',
   description =    'A python package for the curation and interpretation of dielectric barrier discharge ionisation mass spectrometric datasets.',
   long_description_content_type='text/markdown',
   long_description = open('README.md').read(),
   keywords=['python', 'bioinformatics', 'mass spectrometry', 'metabolomics', 'foodomics'],
   classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
   install_requires=[
       "pandas",
       "numpy",
       "tqdm",
       "matchms",
       "matplotlib",
       "pytest",
       "scipy",
       "feather-format",
   ],
)
