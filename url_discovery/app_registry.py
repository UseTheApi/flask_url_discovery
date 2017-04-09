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


@app.route("/test/app/", methods=["GET"])
def app_test():
    return "HELLO_APP"


blue_url_discovery = Blueprint(UD_PATTERN, __name__)


@blue_url_discovery.route(routes_url, methods=["GET"])
def expose_routes():
    global links
    return jsonify(links) 


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


def process_url_string(url: str):
    url_list = url.split(UD_PATTERN)
    return "".join(url_list[1:])


def url_discovery(flask_application: Flask):
    global links
    links.clear()
    server_name = flask_application.config['SERVER_NAME']
    flask_application.config['SERVER_NAME'] = "url_discovery"
    with flask_application.app_context():
        for rule in flask_application.url_map.iter_rules():
            if has_no_empty_params(rule):
                links[rule.endpoint] = dict()
                route = url_for(rule.endpoint, **(rule.defaults or {}))
                links[rule.endpoint].setdefault("active_urls", process_url_string(route))
                links[rule.endpoint].setdefault("methods", list(rule.methods))
    flask_application.config['SERVER_NAME'] = server_name


def url_registry(flask_application: Flask):
    flask_application.register_blueprint(blue_url_discovery)
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

