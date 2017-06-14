from setuptools import setup
from os.path import join, dirname

with open(join(dirname(__file__), 'flask_url_discovery/version.py'), 'r') as f:
    exec(f.read())

with open(join(dirname(__file__), 'requirements.txt'), 'r') as f:
    install_requires = f.read().split("\n")
    print(install_requires)

setup(
    name='Flask-UrlDiscovery',
    version=__version__,
    url='https://github.com/UseTheApi/flask_url_discovery',
    license='MIT',
    author='Alena Lifar',
    author_email='alenaslifar@gmail.com',
    description="A Flask extension for discovering urls in a service. Automatically exposes urls for a service",
    long_description=open('README.rst').read(),
    packages=['flask_url_discovery'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=install_requires,
    test_suite='tests',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
