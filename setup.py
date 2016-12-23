"""Setup script of newsboard"""
from setuptools import setup, find_packages
import newsboard


def read(filename):
    with open(filename) as fd:
        return fd.read()

setup(
    name='newsboard',
    version=newsboard.__version__,
    description=newsboard.__doc__,
    long_description=read('README.rst'),
    keywords=['web', 'django', 'opengraph', 'web-rich-object', 'facebook',
              'rss', 'sitemap'],
    author=newsboard.__author__,
    author_email=newsboard.__email__,
    url=newsboard.__url__,

    packages=find_packages(),
    classifiers=[
        'Framework :: Django',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries :: Python Modules'],

    license=newsboard.__license__,
    include_package_data=True,
    zip_safe=False,
    install_requires=read('requirements.txt').splitlines(),
)
