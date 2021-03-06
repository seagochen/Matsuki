#!/usr/bin/evn python
#coding=utf-8

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="matsuki",
    version="0.0.5",
    author="Orlando Chen",
    author_email="seagochen@hotmail.com",
    description="A collection of tools that may be used to help users coding with flask in an easy way",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seagochen/Matsuki",
    packages=setuptools.find_packages(),
    install_requires=["flask", "siki", "pymysql", "redis"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
