#!/bin/env python

from distutils.core import setup
from brpc import version_str

setup(
    name="BRPC",
    version=version_str,
    packages=["brpc"],
    author="Jonathan Knapp (Thann)",
    author_email="jaknapp8@gmail.com",
    url="https://github.com/bcoin-org/brpc.py",
    license="MIT",
    description="A binary-only RPC protocol for websockets (think socket.io, only faster).",
    long_description="A binary-only RPC protocol for websockets (think socket.io, only faster).",
    # classifiers=[
    #     ""
    # ],
    # scripts=[''],
    #TODO: this doesn't work
    package_dir={"brpc": ""},
    # These go into the python install directory,
    package_data={"brpc": ['README.md', 'brpc']}
    # These go into the OS directory (/usr/ or C:\Python27\)
    # data_files={}
)
