import setuptools


with open('README.md', 'r') as fh:
    long_description = fh.read()


setuptools.setup(
    name='django-nonrelated-inlines',
    version='0.0.1',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bhomnick/django-nonrelated-inlines',
    packages=setuptools.find_packages(),
    install_requires=[
    ],
    python_requires='>=3.6',
)
