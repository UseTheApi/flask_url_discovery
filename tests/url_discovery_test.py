#! /bin/usr/python3

from .test_base import TestBase

from flask_url_discovery.app_registry import discover_urls

__author__ = "Alena Lifar"
__email__ = "alenaslifar@gmail.com"
__date__ = "05/08/2017"

TEST_BLUEPRINT_NAME = 'test_bp1'

app1_simple_case_links = ['test_route2', 'test_route1', 'static']

app1_custom_endpoint_ud_links = ['test_endpoint', 'test_route1', 'static']

app1_registered_blueprint = ['{0}.bp_test_route1'.format(TEST_BLUEPRINT_NAME),
                             '{0}.bp_test_endpoint'.format(TEST_BLUEPRINT_NAME),
                             'test_route1',
                             'static']


class UrlDiscoveryTest(TestBase):

    def setUp(self):
        TestBase.setUp(self)

    def test_DiscoverUrls(self):
        """
        Collects routes from url_map that gets mapped to name of a view_function.
        Validates result dictionary that gets stored directly in the flask application
        :return: void
        """
        print()
        print("====== TEST DISCOVER URLS SIMPLE ======")

        @self.app1.route('/test/second_rule')
        def test_route2():
            """
            Test url_rule + view_function
            :return: void
            """
            return

        discover_urls(self.app1)
        print("Collected Links: ", self.app1.ud_links)
        self.assertEqual(sorted(list(self.app1.ud_links.keys())), sorted(app1_simple_case_links))

    def test_DiscoverUrlsCustomEndpoint(self):
        """
        Collects routes from url_map that gets mapped to name of a view_function or endpoint.
        Validates result dictionary that gets stored directly in the flask application
        :return: void
        """
        print()
        print("====== TEST DISCOVER URLS CUSTOM ENDPOINT ======")

        @self.app1.route('/test/custom_endpoint', endpoint='test_endpoint')
        def test_route2():
            """
            Test url_rule + view_function. Custom endpoint is used
            :return: void
            """
            return

        discover_urls(self.app1)
        print("Collected Links: ", self.app1.ud_links)
        self.assertEqual(sorted(list(self.app1.ud_links.keys())), sorted(app1_custom_endpoint_ud_links))

    def test_DiscoverUrlsFromBlueprint(self):
        """
        Registers a blueprint into an application
        Collects routes from url_map that gets mapped to name of a view_function or endpoint.
        Validates result dictionary that gets stored directly in the flask application
        :return: void
        """
        print()
        print("====== TEST DISCOVER URLS FROM BLUEPRINT ======")

        self.app1.register_blueprint(self.public_blueprint1)

        print(self.app1.url_map)

        discover_urls(self.app1)
        print("Collected Links: ", self.app1.ud_links)
        self.assertEqual(sorted(list(self.app1.ud_links.keys())), sorted(app1_registered_blueprint))

    def test_DiscoverUrlsFromBlueprint_UrlPrefix(self):
        """
        Registers a blueprint into an application with 'url_prefix'
        Collects routes from url_map that gets mapped to name of a view_function or endpoint.
        Validates result dictionary that gets stored directly in the flask application
        :return: void
        """
        print()
        print("====== TEST DISCOVER URLS FROM BLUEPRINT -- URL PREFIX ======")

        test_url_prefix = "/test_prefix"

        self.app1.register_blueprint(self.public_blueprint1, url_prefix=test_url_prefix)

        discover_urls(self.app1)
        print("Collected Links: ", self.app1.ud_links)
        blueprint_links = [link for link in self.app1.ud_links if '.' in link]

        link_list = [self.app1.ud_links[link]['active_urls'][0] for link in blueprint_links]
        # print(link_list)
        [self.assertTrue(test_url_prefix in link) for link in link_list]

    def test_DiscoverUrlsMultipleRules(self):
        """
        Assigns multiple rules to an endpoint
        Collects routes from url_map that gets mapped to name of a view_function or endpoint.
        Validates result dictionary that gets stored directly in the flask application
        :return: void
        """
        print()
        print("====== TEST DISCOVER URLS MULTIPLE RULES ======")

        @self.app1.route('/test/multiple/')
        @self.app1.route('/test/routes/')
        def multiple_routes():
            return

        discover_urls(self.app1)
        print("Collected Links: ", self.app1.ud_links)
        self.assertEqual(len(self.app1.ud_links['multiple_routes']['active_urls']), 2)
