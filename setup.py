import os
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.txt')).read()

# allows setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="plrutils",
    version=open("VERSION").read().strip('\n'),
    description='A simple PLR helper.',
    long_description=README,
    license='FreeBSD License',
    url="https://bitbucket.org/dallagi/plrutils",
    author="Marco Dallagiacoma",
    author_email="dallagiac@fbk.eu",
    packages=['plrutils'],
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: FreeBSD License',  # cosi tanto per
        'Operating System :: OS Indipendent',
        'Framework :: Django',
    ],
    install_requires=["django"],
)

