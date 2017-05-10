#! /bin/usr/python3

from flask import Flask

from .test_base import TestBase
from flask_url_discovery.urls_privation import private
from flask_url_discovery.app_registry import discover_urls


app1_simple_case_links = ['test_route1', 'static']

app1_private_blueprint_links = ['static']


class TestPrivateUrls(TestBase):

    def setUp(self):
        super().setUp()

    def test_PrivateLink(self):
        """
        Adds a private rule to an app.
        Validates that the added rule was hidden and not exposed
        :return: void
        """
        print()
        print("====== TEST PRIVATE LINK ======")

        @private()
        @self.app1.route("/test/hidden_rule/")
        def hidden_rule():
            """
            Test url_rule + view_function
            :return: void
            """
            return

        discover_urls(self.app1)
        print("Collected Links: ", self.app1.ud_links)
        self.assertEqual(list(self.app1.ud_links.keys()), app1_simple_case_links)

    def test_PrivateLink_CustomEndpoint(self):
        """
        Adds a private rule to an app with custom endpoint.
        Validates that the added rule was hidden and not exposed
        :return: void
        """
        print()
        print("====== TEST PRIVATE LINK -- CUSTOM ENDPOINT ======")

        @private()
        @self.app1.route("/test/hidden_rule/", endpoint="test_endpoint1")
        def test_endpoint():
            """
            Test url_rule + view_function. Custom endpoint is used
            :return: void
            """
            return

        discover_urls(self.app1)
        print("Collected Links: ", self.app1.ud_links)
        self.assertEqual(list(self.app1.ud_links.keys()), app1_simple_case_links)

    def test_PrivateBlueprint(self):
        """
        Privates a blueprint.
        Registers a blueprint into an application.
        Collects routes from url_map that gets mapped to name of a view_function or endpoint.
        Validates result dictionary that gets stored directly in the flask application
        :return: void
        """
        print()
        print("====== TEST PRIVATE BLUEPRINT ======")

        app2 = Flask(__name__)

        private(self.private_blueprint)
        app2.register_blueprint(self.private_blueprint)

        discover_urls(app2)
        print("Collected Links: ", app2.ud_links)
        self.assertEqual(list(app2.ud_links.keys()), app1_private_blueprint_links)
