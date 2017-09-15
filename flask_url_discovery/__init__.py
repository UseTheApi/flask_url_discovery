#! /bin/usr/python3

"""
    flask url discovery

    Flask extension that takes a responsibility to collect all
    available urls and expose them under one link.

    :copyright: (c) 2017 by Alena Lifar
    :license: MIT License
"""

from .app_registry import url_discovery
from .urls_privation import private

__author__ = "Alena Lifar"
__version__ = '1.1.1'
