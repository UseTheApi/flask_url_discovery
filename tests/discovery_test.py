#! /bin/usr/python3

from url_discovery import app_registry

import unittest
from flask import Flask

__author__ = "Alena Lifar"
__email__ = "alenaslifar@gmail.com"
__version__ = "0.0.1"
__phase__ = "alpha"
__date__ = "04/08/2017"


app = Flask("app1")


@app.route("/test/app", methods=["GET"])
def test_app():
    return "Testing APP"


test_response = """{"url_discovery.expose_routes": {"active_urls": "/config/routes/",
"methods": ["HEAD", "OPTIONS", "GET"]}, "test_app": {"active_urls": "/test/app",
"methods": ["HEAD", "OPTIONS", "GET"]}}"""


class TestDiscovery(unittest.TestCase):

    def setUp(self):
        self.registered_app = app_registry.url_registry(app).test_client()

    def test_UrlDiscovery(self):
        import json
        print()
        print("======== Testing Url Discovery ========")
        response = self.registered_app.get(app_registry.routes_url)
        print(response.data.decode("utf-8"))
        self.assertEquals(json.loads(test_response).keys(), json.loads(response.data.decode("utf-8")).keys())
