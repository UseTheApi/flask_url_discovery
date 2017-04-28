#! /bin/usr/python3

from url_discovery.app_registry import url_registry, UrlDiscovery, obtain_urls
import json

import unittest
from flask import Flask, Blueprint
from http import HTTPStatus

import time
from multiprocessing import Process
import responses
import requests

__author__ = "Alena Lifar"
__email__ = "alenaslifar@gmail.com"
__version__ = "0.0.1"
__phase__ = "alpha"
__date__ = "04/08/2017"


TEST_HOST = "0.0.0.0"
PRIVATE_RULE="/test/app/"
PRIVATE_BLUEPRINT="app_b"


app = Flask("app1")
url_registry(app)  # Url Registry for app. Allows to private routes and expose routes on /config/routes/


@app.route("/test/app", methods=["GET"])
def test_app():
    return "Testing APP"


test_response = """{"url_discovery.expose_routes": {"active_url": "/config/routes/",
"methods": ["HEAD", "OPTIONS", "GET"]}, "test_app": {"active_url": "/test/app",
"methods": ["HEAD", "OPTIONS", "GET"]}}"""


@UrlDiscovery.private()
@app.route(PRIVATE_RULE, methods=["GET"], endpoint="FOO")
def app_test():
    return "HELLO_APP"

app_b = UrlDiscovery.private(Blueprint(PRIVATE_BLUEPRINT, __name__))


@app_b.route("/app/another", methods=["GET"], endpoint="BOOYA")
def app_another():
    return "yet another"


@app_b.route("/test/boo/", methods=["GET"])
def t():
    return "foo"


def setup_helper(service, test_port):
    service.config['TESTING'] = True

    server_agrs = {
        'host': TEST_HOST,
        'port': test_port,
        'use_reloader': False
    }

    service.debug = True

    server_process = Process(target=service.run, kwargs=server_agrs)
    server_process.start()
    time.sleep(1)
    return server_process


class TestDiscovery(unittest.TestCase):

    def setUp(self):
        app.register_blueprint(app_b)
        self.test_app = app.test_client()
        self.app_proc = setup_helper(app, 5000)

    def tearDown(self):
        self.app_proc.terminate()

    def test_UrlDiscovery(self):
        """
        Url Discovery Test evaluates a response from registered test flask app.
        After registration new blueprint is added to an app collecting all available routes
        :return: void
        """
        print()
        print("======== Testing Url Discovery ========")
        response_obj = requests.get('http://localhost:5000/config/routes/')
        print(response_obj.content.decode("utf-8"))
        self.assertEquals(json.loads(test_response).keys(), json.loads(response_obj.content.decode("utf-8")).keys())

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
        success, urls, traceback = obtain_urls('localhost:5000', 'localhost:5000')
        self.assertTrue(success)
        self.assertFalse(traceback)
        print(urls)
        for item in urls.values():
            self.assertEquals(json.loads(test_response).keys(), item.keys())
