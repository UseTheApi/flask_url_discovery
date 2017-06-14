#! /bin/usr/python3

from flask import current_app
from flask_url_discovery import urls_privation

__author__ = "Alena Lifar"
__email__ = "alenaslifar@gmail.com"
__date__ = "05/08/2017"


def validate_blueprint(endpoint):
    return endpoint not in [bp_name.name for bp_name in urls_privation.private_blueprints]


def validate_route(endpoint):
    with current_app.app_context():
        return not current_app.view_functions.get(endpoint, None) in urls_privation.private_view_functions


def validate_endpoint(endpoint):
    endpoint_list = endpoint.split(".")
    return validate_blueprint(endpoint_list[0]) if len(endpoint_list) > 1 else validate_route(endpoint)


def construct_link_dict(rule, route):
    route_list = [route]
    return dict(
        active_urls=route_list,
        methods=list(rule.methods)
    )
