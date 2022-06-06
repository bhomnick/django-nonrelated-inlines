import os
import sys

import setuptools
from setuptools.command.install import install


with open('README.md', 'r') as fh:
    long_description = fh.read()


VERSION = '0.2'


class VerifyVersion(install):

    def run(self):
        tag = os.getenv('CIRCLE_TAG')
        if tag != VERSION:
            sys.exit('Git tag: {0} does not match the version of this app: {1}'.format(
                tag, VERSION))


setuptools.setup(
    name='django-nonrelated-inlines',
    version=VERSION,
    description='Django admin inlines for unrelated models',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bhomnick/django-nonrelated-inlines',
    author='Ben Homnick',
    author_email='bhomnick@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Flake8',
        'Framework :: tox',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=setuptools.find_packages(),
    install_requires=[
        'Django>=2.0'
    ],
    python_requires='>=3.6',
    cmdclass={
        'verify': VerifyVersion,
    }
)
