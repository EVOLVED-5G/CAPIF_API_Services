# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "access_control_policy"
VERSION = "1.0.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "connexion>=2.0.2",
    "swagger-ui-bundle>=0.0.2",
    "python_dateutil>=2.6.0"
]

setup(
    name=NAME,
    version=VERSION,
    description="CAPIF_Access_Control_Policy_API",
    author_email="",
    url="",
    keywords=["OpenAPI", "CAPIF_Access_Control_Policy_API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['openapi/openapi.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['access_control_policy=access_control_policy.__main__:main']},
    long_description="""\
    API for access control policy. © 2021, 3GPP Organizational Partners (ARIB, ATIS, CCSA, ETSI, TSDSI, TTA, TTC). All rights reserved. 
    """
)

