#! /bin/usr/python3

from url_discovery import app_registry
import json

import unittest
from flask import Flask
from http import HTTPStatus

import responses

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
        """
        Url Discovery Test evaluates a response from registered test flask app.
        After registration new blueprint is added to an app collecting all available routes
        :return: void
        """
        print()
        print("======== Testing Url Discovery ========")
        response_obj = self.registered_app.get(app_registry.routes_url)
        print(response_obj.data.decode("utf-8"))
        self.assertEquals(json.loads(test_response).keys(), json.loads(response_obj.data.decode("utf-8")).keys())

    @responses.activate
    def test_ObtainUrls(self):
        """
        Obtain Urls Test checks parsing data from provided sources
        format of params to obtain_urls *args: str - host:port
        :return: void
        """
        print()
        print("======= Testing Obtain Urls ========")
        responses.add(
                responses.GET, 
                'http://localhost:5000/config/routes/',
                json=json.loads(test_response),
                status=HTTPStatus.OK,
                content_type='application_json'
        )
        success, urls, traceback = app_registry.obtain_urls('localhost:5000', 'localhost:5000')
        self.assertTrue(success)
        self.assertFalse(traceback)
        print(urls)
        for item in urls.values():
            self.assertEquals(json.loads(test_response).keys(), item.keys())
