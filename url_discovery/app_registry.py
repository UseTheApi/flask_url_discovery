#! /bin/usr/python3

from flask import Flask, url_for, Blueprint, Response
from flask.json import jsonify
from multiprocessing import Process
import json

__author__ = "Alena Lifar"
__email__ = "alenaslifar@gmail.com"
__version__ = "0.0.1"
__phase__ = "alpha"
__date__ = "04/08/2017"

UD_PATTERN = "url_discovery"  # unified url_discovery pattern


a = Blueprint("a", __name__)

links = dict()
routes_url = "/config/routes/"


class JSONyfiedResponse(Response):
    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(JSONyfiedResponse, cls).force_type(rv, environ)


@a.route("/app/info/", methods=["GET", "POST"])
def app_info():
    return "Hello_world"


@a.route("/app/test/", methods=["GET", "POST"])
def app_test():
    return "HELLO_APP_TEST"


blue_url_discovery = Blueprint(UD_PATTERN, __name__)


@blue_url_discovery.route(routes_url, methods=["GET"])
def expose_routes():
    global links
    return json.dumps(links)


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
    print(links)


def url_registry(flask_application: Flask):
    flask_application.register_blueprint(blue_url_discovery)
    url_discovery(flask_application)
    return flask_application


server_args = {
        "host": "0.0.0.0",
        "port": 5000,
}


if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(a)
    url_registry(app)
    app.run("0.0.0.0", port=5000)

