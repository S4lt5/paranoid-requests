""" Module containing basic proxy list functionality, used by both paranoid implementations"""
import os
import re
import itertools
import requests



class MissingProxyListError(Exception):
    """
    Used when ProxyList is called, but no or empty list of proxy servers is
    """



class ProxyListDownloadError(Exception):
    """
    Used when the public proxy service cannot be queried
    """

class InvalidProxyError(Exception):
    """
    Thrown when we can obviously see that the passed object is not a (addr,port) tuple
    """




class ProxyList:
    """A list of proxies, to be used in creating a round-robin generator
    exposed via the get_next_proxy() method"""
    def __init__(self, proxies):
        """
        Take the passed proxy list, or create a blank one

        Proxy is a list of tuples: [('address','port'),...]
        """
        if not proxies or not hasattr(proxies, '__len__') or len(proxies) < 1:
            raise MissingProxyListError("A non empty proxylist must be provided to ProxyList()")

        for prox in proxies:
            if not prox or not hasattr(proxies,'__len__') or len(prox) != 2:
                raise InvalidProxyError("Each proxy must be a two-value tuple containing the address and port")


        # do I really need this?
        self.proxies = proxies
        #Create an infinite iterator that cycles through all of the proxies
        self.generator = itertools.cycle(proxies)

    def get_next_proxy(self):
        """Return the next proxy to be used as a tuple (host,port)"""
        return next(self.generator)


#for determining if a host is valid
PROXY_REGEX=re.compile(r"^((?:(?:[a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*(?:[A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])):([\d]+)$")

class ProxyListLoader:
    """A file-based proxy list loader that reads one entry per line in host:port format"""
    @staticmethod
    def from_text_file(input_path):
        """Load a proxy list from a multiline text file with the format address:port, one per line."""

        if not os.path.exists(input_path) or not os.path.isfile(input_path):
            raise FileNotFoundError(f"The input file {input_path} does not exist.")


        with open(input_path,'r') as file:
            content = file.read()
            return ProxyListLoader.from_string(content)

    @staticmethod
    def from_string(proxylist_contents):
        """Read a proxy list from a string, one proxy per line in host:port format"""
        proxies = []
        for line in proxylist_contents.split("\n"):
            line = line.strip()
            proxy = ProxyListLoader.parse_proxy_entry(line)
            proxies.append(proxy)


        return ProxyList(proxies=proxies)

    @staticmethod
    def from_url(url):
        """Load a proxy list from a URL, the url must have text content with the format addresS:port, one per line."""
        resp = requests.get(url,timeout=20)

        if resp.status_code != 200:
            raise ProxyListDownloadError(f"Can't download the proxy list from {url}")

        return ProxyListLoader.from_string(resp.text)



    public_http_proxies_url = "https://cdn.jsdelivr.net/gh/TheSpeedX/PROXY-List@master/http.txt"
    @staticmethod
    def from_default_public_proxy_list():
        """Load a proxy list from TheSpeedX's list of public proxies
        See https://github.com/TheSpeedX/PROXY-List for up to date licensing info."""

        return ProxyListLoader.from_url(ProxyListLoader.public_http_proxies_url)



    @staticmethod
    def parse_proxy_entry(line):
        """Validate a line of text iput that will be turned into a proxy entry, then return a tuple of host,port"""
        match = PROXY_REGEX.search(line)
        if match is None:
            raise InvalidProxyError(f"The proxy entry {line} is not in the correct format of 'host:port'")

        #match 1 is the host, match 2 is the port
        return (match[1],int(match[2]))
