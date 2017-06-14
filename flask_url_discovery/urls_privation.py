#! /bin/usr/python3

__author__ = "Alena Lifar"
__email__ = "alenaslifar@gmail.com"
__date__ = "05/08/2017"

private_view_functions = list()
private_blueprints = list()


def add_private_link(func):
    """
    Appends func to private collection

    :param func: decorated function
    :return: void
    """
    global private_view_functions
    private_view_functions.append(func)


def add_private_bp(bp):
    """
    Adds a Blueprint name into collection

    :param bp: flask Blueprint
    :return:
    """
    global private_blueprints
    private_blueprints.append(bp)


def private(bp=None):
    """
    Function and Decorator that allows a user to private some urls and blueprints.
    Decorator usage is preferable when used with 'app.route' decorator.
    Intended to be used as function for 'Flask.Blueprint' and 'app.add_url_rule'

    Usage:
        **with routes:** ::

            @private()
            @app.route('/route/', methods=['GET'], **options)
            def view_func():
                '''
                this is your function
                '''

    Usage:
        **with blueprints:** ::

            some_bp = private(Blueprint("name", __name__))

        *or*::

            some_bp = Blueprint("name", __name__)
            private(some_bp)

    private does not modify route or blueprint

    :param bp: flask Blueprint
    :type bp: Flask.Blueprint
    :return: func
    """
    if bp:
        add_private_bp(bp)
        return bp

    def decorator(func):
        add_private_link(func)
        return
    return decorator
