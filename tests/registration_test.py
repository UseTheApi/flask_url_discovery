#! /bin/usr/python3

from flask import Flask

from .test_base import TestBase
from flask_url_discovery.app_registry import url_discovery

# from unittest.mock import Mock, patch
from mock import Mock, patch
from multiprocessing import Process
import time
import json
import requests

app1_simple_case_links = ['flask_url_discovery.expose_routes', 'test_route1', 'static']
app2_links = ['flask_url_discovery.expose_routes', 'static']

TEST_HOST = "0.0.0.0"


def setup_helper(service, test_port):
    service.config['TESTING'] = True

    server_agrs = {
        'host': TEST_HOST,
        'port': test_port,
        'use_reloader': False
    }

    service.debug = True

    server_process = Process(target=service.run, kwargs=server_agrs)
    return server_process


class RegistrationTest(TestBase):

    def setUp(self):
        TestBase.setUp(self)
        self.app2 = Flask(__name__)

    @patch('flask.Flask.run')
    def test_Registration(self, run_mock):
        """
        Checks that discover_urls method is called on flask application run() method
        :param run_mock: run method for flask app mock object
        :type run_mock: Mock
        :return: void
        """
        print()
        print("====== TEST REGISTRATION ======")

        discover_urls_mock = Mock()

        with patch('flask_url_discovery.app_registry.discover_urls', new=discover_urls_mock):
            url_discovery(self.app1)
            self.app1.run()
            discover_urls_mock.assert_called_once()

    @patch('flask.Flask.run')
    def test_UrlDiscoveryBlueprint(self, run_mock):
        """
        Checking that run method for a flask app invokes discovery of urls
        and stores it into an app object
        :param run_mock: run method for flask app mock object
        :type run_mock: Mock
        :return: void
        """
        print()
        print("====== TEST URL DISCOVERY BLUEPRINT ======")

        run_mock.return_value = True

        url_discovery(self.app1)

        # invoking an application run
        self.app1.run()

        # makes sure that url_discovery blueprint is registered to app
        self.assertEqual(sorted(list(self.app1.ud_links.keys())), sorted(app1_simple_case_links))

    def test_ApplicationRun(self):
        """
        Registering actual application
        and invoking an actual request to a registered Blueprint route
        :return: void
        """
        print()
        print("====== TEST APPLICATION RUN ======")

        # Registering application
        url_discovery(self.app2)

        # Starting it in a separate Process in order to proceed to checks
        self.app_process = setup_helper(self.app2, 5002)
        self.app_process.start()
        time.sleep(1)

        # invoking actual request to added route
        response = requests.get('http://localhost:5002/config/routes/')

        # matching response
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(sorted(list(response_data.keys())), sorted(app2_links))
        self.app_process.terminate()


