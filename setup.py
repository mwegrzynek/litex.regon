# -*- encoding: UTF-8 -*-
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()

requires = [
    'setuptools',
    'requests',
    'lxml'
]

version = '1.0.3'

setup(
    name='litex.regon',
    version=version,
    description='An API for accessing a Polish REGON database',
    long_description=README,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Database :: Front-Ends"
    ],
    author='Michal Wegrzynek',
    author_email='mwegrzynek@litex.pl',
    url='http://litexservice.pl',
    license='GPL',
    keywords='regon soap database',
    package_dir={'': 'src'},
    namespace_packages=['litex'],
    packages=find_packages('src'),
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    install_requires=requires,
    tests_require=['nose']
)
