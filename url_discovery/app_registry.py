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


class UrlDiscovery(object):
    routes_url = "/config/routes/"
    links = dict()
    private_endpoints = list()
    private_blueprints_names = list()
    blue_url_discovery = Blueprint(UD_PATTERN, __name__)
    flask_app = None

    @classmethod
    def add_private_link(cls, func):
        """
        Maps view_func to an endpoint and stores in the collection
        :param func: decorated function
        :return: void
        """
        with cls.flask_app.app_context():
            print(cls.flask_app.view_functions)
            item = func.__name__ if func in cls.flask_app.view_functions \
                else [endpoint for endpoint in cls.flask_app.view_functions.keys()
                      if cls.flask_app.view_functions[endpoint] is func][0]
        cls.private_endpoints.append(item)

    @classmethod
    def add_private_bp(cls, bp):
        """
        Adds a Blueprint name into collection
        :param bp: flask Blueprint
        :return:
        """
        cls.private_blueprints_names.append(bp.name)

    @staticmethod
    def private(bp=None):
        """
        Function and Decorator that allows a user to private some urls and blueprints
        Usage:
            with routes:

        @UrlDiscovery.private()
        @app.route("/route/", methods=["GET"], **options)
        def view_func():
            ...

            with blueprints:

        some_bp = UrlDiscovery.private(Blueprint("name", __name__))

        or

        some_bp = Blueprint("name", __name__)
        UrlDiscovery.private(some_bp)

        UrlDiscovery.private does not modify route or blueprint

        :param bp: flask Blueprint
        :return: func
        """
        if bp:
            UrlDiscovery.add_private_bp(bp)
            return bp

        def decorator(func):
            UrlDiscovery.add_private_link(func)
            return
        return decorator


@UrlDiscovery.blue_url_discovery.route(UrlDiscovery.routes_url, methods=["GET"])
def expose_routes():
    """
    Route for exposed URL of a service
    :return: links
    """
    return jsonify(UrlDiscovery.links)


def validate_blueprint(endpoint):
    endpoint_list = endpoint.split(".")
    return not len(endpoint_list) > 1 or not endpoint_list[0] in UrlDiscovery.private_blueprints_names


def validate_route(endpoint):
    return endpoint not in UrlDiscovery.private_endpoints


# http://stackoverflow.com/questions/13317536/get-a-list-of-all-routes-defined-in-the-app#13318415
def has_no_empty_params(rule):
    """
    http://stackoverflow.com/questions/13317536/get-a-list-of-all-routes-defined-in-the-app#13318415
    :param rule: Rule werkzeug
    :return: boolean
    """
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


def process_url_string(url: str):
    """
    Stores only uri routes without hostname
    :param url: str
    :return: str
    """
    url_list = url.split(UD_PATTERN)
    return "".join(url_list[1:])


def construct_link_dict(rule, route):
    return dict(
        active_urls=process_url_string(route),
        methods=list(rule.methods)
    )


def get_route(rule):
    """
    Get route by an rule endpoint using url_for
    :param rule: Rule werkzeug
    :return: route
    """
    with UrlDiscovery.flask_app.app_context():
        return url_for(rule.endpoint, **(rule.defaults or {}))


def url_discovery(flask_application: Flask):
    """
    Iterates through url_map and filters rules to expose available routes for a service
    Fills UrlDiscovery.links dict
    :param flask_application: Flask
    :return: void
    """
    print("Private Endpoints", UrlDiscovery.private_endpoints)
    print("Private Blueprints", UrlDiscovery.private_blueprints_names)
    UrlDiscovery.links.clear()
    server_name = flask_application.config['SERVER_NAME']
    flask_application.config['SERVER_NAME'] = "url_discovery"
    non_empty_rules = [rule for rule in flask_application.url_map.iter_rules()
                       if has_no_empty_params(rule)
                       and validate_blueprint(rule.endpoint) and validate_route(rule.endpoint)]

    rules_and_routes = [(rule, get_route(rule)) for rule in non_empty_rules]

    UrlDiscovery.links = {rule.endpoint: construct_link_dict(rule, route) for rule, route in rules_and_routes}

    flask_application.config['SERVER_NAME'] = server_name


def url_registry(flask_application: Flask):
    """
    Registers flask application within url discovery
    discovers all available routes for the app and exposing it at a new route

    by default: http://{uri}/config/routes/
    you may reset this route by setting UrlDiscovery.routes_url
    :param flask_application: Flask
    :return: void
    """
    flask_application.register_blueprint(UrlDiscovery.blue_url_discovery)
    UrlDiscovery.flask_app = flask_application
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
        uri_string = base + dependent_host_port + UrlDiscovery.routes_url
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
    app = Flask(__name__)
    # app.register_blueprint(app_b)
    url_registry(app)
    print(app.url_map)
    app.run("0.0.0.0", port=5000)
    # s, c, t = obtain_urls("localhost:6000", "localhost:5000")

