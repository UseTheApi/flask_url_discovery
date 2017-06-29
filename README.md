# Flask Url Discovery

A Flask extension for discovering urls in a service and expose service's routes for others.

## Installation

Install the extention using ``pip`` or ``easy_install``.

```bash
$ pip install -U Flask-UrlDiscovery
```

## Usage

This package exposes a Flask extention that allows the user to automatically collect all (by default) routes that are created by Flask application or a Blueprint. The user can provide a custom uri string for exposing routes on the system as well as restrict the access to some routes or Blueprints.


### Usage with Flask app and Blueprint

In order to expose all routes on the system the user only has to register Flask application with ```url_discovery```:

```python
from flask import Flask, Blueprint
from flask_url_discovery import url_discovery

app = Flask(__name__)
url_discovery(app)

app_bp = Blueprint("my_bp", __name__)


@app.route("/")
def hello_world():
  return "Hello World!"

@app_bp.route("/hello/")
def hello_bp():
  return "Hello Flask Blueprint"

if __name__ == "__main__":
  app.register_blueprint(app_bp)
  app.run('0.0.0.0', 5000)
```

By default all of the routes are getting exposed on http://host::port/**config/routes/**

Here is sample response for **/config/routes/**  ```GET``` request:

```json
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
            "/"
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
```

### Custom routes url

The user can specify custom routes url for url discovery

```python
    from flask import Flask
    from flask_url_discovery import url_discovery
    
    app = Flask(__name__)
    url_discovery(app, custom_routes_url="/your_custom_routes_url/")
    
    @app.route("/")
    def helloWorld():
      return "Hello World!"
```

Flask UrlDiscovery perfectly works with ```url_prefix``` for Flask Blueprints:

```python
from flask import Flask, Blueprint
from flask_url_discovery import url_discovery

app = Flask(__name__)
url_discovery(app)

app_bp = Blueprint("my_bp", __name__)


@app.route("/")
def hello_world():
  return "Hello World!"

@app_bp.route("/hello/")
def hello_bp():
  return "Hello Flask Blueprint"

if __name__ == "__main__":
  app.register_blueprint(app_bpm url_prefix="/custom_prefix")
  app.run('0.0.0.0', 5000)
```

Response:
```json
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
```

### Private routes and Blueprints


