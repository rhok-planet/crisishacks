#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyPI information fetcher per repo
"""

from datetime import datetime
import locale
import sys
import xmlrpclib

locale.setlocale(locale.LC_ALL, '')

class PypiVersion(object):
    
    def __init__(self, release_data):
        self.__dict__.update(release_data)
        
def fetch_releases(hack_name, include_hidden=True):
    
    if not hack_name:
        raise TypeError("hack_name requires a valid hack name")
    
    hack_name = hack_name
    include_hidden = include_hidden
    proxy = xmlrpclib.Server('http://pypi.python.org/pypi')
            
    releases = []
    
    for version in proxy.hack_releases(hack_name, include_hidden):
        release_data = PypiVersion(proxy.release_data(hack_name, version))
        release_data.hidden = release_data._pypi_hidden

        release_data.downloads = 0
        for download in proxy.release_urls(hack_name, version):
            release_data.downloads +=  download["downloads"]
            
        releases.append(release_data)    
    return releases