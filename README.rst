Flask Url Discovery
===================

A Flask extension for discovering urls in a service and expose service's routes for others.

Installation
------------

Install the extention using ``pip`` or ``easy_install``.

.. code:: bash

    $ pip install -U Flask-UrlDiscovery

Usage
-----

This package exposes a Flask extention that allows the user to automatically collect all (by default) routes that are created by Flask application or a Blueprint. The user can provide a custom uri string for exposing routes on the system as well as **restrict** the access to some routes or Blueprints.


Usage with Flask app and Blueprint
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to expose all routes on the system the user only has to register Flask application with ``url_discovery``:

.. code:: python

    from flask import Flask, Blueprint
    from flask_url_discovery import url_discovery

    app = Flask(__name__)
    url_discovery(app)

    app_bp = Blueprint('my_bp', __name__)


    @app.route('/')
    @app.route('/health_check/')
    def hello_world():
      return 'Hello World!'

    @app_bp.route('/hello/')
    def hello_bp():
      return 'Hello Flask Blueprint'

    if __name__ == "__main__":
      app.register_blueprint(app_bp)
      app.run('0.0.0.0', 5000)

By default all of the routes are getting exposed on http://{host:port}/config/routes/

Here is sample response for **/config/routes/**  ``GET`` request:

.. code:: python

    {
        "flask_url_discovery.expose_routes": {
            "active_urls": [
                "/config/routes/"
            ],
            "methods": [
                "GET",
                "HEAD",
                "OPTIONS"
            ]
        },
        "hello_world": {
            "active_urls": [
                "/",
                "/health_check/"
            ],
            "methods": [
                "GET",
                "HEAD",
                "OPTIONS"
            ]
        },
        "my_bp.hello_bp": {
            "active_urls": [
                "/hello/"
            ],
            "methods": [
                "GET",
                "HEAD",
                "OPTIONS"
            ]
        },
        "static": {
            "active_urls": [
                "/static/<path:filename>"
            ],
            "methods": [
                "GET",
                "HEAD",
                "OPTIONS"
            ]
        }
    }
    
Make a use of ``enpoint`` parameter to encapsulate a function name:

.. code:: python
    
    from flask import Flask
    from flask_url_discovery import url_discovery
    
    app = Flask(__name__)
    url_discovery(app)
    
    @app.route('/hello_world/', endpoint='custom_endpoint')
    def hello_world():
        return 'Hello World!'
        
**/config/routes/** response:

.. code:: python

    <...>
    "custom_endpoint": {
            "active_urls": [
                "/hello_world/"
            ],
            "methods": [
                "GET",
                "HEAD",
                "OPTIONS"
            ]
        },
    <...>

Custom routes url
-----------------

The user can specify custom routes url for url discovery

.. code:: python

    from flask import Flask
    from flask_url_discovery import url_discovery
    
    app = Flask(__name__)
    url_discovery(app, custom_routes_url='/your_custom_routes_url/')
    
    @app.route('/')
    def hello_world():
      return 'Hello World!'

Flask UrlDiscovery perfectly works with ``url_prefix`` for Flask Blueprints:

.. code:: python

    from flask import Flask, Blueprint
    from flask_url_discovery import url_discovery

    app = Flask(__name__)
    url_discovery(app)

    app_bp = Blueprint('my_bp', __name__)


    @app.route('/')
    def hello_world():
      return 'Hello World!'

    @app_bp.route('/hello/')
    def hello_bp():
      return 'Hello Flask Blueprint'

    if __name__ == "__main__":
      app.register_blueprint(app_bpm, url_prefix='/custom_prefix')
      app.run('0.0.0.0', 5000)

**/config/routes/** response:

.. code:: python

    <...>
    "my_bp.hello_bp": {
            "active_urls": [
                "/custom_prefix/hello/"
            ],
            "methods": [
                "GET",
                "OPTIONS",
                "HEAD"
            ]
        },
    <...>

Private routes and Blueprints
-----------------------------

The user can private a single route of Flask application/Blueprint as well as a whole Blueprint. Flask UrlDiscovery provides a decorator function.

**Usage with route():**

.. code:: python

    from flask import Flask, Blueprint
    from flask_url_discovery import url_discovery, private

    app = Flask(__name__)
    url_discovery(app)

    app_bp = Blueprint('my_bp', __name__)


    @app.route('/')
    def hello_world():
        return 'Hello World!'


    @private()
    @app.route('/restricted_route/')
    def private_endpoint():
        return 'Hello Private Endpoint'


    @app_bp.route('/hello/')
    def hello_bp():
        return 'Hello Flask Blueprint'

    if __name__ == "__main__":
        app.register_blueprint(app_bp)
        app.run('0.0.0.0', 5000)

``private_endpoint()`` will not be shown in the response of ``/config/routes/`` request. Same approach is valid for privating a route of a Blueprint.

**Usage with Flask Blueprints:**

.. code:: python

    from flask import Flask, Blueprint
    from flask_url_discovery import url_discovery, private

    app = Flask(__name__)
    url_discovery(app)

    # or: app_bp = private(Blueprint('my_bp', __name__))
    app_bp = Blueprint('my_bp', __name__)
    private(app_bp)


    @app.route('/')
    def hello_world():
        return 'Hello World!'


    @app_bp.route('/private/hello/')
    def hello_bp():
        return "Hello Flask Blueprint"


    @app_bp.route('/private/goodbye/')
    def bye_bp():
        return "Goodbye Moonmen"


    if __name__ == "__main__":
        app.register_blueprint(app_bp)
        app.run('0.0.0.0', 5000)

``app_bp`` Blueprint is fully **private** now and none of the routes belong to this Blueprint will be exposed through API by UrlDiscovery

Test
----

The Package includes a `test suite <https://github.com/UseTheApi/flask_url_discovery/tree/master/tests>`_. To exercise tests run:

.. code:: bash

    python setup.py tests
    
Docs
----

The package is provided with Sphinx documentation. To create a documentation execute ``make html`` in `docs <https://github.com/UseTheApi/flask_url_discovery/tree/master/docs>`_ directory.

Contributing
------------

If you have any questions, find any bugs/problems or have an idea of an improvement, please create an issue on `GitHub <https://github.com/UseTheApi/flask_url_discovery>`_ and/or send me an e-mail.
