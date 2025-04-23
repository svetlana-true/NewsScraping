# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='news-scraping',
    version='0.1.0',
    description='Package for news scraping',
    long_description=readme,
    author='Svetlana Pivtoratskaia',
    author_email='svetlana.true.zr@gmail.com',
    url='https://github.com/',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)