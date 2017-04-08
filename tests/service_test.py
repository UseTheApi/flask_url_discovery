#! /bin/usr/python3

import unittest

import time
from flask import Flask
from multiprocessing import Process

__author__ = "Alena Lifar"
__email__ = "alenaslifar@gmail.com"
__version__ = "0.0.1"
__phase__ = "alpha"
__date__ = "04/08/2017"


TEST_HOST = "0.0.0.0"
app1 = Flask(__name__)
app2 = Flask(__name__)


@app1.route("/test/app1/", methods=["GET"])
def test_app1():
    return "Hello from app1"


@app2.route("/test/app2", methods=["GET"])
def test_app2():
    return "Hello from app2"


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


def url_discovery(app):
    return app


class TestServiceUrlDiscovery(unittest.TestCase):
    registered_app1 = None
    registered_app2 = None
    server1_process = None
    server2_process = None

    @classmethod
    def setUpClass(cls):
        cls.registered_app1 = url_discovery(app1)
        cls.registered_app2 = url_discovery(app2)

    def setUp(self):
        TestServiceUrlDiscovery.server1_process = setup_helper(TestServiceUrlDiscovery.registered_app1, 5001)
        TestServiceUrlDiscovery.server2_process = setup_helper(TestServiceUrlDiscovery.registered_app2, 5002)

    def tearDown(self):
        TestServiceUrlDiscovery.server1_process.terminate()
        TestServiceUrlDiscovery.server2_process.terminate()

    def test_UrlDiscovery(self):
        pass
