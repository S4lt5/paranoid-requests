""" Module containing automatic public proxy list parser"""
from paranoid_requests.paranoid_core import ProxyList

class PublicProxyList(ProxyList):
    """A class that automatically pulls public HTTP proxy list and creates a ProxyList"""
