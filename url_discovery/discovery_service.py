#! /bin/usr/python3

import requests

__author__ = "Alena Lifar"
__email__ = "alenaslifar@gmail.com"
__version__ = "0.0.1"
__phase__ = "alpha"
__date__ = "04/08/2017"


class DiscoveryService(object):
    def __init__(self):
        self.__put_json_headers = {
                'content-type': 'application/json',
                'Accept': 'application/json'
                }
        self.__get_json_headers = {'Accept': 'application/json'}

        self.__post_xml_headers = {
                'content-type': 'application/xml',
                'Accept': 'application/xml'
                }
        self.__get_xml_headers = {'Accept': 'application/xml'}
        self.__http_base = "http://"
        self.__unified_url_of_dependents = "/config/routes/"

    @property
    def put_json_headers(self):
        return self.__put_json_headers

    @put_json_headers.setter
    def put_json_headers(self, value):
        pass

    @property
    def get_json_headers(self):
        return self.__get_json_headers

    @get_json_headers.setter
    def get_json_headers(self, value):
        pass

    @property
    def post_xml_headers(self):
        return self.__post_xml_headers

    @post_xml_headers.setter
    def post_xml_headers(self, value):
        pass

    @property
    def get_xml_headers(self):
        return self.__get_xml_headers

    @get_xml_headers.setter
    def get_xml_headers(self, value):
        self.__get_xml_headers = value

    @property
    def http_base(self):
        return self.__http_base

    @http_base.setter
    def http_base(self, value):
        pass

    @property
    def unified_url_of_dependents(self):
        return self.__unified_url_of_dependents

    @unified_url_of_dependents.setter
    def unified_url_of_dependents(self, value):
        self.__unified_url_of_dependents = value

    def obtain_urls(self, *args):
        url_collection = list()
        for dependent_host_port in args:
            uri_string = self.http_base + dependent_host_port + self.unified_url_of_dependents
            r = requests.get(uri_string)
            dependent_urls_dict = r.json()
            url_collection.append(dependent_urls_dict)
        return url_collection

