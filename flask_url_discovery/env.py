#! /bin/usr/python3

from flask import Blueprint

__author__ = "Alena Lifar"
__email__ = "alenaslifar@gmail.com"
__version__ = "0.0.1"
__phase__ = "alpha"
__date__ = "04/08/2017"

UD_PATTERN = "flask_url_discovery"

default_routes_url = '/config/routes/'
blue_url_discovery = Blueprint(UD_PATTERN, __name__)

