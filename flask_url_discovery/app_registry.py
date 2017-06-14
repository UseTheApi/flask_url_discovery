#! /bin/usr/python3

from flask import current_app, jsonify
from flask_url_discovery import env, utils

__author__ = "Alena Lifar"
__email__ = "alenaslifar@gmail.com"
__date__ = "05/08/2017"


def expose_routes():
    """
    Route for exposed URLs of a service

    :return: dictionary of links
    """
    with current_app.app_context():
        links = jsonify(current_app.ud_links)
    return links


def discover_urls(flask_application):
    """
    Iterates through url_map and filters rules to expose available routes for a service
    Attaches contructed links dictionary to flask_application

    :param flask_application:
    :type flask_application: Flask

    :return: void
    """
    server_name = flask_application.config['SERVER_NAME']
    flask_application.config['SERVER_NAME'] = "flask_url_discovery"
    with flask_application.app_context():
        non_empty_rules = [rule for rule in flask_application.url_map.iter_rules()
                           if utils.validate_endpoint(rule.endpoint)]

        rules_and_routes = [
            (rule, rule.rule) for rule in non_empty_rules
            ]

        links = dict()

        for rule, route in rules_and_routes:
            if links.get(rule.endpoint, None):
                links[rule.endpoint]['active_urls'].append(route)
            else:
                links[rule.endpoint] = utils.construct_link_dict(rule, route)

        flask_application.ud_links = links

    flask_application.config['SERVER_NAME'] = server_name


def register(application, route_url):
    """
    Assigns application to class property flask_app
    Wraps flask run() method in order to invoke url discovery on the run()

    :param application:
    :type application: Flask

    :param route_url: custom link for exposing all routes of the system
    :type route_url: str

    :return: void
    """

    # Adding a rule to flask_url_discovery blueprint
    env.blue_url_discovery.add_url_rule(
            route_url,
            'expose_routes',
            expose_routes,
            methods=['GET']
        )

    run_func = getattr(application, 'run')

    def url_discovery_run(*args, **kwargs):
        discover_urls(application)
        return run_func(*args, **kwargs)

    setattr(application, 'run', url_discovery_run)


def url_discovery(flask_application, custom_routes_url=None):
    """
    Registers flask application within url discovery
    discovers all available routes for the app and exposing it at a new route

    by default: http://{uri}/config/routes/
    you may reset this route by setting providing custom_url parameter

    :param flask_application:
    :type flask_application: Flask

    :param custom_routes_url: custom uri for routes
    :type custom_routes_url: str

    :return: void
    """
    register(flask_application, custom_routes_url or env.default_routes_url)
    flask_application.register_blueprint(env.blue_url_discovery)
    return flask_application
