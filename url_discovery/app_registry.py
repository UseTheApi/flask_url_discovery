#! /bin/usr/python3

from flask import Flask, url_for, Blueprint
from flask import jsonify
import requests
from http import HTTPStatus

__author__ = "Alena Lifar"
__email__ = "alenaslifar@gmail.com"
__version__ = "0.0.1"
__phase__ = "alpha"
__date__ = "04/08/2017"

UD_PATTERN = "url_discovery"  # unified url_discovery pattern


links = dict()
routes_url = "/config/routes/"


app = Flask(__name__)


class UrlDiscovery(object):
    routes_url = "/config/routes"
    links = dict()
    private_endpoints = list()
    private_blueprints_names = list()
    blue_url_discovery = Blueprint(UD_PATTERN, __name__)

    @classmethod
    def add_private_link(cls, name):
        print("ADD PRIVATE LINK")
        cls.private_endpoints.append(name)

    @classmethod
    def add_private_bp(cls, bp):
        print("ADD PRIVATE BP")
        cls.private_blueprints_names.append(bp.name)

    @staticmethod
    def private(bp=None):
        if bp:
            UrlDiscovery.add_private_bp(bp)
            return bp

        def decorator(func):
            UrlDiscovery.add_private_link(func.__name__)
            return
        return decorator


@UrlDiscovery.blue_url_discovery.route(routes_url, methods=["GET"])
def expose_routes():
    return jsonify(UrlDiscovery.links)


@UrlDiscovery.private()
@app.route("/test/app/", methods=["GET"], endpoint="FOO")
def app_test():
    return "HELLO_APP"


@app.route("/app/new/", methods=["GET"])
def app_new():
    return "HELLO_WORLD"


@app.route("/app/another", methods=["GET"])
def app_another():
    return "yet another"


@app.route("/test/boo/", methods=["GET"])
def t():
    return "foo"


def validate_blueprint(endpoint):
    bp = endpoint.split(".")
    if len(bp) > 1:
        print("PRIVATE")

    print(bp)
    return True


# http://stackoverflow.com/questions/13317536/get-a-list-of-all-routes-defined-in-the-app#13318415
def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


def process_url_string(url: str):
    url_list = url.split(UD_PATTERN)
    return "".join(url_list[1:])


def construct_link_dict(rule, route):
    return dict(
        active_urls=process_url_string(route),
        methods=list(rule.methods)
    )


def get_route(rule):
    return url_for(rule.endpoint, **(rule.defaults or {}))


def url_discovery(flask_application: Flask):
    UrlDiscovery.links.clear()
    server_name = flask_application.config['SERVER_NAME']
    flask_application.config['SERVER_NAME'] = "url_discovery"
    with flask_application.app_context():
        non_empty_rules = [rule for rule in flask_application.url_map.iter_rules()
                           if has_no_empty_params(rule)
                           and validate_blueprint(rule.endpoint)]

        rules_and_routes = [(rule, get_route(rule)) for rule in non_empty_rules]

        UrlDiscovery.links = {rule.endpoint: construct_link_dict(rule, route) for rule, route in rules_and_routes}

    flask_application.config['SERVER_NAME'] = server_name


def url_registry(flask_application: Flask):
    flask_application.register_blueprint(UrlDiscovery.blue_url_discovery)
    url_discovery(flask_application)
    return flask_application


def obtain_urls(*args, https=False):
    """
    Obtain Urls requests routes from provided sources by requesting their registered API
    :param args: a number of parameters of format: str - "host:port" or "domain_name"
    :param https: boolean
    :return: tuple:
        success: boolean - True if all of the provided args are valid
        url_collection: dict - dictionary of successfully requested urls
        traceback: dict - traceback per invalid arg
    """
    base = "https://" if https else "http://"
    url_collection = dict()
    success = True
    traceback = dict()

    for dependent_host_port in args:
        uri_string = base + dependent_host_port + routes_url
        try:
            r = requests.get(uri_string)
            if r.status_code == HTTPStatus.OK:
                dependent_urls_dict = r.json()
            else:
                traceback[dependent_host_port] = r
                success = False
                continue
        except requests.exceptions.ConnectionError as e:
            traceback[dependent_host_port] = e
            success = False
            continue
        url_collection[dependent_host_port] = dependent_urls_dict
    return success, url_collection, traceback


if __name__ == "__main__":
    url_registry(app)
    app.run("0.0.0.0", port=5000)
    # s, c, t = obtain_urls("localhost:6000", "localhost:5000")

