#! /bin/usr/python3

from flask import Flask, Blueprint
import unittest

TEST_BLUEPRINT_NAME = 'test_bp1'


class TestBase(unittest.TestCase):

    def setUp(self):
        self.app1 = Flask('test_app1')
        self.public_blueprint1 = Blueprint(TEST_BLUEPRINT_NAME, __name__)

        @self.app1.route('/test/')
        def test_route1():
            """
            Test url_rule + view_function
            :return: void
            """
            return

        @self.public_blueprint1.route('/bp_route1/')
        def bp_test_route1():
            """
            Test url_rule + view_function
            :return: void
            """
            return

        @self.public_blueprint1.route('/bp_route2/', endpoint='bp_test_endpoint')
        def bp_test_route2():
            """
            Test url_rule + view_function. Custom endpoint is used
            :return: void
            """
            return

        self.private_blueprint = Blueprint("test_bp", __name__)

        @self.private_blueprint.route('/bp_route1/')
        def bp_test_route1():
            """
            Test url_rule + view_function
            :return: void
            """
            return

        @self.private_blueprint.route('/bp_route2/', endpoint='bp_test_endpoint')
        def bp_test_route2():
            """
            Test url_rule + view_function. Custom endpoint is used
            :return: void
            """
            return
