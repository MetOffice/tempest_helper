# (C) British Crown Copyright 2022, Met Office.
# Please see LICENSE for license details.
import os
import setuptools


def get_long_description():
    """Use the contents of README.md as the long description"""
    with open("README.md", "r") as fh:
        return fh.read()


def extract_version():
    """
    Retrieve version information from the  __init__.py module.
    """
    version = ""
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, "tempest_helper", "__init__.py")

    with open(filename) as fd:
        for line in fd:
            line = line.strip()
            if line.startswith("__version__"):
                try:
                    version = line.split("=")[1].strip(" \"'")
                except Exception:
                    pass
                break

    if not version:
        print(f"WARNING: Unable to parse version information from file: {filename}")
        version = "0.0.0"

    return version


setuptools.setup(
    name="tempest_helper",
    packages=["tempest_helper"],
    version=extract_version(),
    license="BSD 3-Clause License",
    description=(
        "tempest_helper is a Python module for the easier manipulation of "
        "TempestExtremes data."
    ),
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Met Office",
    author_email="jon.seddon@metoffice.gov.uk",
    url="https://github.com/MetOffice/tempest_helper",
    download_url="https://github.com/MetOffice/tempest_helper/releases",
    keywords=["TempestExtremes", "climate", "tracking"],
    install_requires=[
        "scitools-iris",
        "matplotlib",
        "Cartopy",
        "cftime",
        "numpy",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
